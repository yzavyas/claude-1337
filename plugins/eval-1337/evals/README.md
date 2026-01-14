# Evaluating and Tuning eval-1337

This directory contains evals for the eval-1337 skill itself.

## Two-Level Evaluation

### Level 1: Activation (F1)

**Question:** Does the skill trigger on the right prompts?

```bash
python run_eval.py activation
```

**Metrics:**
- **Precision**: When it activates, is it relevant?
- **Recall**: When it should activate, does it?
- **F1**: Balanced score

**Test Cases:** `activation-suite.json`
- `must_trigger`: Eval-related questions (should activate)
- `should_not_trigger`: Non-eval questions (should not activate)
- `acceptable`: Ambiguous (excluded from F1)

### Level 2: Methodology (Rubric)

**Question:** When activated, does Claude follow the methodology?

```bash
python run_eval.py methodology
```

**Criteria:**
| Criterion | Weight | What It Measures |
|-----------|--------|------------------|
| metric_selection | 25% | Recommends appropriate metrics? |
| failure_modes | 20% | Addresses both failure modes? |
| non_determinism | 15% | Accounts for stochasticity? |
| framework_guidance | 15% | Actionable framework recommendations? |
| pitfall_awareness | 15% | Warns about common traps? |
| actionability | 10% | Provides code/concrete steps? |

**Test Cases:** `methodology-rubric.json`

## Running Evals

```bash
# Prerequisites
pip install anthropic

# Run specific eval
python run_eval.py activation
python run_eval.py methodology

# Run all
python run_eval.py all
```

## Interpreting Results

### Activation Results

```
Precision: 85%    # When it fires, it's right 85% of time
Recall:    90%    # It catches 90% of eval questions
F1:        87%    # Balanced score

Status: GOOD
```

| F1 Score | Interpretation |
|----------|----------------|
| 85%+ | Excellent - no action needed |
| 70-85% | Good - minor tuning |
| 50-70% | Needs work - review triggers |
| <50% | Poor - significant changes needed |

### Methodology Results

```
Average Score: 78%
Pass Rate:     75%

Criterion Averages (0-3 scale):
  metric_selection: 2.5 [OK]
  failure_modes: 1.8 [WEAK]    <- Needs attention
  non_determinism: 2.2 [OK]
```

## Tuning Guide

### Low Recall (Under-activation)

**Symptom:** Skill doesn't trigger on valid eval questions.

**Fix:** Broaden the skill description.

```yaml
# Before
description: "Write evals for LLM agents"

# After
description: "Write evals for LLM agents, multi-agent systems, skills, MCP servers. Use when: building test suites, measuring effectiveness, evaluating tools, choosing eval frameworks."
```

**Add keywords:**
- eval, evaluation, evals
- test suite, testing
- metrics, measure, measurement
- precision, recall, F1
- pass@k, accuracy
- benchmark

### Low Precision (Over-activation)

**Symptom:** Skill triggers on non-eval questions.

**Fix:** Tighten the description with specificity.

```yaml
# Before
description: "Help with testing and metrics"

# After
description: "Write evals for LLM agents and AI systems. NOT for: unit tests, integration tests, performance benchmarks, business metrics."
```

**Add exclusions:**
- Distinguish from unit/integration testing
- Distinguish from runtime performance
- Distinguish from business analytics

### Weak Methodology Criteria

| Weak Criterion | Tuning Action |
|----------------|---------------|
| metric_selection | Add more rows to "Match Metric to Target" table |
| failure_modes | Emphasize precision/recall duality in core sections |
| non_determinism | Make pass@k guidance more prominent |
| framework_guidance | Expand framework decision matrix |
| pitfall_awareness | Add more entries to "Common Pitfalls" table |
| actionability | Add more code examples to references |

### Example: Fixing Weak failure_modes

If `failure_modes` scores low, the skill isn't emphasizing dual failure modes enough.

**Action:** Strengthen the "Core Problem" section in SKILL.md:

```markdown
## The Core Problem

Single metrics lie. You need BOTH:
- **Precision** (false positive rate) - noise when it fires wrong
- **Recall** (false negative rate) - misses when it should fire

Example: 100% recall + 50% precision = triggers on everything (useless)
```

## Continuous Improvement

### 1. Run Evals After Changes

```bash
# Before PR
python run_eval.py all > before.txt

# Make changes to SKILL.md or references

# After changes
python run_eval.py all > after.txt

# Compare
diff before.txt after.txt
```

### 2. Add Failing Cases

When you find prompts that should/shouldn't trigger:

```json
// Add to activation-suite.json
{
  "id": "must-016",
  "prompt": "New prompt that should trigger",
  "expectation": "must_trigger",
  "rationale": "Why this should trigger"
}
```

### 3. Track Metrics Over Time

| Date | Precision | Recall | F1 | Methodology |
|------|-----------|--------|-----|-------------|
| 2026-01-14 | 85% | 90% | 87% | 78% |
| ... | ... | ... | ... | ... |

### 4. Version Test Suites

```
evals/
├── activation-suite.json      # Current
├── activation-suite-v1.json   # Previous version
├── methodology-rubric.json
└── CHANGELOG.md
```

## Adding New Test Cases

### For Activation

```json
{
  "id": "must-XXX",
  "prompt": "Your test prompt here",
  "expectation": "must_trigger | should_not_trigger | acceptable",
  "rationale": "Why this expectation"
}
```

**Guidelines:**
- Include diverse phrasings
- Cover edge cases
- Balance positive/negative (aim for 50/50)
- Document rationale for borderline cases

### For Methodology

```json
{
  "id": "method-XXX",
  "prompt": "Complex eval question",
  "expected_criteria": {
    "metric_selection": ["expected metrics to mention"],
    "failure_modes": ["expected failure modes"],
    ...
  },
  "min_score": 0.70
}
```

## Troubleshooting

### "No anthropic module"

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your-key
```

### Inconsistent Results

LLMs are stochastic. The harness runs multiple trials and takes majority vote. If results vary wildly:

1. Increase `n_trials` in `run_eval.py`
2. Check if test cases are ambiguous
3. Review the activation heuristics in `check_skill_activation()`

### False Positives in Activation

The `check_skill_activation()` function uses keyword heuristics. If it's detecting activation incorrectly:

1. Review the `indicators` list
2. Adjust the threshold (default: 3 matches)
3. Consider more sophisticated detection (e.g., LLM-as-judge)
