"""Analyst agent for HumanEval results.

Uses:
- sensei-1337: Clear communication, accuracy-first analysis
- Strawberry: Deliberate, slow thinking
- COVE (Chain of Verification): Draft → Verify → Independent verification → Synthesize

Outputs:
- results-analysis.md: Polished markdown report
- results-analysis.html: Styled HTML version
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock

# Load sensei skill for incorporation
SENSEI_SKILL = Path("/Users/yza.vyas/.claude/skills/sensei-1337/SKILL.md").read_text()

ANALYST_SYSTEM_PROMPT = f"""You are an experiment analyst using rigorous methodology.

## Methodology

### 1. Strawberry Approach (Deliberate Thinking)
Before drawing conclusions:
- Count letters if asked (this is a metaphor for slowing down)
- Check each assumption explicitly
- State what you observe vs what you infer
- Question your first interpretation

### 2. COVE (Chain of Verification)
Four-phase analysis:
1. **Draft**: Initial observations and claims
2. **Verify**: For each claim, ask "what would prove this wrong?"
3. **Independent Verification**: Re-examine data without looking at draft
4. **Synthesize**: Reconcile verified findings into final analysis

### 3. Accuracy Standards (from sensei-1337)
- Distinguish findings from inferences
- State what was actually measured
- Acknowledge limitations
- Would an honest skeptic accept this framing?

## Output Format

Your analysis must include:

### For Markdown Report:
- Executive summary (30 seconds)
- Key findings table
- Detailed analysis with evidence
- Methodology notes (what COVE verification found)
- Limitations and caveats
- Raw data summary

### For HTML Report:
- Same content with tasteful styling
- Clean typography (system fonts, good line height)
- Tables with proper styling
- Responsive layout
- No external dependencies (inline CSS)

## Skills Context

{SENSEI_SKILL[:2000]}  # Truncated for context

## Your Task

Analyze the HumanEval benchmark results comparing single-shot vs ralph-style iteration.
Use COVE methodology: draft your analysis, verify each claim, then synthesize.
Be precise about what the data shows vs what we infer from it.
"""


async def run_analyst(results_file: str) -> tuple[str, str]:
    """Run the analyst agent on results file.

    Returns (markdown_content, html_content).
    """
    results_path = Path(results_file)
    results_data = json.loads(results_path.read_text())

    workspace = results_path.parent

    options = ClaudeAgentOptions(
        system_prompt=ANALYST_SYSTEM_PROMPT,
        allowed_tools=["Read", "Write"],
        model="sonnet",  # Use Sonnet for analysis quality
        cwd=str(workspace),
        permission_mode="acceptEdits",
    )

    analysis_prompt = f"""Analyze these HumanEval benchmark results using COVE methodology.

## Results Data

```json
{json.dumps(results_data, indent=2)}
```

## Your Task

1. **COVE Phase 1 - Draft**: Write initial observations
2. **COVE Phase 2 - Verify**: For each claim, state what would prove it wrong
3. **COVE Phase 3 - Independent**: Re-read the data fresh, note any new observations
4. **COVE Phase 4 - Synthesize**: Reconcile into final verified analysis

## Output Requirements

1. First, write a polished analysis to `results-analysis.md`
2. Then, write a styled HTML version to `results-analysis.html`

The HTML should:
- Have inline CSS (no external deps)
- Use system font stack
- Be responsive
- Look professional but not over-designed

Focus on:
- What does this data actually show?
- What can we confidently claim?
- What are the limitations?
- What would need further investigation?
"""

    accumulated_text = ""

    async with ClaudeSDKClient(options=options) as client:
        await client.query(analysis_prompt)

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        accumulated_text += block.text
            elif isinstance(message, ResultMessage):
                print(f"Analysis complete. Tokens: {message.usage}")

    # Read the generated files
    md_path = workspace / "results-analysis.md"
    html_path = workspace / "results-analysis.html"

    md_content = md_path.read_text() if md_path.exists() else ""
    html_content = html_path.read_text() if html_path.exists() else ""

    return md_content, html_content


async def main():
    import argparse
    parser = argparse.ArgumentParser(description="Analyze HumanEval results")
    parser.add_argument("results_file", help="Path to results JSON file")
    args = parser.parse_args()

    print(f"Analyzing {args.results_file}...")
    md_content, html_content = await run_analyst(args.results_file)

    if md_content:
        print(f"\n✓ Markdown report written")
    if html_content:
        print(f"✓ HTML report written")


if __name__ == "__main__":
    asyncio.run(main())
