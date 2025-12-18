# Eval Framework Reference

Technical specification for the claude-1337-evals framework.

---

## Metrics

### Precision

**Definition**: When the skill activates, how often is it correct?

```
Precision = True Positives / (True Positives + False Positives)
```

| Value | Interpretation |
|-------|----------------|
| 1.0 | Perfect - never activates incorrectly |
| 0.8+ | Good - few false activations |
| 0.5-0.8 | Needs work - noisy |
| <0.5 | Poor - mostly noise |

### Recall

**Definition**: When the skill should activate, how often does it?

```
Recall = True Positives / (True Positives + False Negatives)
```

| Value | Interpretation |
|-------|----------------|
| 1.0 | Perfect - catches all valid triggers |
| 0.8+ | Good - misses few |
| 0.5-0.8 | Needs work - missing triggers |
| <0.5 | Poor - misses most |

### F1 Score

**Definition**: Harmonic mean of precision and recall.

```
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

| Value | Interpretation |
|-------|----------------|
| 0.9+ | Excellent |
| 0.8-0.9 | Good |
| 0.6-0.8 | Acceptable |
| <0.6 | Needs improvement |

### Accuracy

**Definition**: Overall correctness.

```
Accuracy = (True Positives + True Negatives) / Total
```

Less useful than F1 for imbalanced datasets.

---

## Expectation Labels

### `must_activate`

The skill **must** activate for this prompt. Failure to activate is a False Negative.

**Use for**: Direct matches, explicit tool mentions, clear domain questions.

```json
{
  "prompt": "What crate should I use for CLI arguments in Rust?",
  "expectation": "must_activate",
  "rationale": "Direct Rust tooling question, clap is the answer"
}
```

### `should_not_activate`

The skill **must not** activate for this prompt. Activation is a False Positive.

**Use for**: Off-topic prompts, different domains, general questions.

```json
{
  "prompt": "Help me write a Python web scraper",
  "expectation": "should_not_activate",
  "rationale": "Python, not Rust"
}
```

### `acceptable`

Either outcome is reasonable. Excluded from precision/recall calculation.

**Use for**: Ambiguous cases, edge cases, borderline prompts.

```json
{
  "prompt": "Explain Rust ownership and borrowing",
  "expectation": "acceptable",
  "rationale": "Core Rust concept, but skill is about tooling not teaching"
}
```

---

## Outcome Classifications

| Outcome | Meaning | Contribution |
|---------|---------|--------------|
| `tp` | True Positive | +Precision, +Recall |
| `fp` | False Positive | -Precision |
| `tn` | True Negative | +Accuracy |
| `fn` | False Negative | -Recall |
| `acceptable` | Ambiguous | Excluded |
| `error` | Test failed | Excluded |

---

## Modes

### `baseline`

No system prompt. True baseline behavior.

**Use for**: Measuring natural activation without intervention.

### `smart`

Per-topic evaluation prompt:

```
When you receive a request that might benefit from specialized knowledge:
1. Check if you've already activated a relevant skill this session
2. If not, scan <available_skills> for matches and activate before responding
3. Skip re-evaluation for topics you've already covered
```

**Use for**: Production recommendation. Balances activation with efficiency.

### `forced`

Every-message evaluation prompt:

```
Before responding to any user request, you MUST:
1. EVALUATE each skill in <available_skills>
2. ACTIVATE relevant skills
3. Only THEN respond
```

**Use for**: Testing only. Artificially inflates recall, may hurt precision.

---

## Test Suite Schema

```json
{
  "name": "string (required)",
  "description": "string (optional)",
  "runs_per_case": "integer 1-20 (default: 5)",
  "skills": [
    {
      "name": "string (required) - skill name in available_skills",
      "plugin": "string (required) - plugin containing the skill",
      "test_cases": [
        {
          "prompt": "string (required)",
          "expectation": "must_activate | should_not_activate | acceptable",
          "rationale": "string (optional) - why this expectation"
        }
      ]
    }
  ],
  "negative_cases": [
    {
      "prompt": "string (required)",
      "expectation": "should_not_activate",
      "rationale": "string (optional)"
    }
  ]
}
```

---

## CLI Commands

### `test`

Run a single prompt test.

```bash
skill-test test "prompt" \
  --skill SKILL_NAME \
  --expect must|should_not|acceptable \
  --mode baseline|smart|forced \
  --runs N
```

### `suite`

Run a complete test suite.

```bash
skill-test suite SUITE_FILE \
  --mode baseline|smart|forced \
  --output REPORT.md \
  --json-output RESULTS.json
```

### `compare`

Compare multiple modes.

```bash
skill-test compare SUITE_FILE \
  --modes baseline smart forced \
  --output COMPARISON.md
```

### `init-suite`

Generate sample test suite.

```bash
skill-test init-suite OUTPUT.json
```

---

## Report Sections

### Overall Metrics

Precision, recall, F1, accuracy for entire suite.

### Confusion Matrix

Visual TP/FP/TN/FN breakdown.

### Per-Skill Breakdown

Metrics for each skill individually.

### Detailed Results

- False Negatives (missed activations) - most actionable
- False Positives (incorrect activations) - noise
- Errors (test failures)
- Success summary

### Methodology

Explains how tests were run.

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAUDE_1337_PLUGINS` | `../plugins` | Path to plugins directory |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error |

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `claude-agent-sdk` | Claude Code integration |
| `pydantic` | Data models, validation |
| `click` | CLI framework |
| `rich` | Terminal output |
