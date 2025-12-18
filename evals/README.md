# claude-1337-evals

Rigorous skill activation testing for the claude-1337 marketplace using the Claude Agent SDK.

**Deep Dives**:
- [docs/WHY_EVALS_MATTER.md](docs/WHY_EVALS_MATTER.md) - philosophy, connection to TDD and scientific method
- [docs/REFERENCE.md](docs/REFERENCE.md) - metrics definitions, schemas, CLI reference

## Why Rigorous Evaluation Matters

**Raw activation rate is meaningless.** A system that activates skills on every prompt has 100% "activation rate" but is useless. Real evaluation requires:

- **Precision**: When a skill activates, is it actually relevant?
- **Recall**: When a skill should activate, does it?
- **F1 Score**: Balanced metric that penalizes both missed activations and false activations

## Key Concepts

```
                        ACTUAL ACTIVATION
                        Yes         No
                    +-----------+-----------+
SHOULD      Yes     |    TP     |    FN     |  <- Recall = TP/(TP+FN)
ACTIVATE            | (correct) | (missed)  |
                    +-----------+-----------+
            No      |    FP     |    TN     |
                    | (noise)   | (correct) |
                    +-----------+-----------+
                         ^
                    Precision = TP/(TP+FP)
```

## Installation

```bash
cd evals
uv sync
```

## Usage

### Single Test with Expectation

```bash
# Test that a skill SHOULD activate
uv run skill-test test "How do I use ripgrep?" -s terminal-1337 -e must -n 5

# Test that a skill should NOT activate
uv run skill-test test "Write a haiku" -s terminal-1337 -e should_not -n 5

# Compare modes
uv run skill-test test "Find TODO comments" -s terminal-1337 -m baseline
uv run skill-test test "Find TODO comments" -s terminal-1337 -m forced
```

### Run Rigorous Test Suite

```bash
# Create sample suite
uv run skill-test init-suite sample-suite.json

# Run suite with baseline (no system prompt)
uv run skill-test suite suites/rigorous-v1.json -m baseline -o baseline-report.md

# Run suite with forced eval
uv run skill-test suite suites/rigorous-v1.json -m forced -o forced-report.md

# Compare all modes
uv run skill-test compare suites/rigorous-v1.json -o comparison-report.md
```

## Test Suite Format

Test suites use labeled expectations for rigorous evaluation:

```json
{
  "name": "rigorous-v1",
  "description": "Rigorous skill activation eval",
  "runs_per_case": 5,
  "skills": [
    {
      "name": "terminal-1337",
      "plugin": "terminal-1337",
      "test_cases": [
        {
          "prompt": "How do I use ripgrep to search?",
          "expectation": "must_activate",
          "rationale": "Direct mention of ripgrep"
        },
        {
          "prompt": "Help me write a Python script",
          "expectation": "should_not_activate",
          "rationale": "Python task, not CLI tools"
        },
        {
          "prompt": "How do I grep for a pattern?",
          "expectation": "acceptable",
          "rationale": "Could use built-in grep or suggest rg"
        }
      ]
    }
  ],
  "negative_cases": [
    {
      "prompt": "Write me a haiku",
      "expectation": "should_not_activate",
      "rationale": "Creative task, no skill should activate"
    }
  ]
}
```

### Expectation Labels

| Label | Meaning | Used For |
|-------|---------|----------|
| `must_activate` | Skill should definitely activate | Clear matches (TP/FN) |
| `should_not_activate` | Skill should NOT activate | Off-topic prompts (TN/FP) |
| `acceptable` | Either outcome is reasonable | Ambiguous cases (excluded from metrics) |

## Modes

| Mode | System Prompt | Use Case |
|------|---------------|----------|
| `baseline` | None | True baseline, no intervention |
| `smart` | Per-topic evaluation | Production recommendation |
| `forced` | Every-message evaluation | Testing, not recommended for production |

## Interpreting Results

### Good Results

```
Precision: 90%   (few false activations)
Recall: 80%      (catches most valid triggers)
F1: 85%          (balanced)
```

### Red Flags

| Pattern | Problem |
|---------|---------|
| High recall, low precision | Over-activating (noise) |
| Low recall, high precision | Under-activating (misses) |
| High F1 with "forced" only | Dependent on artificial prompting |

## Methodology

This is **ground truth** testing. We observe actual `Skill()` tool calls:

```python
async for message in query(prompt=prompt, options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                if block.name == "Skill":
                    skill_called = True  # Ground truth
```

We do NOT ask Claude "would you use this skill?" - we observe behavior.

## Previous Methodology (Deprecated)

The old eval framework only measured activation rate without ground truth labels:

```json
{
  "expected_triggers": ["How do I use ripgrep?"]
}
```

This was flawed because:
1. All test cases assumed activation was correct
2. No measurement of false positives
3. Cherry-picked prompts inflated results

## Research Sources

- [Scott Spence: Skills activation study](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably) - 200+ test study showing 84% with forced eval
- [Lee Han Chung: Skills deep dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) - How skills work internally
- [Anthropic: Equipping agents with skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
