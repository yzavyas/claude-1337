# REP-002 v2 Pilot Analysis

**Date**: 2026-01-20
**Batch**: rep-002-v2-pilot
**Task**: safe-calculator (discriminating, function grader)
**Runs**: 6 total (2 per condition × 3 conditions)

---

## Summary Results

| Condition | n | Avg Quality | Avg Judgment | Avg Weighted | Attempts |
|-----------|---|-------------|--------------|--------------|----------|
| mandate-template | 2 | 0.967 | 2.5 | 0.939 | 15, 14 |
| baseline | 2 | 0.933 | 2.5 | 0.924 | 15, 13 |
| motivation | 2 | 0.833 | 2.0 | 0.818 | 13, 12 |

**Note**: Higher is better. Total scores out of 15.

---

## Key Observations

### 1. Results Counter to Hypothesis

The hypothesis stated: *"Motivation-based prompting produces better judgment than mandate-based prompting on ambiguous tasks."*

The pilot data shows the **opposite**:
- Mandate-template performed best (0.967 quality)
- Baseline performed second (0.933 quality)
- Motivation performed worst (0.833 quality)

### 2. The Key Discriminator Worked

`judgment_under_ambiguity` was designed as the key metric. It did discriminate:
- Motivation: avg 2.0 (never hit 3)
- Others: avg 2.5 (both hit 3 once)

This suggests the rubric and task CAN distinguish prompting approaches.

### 3. Qualitative Patterns in Rationales

**Motivation condition issues**:
- "incomplete implementation (truncated validation function)"
- "critical bug in negative number handling"
- "questionable design decisions (like rejecting unary plus)"

**Mandate/baseline patterns**:
- "production-quality code with comprehensive testing"
- "comprehensive error handling, proper edge case coverage"
- Only minor issues: "implicit assumptions about edge cases"

---

## Interpretation

### Why Might Motivation Underperform?

1. **Cognitive load**: The "WHY" framing may add mental overhead without aiding implementation
2. **Task mismatch**: safe-calculator is technically clear; motivation shines on genuinely ambiguous tasks
3. **Prompt design**: The motivation prompt may need refinement
4. **Statistical noise**: n=2 is meaningless for conclusions

### What the Mandate Prompt Provides

Looking at `mandate-template.md`:
- Explicit artifacts to create (spec, test plan, implementation)
- Checkpoint structure
- Clear verification steps

This scaffolding may help Claude produce more complete implementations.

---

## Limitations

### Sample Size
**n=2 per condition is insufficient.** With this variance:
- Baseline: [15, 13] = 13.3% variance
- Motivation: [13, 12] = 4.0% variance
- Mandate: [15, 14] = 3.4% variance

Need **n≥20** for statistical confidence (power analysis suggests n=50 for small effects).

### Task Ambiguity
The safe-calculator task has clear success criteria (tests pass). True ambiguity testing needs tasks where "correct" is debatable.

### Single Task
We tested ONE task. Task-condition interactions likely exist.

---

## Recommendations for Full Run

### 1. Increase Sample Size
- **Minimum**: 20 runs per condition
- **Recommended**: 50 runs per condition for small effect detection

### 2. Add More Tasks
- Include genuinely ambiguous tasks (Level 2-3 ambiguity)
- Task stratification: clear vs. ambiguous

### 3. Refine Conditions
Consider whether:
- Motivation prompt needs strengthening
- Mandate prompt provides unfair structure advantage
- Baseline is actually well-calibrated

### 4. Monitor Judge Consistency
Run the same solution through the judge multiple times to measure scoring variance.

---

## Next Steps

1. [ ] Review motivation prompt - is it too vague?
2. [ ] Design Level-3 ambiguous tasks (genuinely unclear requirements)
3. [ ] Run larger batch: 20+ runs per condition
4. [ ] Add inter-rater reliability check for judge

---

## Raw Data

Stored in: `rep-002-v2-pilot_judged.jsonl`

```
Condition     | Attempt | Total | Judgment | Pass |
--------------+---------+-------+----------+------+
baseline      | 1       | 15    | 3        | ✓    |
baseline      | 2       | 13    | 2        | ✓    |
motivation    | 1       | 13    | 2        | ✓    |
motivation    | 2       | 12    | 2        | ✓    |
mandate-temp. | 1       | 15    | 3        | ✓    |
mandate-temp. | 2       | 14    | 2        | ✓    |
```
