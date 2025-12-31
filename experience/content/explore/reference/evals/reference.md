# eval framework reference

technical specification for the claude-1337-evals framework.

---

## metrics

### precision

**definition**: when the skill activates, how often is it correct?

```
Precision = True Positives / (True Positives + False Positives)
```

| value | interpretation |
|-------|----------------|
| 1.0 | perfect - never activates incorrectly |
| 0.8+ | good - few false activations |
| 0.5-0.8 | needs work - noisy |
| <0.5 | poor - mostly noise |

### recall

**definition**: when the skill should activate, how often does it?

```
Recall = True Positives / (True Positives + False Negatives)
```

| value | interpretation |
|-------|----------------|
| 1.0 | perfect - catches all valid triggers |
| 0.8+ | good - misses few |
| 0.5-0.8 | needs work - missing triggers |
| <0.5 | poor - misses most |

### F1 score

**definition**: harmonic mean of precision and recall.

```
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

| value | interpretation |
|-------|----------------|
| 0.9+ | excellent |
| 0.8-0.9 | good |
| 0.6-0.8 | acceptable |
| <0.6 | needs improvement |

### accuracy

**definition**: overall correctness.

```
Accuracy = (True Positives + True Negatives) / Total
```

less useful than F1 for imbalanced datasets.

---

## expectation labels

### `must_activate`

the skill **must** activate for this prompt. failure to activate is a false negative.

**use for**: direct matches, explicit tool mentions, clear domain questions.

```json
{
  "prompt": "What crate should I use for CLI arguments in Rust?",
  "expectation": "must_activate",
  "rationale": "Direct Rust tooling question, clap is the answer"
}
```

### `should_not_activate`

the skill **must not** activate for this prompt. activation is a false positive.

**use for**: off-topic prompts, different domains, general questions.

```json
{
  "prompt": "Help me write a Python web scraper",
  "expectation": "should_not_activate",
  "rationale": "Python, not Rust"
}
```

### `acceptable`

either outcome is reasonable. excluded from precision/recall calculation.

**use for**: ambiguous cases, edge cases, borderline prompts.

```json
{
  "prompt": "Explain Rust ownership and borrowing",
  "expectation": "acceptable",
  "rationale": "Core Rust concept, but skill is about tooling not teaching"
}
```

---

## outcome classifications

| outcome | meaning | contribution |
|---------|---------|--------------|
| `tp` | true positive | +precision, +recall |
| `fp` | false positive | -precision |
| `tn` | true negative | +accuracy |
| `fn` | false negative | -recall |
| `acceptable` | ambiguous | excluded |
| `error` | test failed | excluded |

---

## modes

### `baseline`

no system prompt. true baseline behavior.

**use for**: measuring natural activation without intervention.

### `smart`

per-topic evaluation prompt:

```
When you receive a request that might benefit from specialized knowledge:
1. Check if you've already activated a relevant skill this session
2. If not, scan <available_skills> for matches and activate before responding
3. Skip re-evaluation for topics you've already covered
```

**use for**: production recommendation. balances activation with efficiency.

### `forced`

every-message evaluation prompt:

```
Before responding to any user request, you MUST:
1. EVALUATE each skill in <available_skills>
2. ACTIVATE relevant skills
3. Only THEN respond
```

**use for**: testing only. artificially inflates recall, may hurt precision.

---

## test suite schema

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

## CLI commands

### `test`

run a single prompt test.

```bash
skill-test test "prompt" \
  --skill SKILL_NAME \
  --expect must|should_not|acceptable \
  --mode baseline|smart|forced \
  --runs N
```

### `suite`

run a complete test suite.

```bash
skill-test suite SUITE_FILE \
  --mode baseline|smart|forced \
  --output REPORT.md \
  --json-output RESULTS.json
```

### `compare`

compare multiple modes.

```bash
skill-test compare SUITE_FILE \
  --modes baseline smart forced \
  --output COMPARISON.md
```

### `init-suite`

generate sample test suite.

```bash
skill-test init-suite OUTPUT.json
```

---

## report sections

### overall metrics

precision, recall, F1, accuracy for entire suite.

### confusion matrix

visual TP/FP/TN/FN breakdown.

### per-skill breakdown

metrics for each skill individually.

### detailed results

- false negatives (missed activations) - most actionable
- false positives (incorrect activations) - noise
- errors (test failures)
- success summary

### methodology

explains how tests were run.

---

## environment variables

| variable | default | description |
|----------|---------|-------------|
| `CLAUDE_1337_PLUGINS` | `../plugins` | path to plugins directory |

---

## exit codes

| code | meaning |
|------|---------|
| 0 | success |
| 1 | error |

---

## dependencies

| package | purpose |
|---------|---------|
| `claude-agent-sdk` | claude code integration |
| `pydantic` | data models, validation |
| `click` | CLI framework |
| `rich` | terminal output |
