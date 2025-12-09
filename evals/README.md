# claude-1337-evals

Skill activation testing for the claude-1337 marketplace using the Claude Agent SDK.

## Why This Exists

Skills only activate ~20% of the time by default. This tool measures **actual** activation - not asking Claude's opinion, but observing whether it invokes the `Skill()` tool.

## Key Insights

### Skill Activation Research

From [Scott Spence's 200+ test study](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably):

| Approach | Success Rate |
|----------|--------------|
| No intervention (baseline) | ~20% |
| Simple instruction | ~20% |
| LLM eval hook | 80% |
| Forced eval hook | **84%** |

### How Skills Actually Work

From [Lee Han Chung's deep dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/):

- **No algorithmic routing** - no regex, no embeddings, no classifiers
- **Pure LLM reasoning** - Claude reads skill descriptions and decides
- **Description is everything** - it's the only signal for matching

### What Makes Skills Activate

| Pattern | Why |
|---------|-----|
| "Use when:" clause | Explicit trigger conditions |
| Specific tools/terms | "axum, tonic, sqlx" not "backend" |
| Action verbs | "building", "debugging", "configuring" |
| Front-loaded keywords | Claude matches against description |

## Installation

```bash
cd evals
uv sync
```

## Usage

### Single Test

```bash
uv run skill-test test "How do I search for a pattern in my codebase?" -s terminal-1337 -n 3
```

### Run Test Suite

```bash
# Create sample suite
uv run skill-test init-suite sample-suite.json

# Run suite
uv run skill-test suite sample-suite.json -o report.md
```

## How It Works

1. Sends prompts through Claude Agent SDK
2. Monitors response stream for `ToolUseBlock` with `name == "Skill"`
3. Records whether skill was actually invoked (ground truth)
4. Generates markdown reports suitable for PRs

## Test Suite Format

```json
{
  "name": "claude-1337-skills",
  "description": "Test activation of marketplace skills",
  "skills": [
    {
      "name": "terminal-1337",
      "plugin": "terminal-1337",
      "expected_triggers": [
        "How do I search for a pattern in my codebase?",
        "What's a fast way to find files by name?"
      ]
    }
  ],
  "runs_per_prompt": 3
}
```

## Methodology

This is **not** a proxy test. We don't ask Claude "would you use this skill?" - we observe actual tool invocation:

```python
async for message in query(prompt=prompt, options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                if block.name == "Skill":
                    skill_called = True  # Ground truth
```

## Interpreting Results

| Rate | Meaning |
|------|---------|
| 80%+ | Skill description is working well |
| 50-79% | Description needs improvement |
| <50% | Description likely missing "Use when:" or too vague |

## Sources

- [Anthropic: Equipping agents with skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Scott Spence: Skills activation study](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably)
- [Lee Han Chung: Skills deep dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
