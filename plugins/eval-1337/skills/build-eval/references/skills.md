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

## OTel Instrumentation

Trace skill activation for debugging (see [otel.md](otel.md)):

```python
with tracer.start_as_current_span("skill_check") as span:
    span.set_attribute("prompt", prompt[:200])
    span.set_attribute("available_skills", len(skills))

    for skill in skills:
        with tracer.start_as_current_span("skill_match") as skill_span:
            skill_span.set_attribute("skill_name", skill.name)
            matches = skill.matches(prompt)
            skill_span.set_attribute("activated", matches)
```

## Sources

- [Scott Spence](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably) - 84% recall study, testing methodology
- [Skills Tokenomics](https://www.reddit.com/r/ClaudeAI/comments/1pha74t/deep_dive_anatomy_of_a_skill_its_tokenomics_why/) - Budget limits, truncation behavior
- [CLAUDE.md Experiment](https://www.reddit.com/r/ClaudeAI/comments/1pe37e3/claudemd_and_skills_experiment_whats_the_best_way/) - Hybrid approach validation
- [Claude Code Skills Docs](https://code.claude.com/docs/en/skills) - Official specification
