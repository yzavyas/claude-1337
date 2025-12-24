# Skill Activation Evaluation

Measuring whether skills trigger on the right prompts.

## Why Classification Metrics

Skills have TWO failure modes:
- **False Positive**: Triggers when it shouldn't (noise)
- **False Negative**: Doesn't trigger when it should (miss)

Raw "activation rate" is meaningless. Need precision AND recall.

## The Confusion Matrix

```
                      ACTUALLY TRIGGERED
                        Yes         No
                    +-----------+-----------+
SHOULD        Yes   |    TP     |    FN     |
TRIGGER             |  Correct  |  Missed   |
                    +-----------+-----------+
              No    |    FP     |    TN     |
                    |   Noise   |  Correct  |
                    +-----------+-----------+
```

## Metrics

```
Precision = TP / (TP + FP)
  "When skill activates, is it relevant?"

Recall = TP / (TP + FN)
  "When skill should activate, does it?"

F1 = 2 × (P × R) / (P + R)
  "Balanced score - punishes extremes"
```

## Labeled Test Cases

```json
{
  "skills": [
    {
      "name": "rust-1337",
      "test_cases": [
        {
          "prompt": "What crate for CLI args in Rust?",
          "expectation": "must_activate",
          "rationale": "Direct Rust tooling question"
        },
        {
          "prompt": "Help me write a Python script",
          "expectation": "should_not_activate",
          "rationale": "Python task, not Rust"
        },
        {
          "prompt": "Explain Rust ownership",
          "expectation": "acceptable",
          "rationale": "Core concept, skill is about tooling"
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

## Expectation Labels

| Label | Meaning | Contribution |
|-------|---------|--------------|
| must_activate | Should definitely fire | TP or FN |
| should_not_activate | Must not fire | TN or FP |
| acceptable | Either is fine | Excluded from metrics |

## Testing Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| baseline | No system prompt | True baseline |
| smart | Per-topic evaluation | Production |
| forced | Every-message evaluation | Testing only |

**Warning:** Forced mode inflates recall but may hurt precision.

## Ground Truth Testing

Observe actual `Skill()` tool calls:

```python
async for message in query(prompt=prompt):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                if block.name == "Skill":
                    skill_called = True  # Ground truth
```

Don't ask Claude "would you use this skill?" - observe behavior.

## Interpreting Results

| Pattern | Problem | Fix |
|---------|---------|-----|
| High recall, low precision | Over-activating | Tighten description |
| Low recall, high precision | Under-activating | Broaden triggers |
| Great forced, bad baseline | Artificial | Use smart mode |

## Thresholds

| F1 | Interpretation |
|----|----------------|
| 0.85+ | Excellent |
| 0.70-0.85 | Good |
| 0.50-0.70 | Needs work |
| < 0.50 | Poor |
