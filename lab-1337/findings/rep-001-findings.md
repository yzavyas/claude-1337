---
tags: [iteration, cost-benefit, humaneval]
---

# When Iteration Actually Helps

**REP-001 Findings** — Published 2026-01-16

---

## TL;DR

We ran 164 coding problems through Claude Haiku twice: once single-shot, once with self-review iteration.

**The punchline**: Iteration improved success from 87% to 99% at 10x the token cost.

**The insight**: Iteration is insurance, not optimization. It only helps the 13% of tasks at the edge of capability — recovering 91% of those failures. For the 87% that succeed anyway, it just burns tokens.

**The decision**: If failure costs more than 10x tokens, iterate. Otherwise, single-shot.

---

## What We Measured

**Benchmark**: HumanEval (164 Python coding problems)
**Model**: Claude 3.5 Haiku
**Strategies**: Single-shot vs Ralph-style self-review iteration

| Strategy | Pass Rate | Average Tokens |
|----------|-----------|----------------|
| Single-shot | 86.6% (142/164) | 232 |
| Ralph iteration | 98.8% (162/164) | 2,264 |

**Cost-benefit**: 12.2% improvement at ~10x token cost.

---

## The Core Pattern

```
Total problems:          164
Single-shot solved:      142 (87%)
Single-shot failed:       22 (13%)

Of those 22 failures:
  Iteration recovered:    20 (91%)
  Still failed:            2 (9%)
```

**What this means**:

- For ~87% of tasks, the model gets it right immediately. Iteration wastes tokens.
- For ~13% at capability edge, iteration recovers 91% of failures.
- 2 problems failed both strategies — that's the model's ceiling.

---

## Visualizing the Tradeoff

```
                    ITERATION VALUE

Pass Rate
 99% ─────────────────────────────●  Ralph (98.8%)
 96% ─
 93% ─
 90% ─
 87% ─●───────────────────────────  Single-shot (86.6%)
      └─────┬─────┬─────┬─────┬────
           2x    4x    6x    8x   10x
                Token Cost

    12.2% improvement at ~10x cost
```

The question: Is that 12% worth 10x cost for your use case?

---

## When to Use Each

### Single-shot (87% success)

Use when:
- Speed matters more than perfection
- Token budget is constrained
- Task is well within model capability
- Occasional failure is acceptable
- You're doing exploratory or draft work

**Example**: Generating documentation, refactoring suggestions, code explanations.

### Iteration (99% success)

Use when:
- Correctness is non-negotiable
- Task has known edge cases or complexity
- Cost of failure exceeds 10x token cost
- Critical path or production code
- Final/shipping deliverables

**Example**: Production bug fixes, security-sensitive code, customer-facing features.

---

## The Decision Framework

```python
if (cost_of_failure > 10x_token_cost):
    use_iteration()
else:
    use_single_shot()
```

Simple heuristic, backed by data.

---

## What Iteration Can't Fix

Two problems (HumanEval/80, HumanEval/130) failed both strategies.

This tells us:
- Iteration is **recovery**, not capability expansion
- There's a ceiling (98.8%, not 100%)
- Some problems require reasoning the model can't perform
- More iterations won't help beyond capability limits

**Practical implication**: If iteration fails, try a different model or approach. More iterations won't help.

---

## Why This Matters

Before this experiment, the discourse was:

> "Ralph-style iteration always improves results." — Testimonials, no data

We searched. **No controlled experiments exist** measuring Ralph effectiveness quantitatively.

Now we have data:
- Clear signal (12% improvement)
- Reproducible (pattern holds across subsets)
- Actionable (decision framework emerges)

**Evidence beats anecdotes.**

---

## Additional Context

### Subset Consistency

Earlier runs on problem subsets showed the same pattern:

| Subset | Single-shot | Ralph | Recovered |
|--------|-------------|-------|-----------|
| Easy (0-49) | 94.0% | 100% | +3 |
| Hard (50-79) | 93.3% | 100% | +2 |
| **Full (0-163)** | **86.6%** | **98.8%** | **+20** |

Larger samples expose more edge cases. The full dataset revealed the true distribution.

### What We Didn't Measure

Academic research (IEEE-ISTAS 2025) shows iteration may improve functional correctness while degrading **security** — a dimension we didn't evaluate.

**Future work**: Measure security vulnerabilities, code quality, optimal iteration count.

---

## Limitations

Be honest about scope:

- **Single model**: Haiku only (does pattern hold for Sonnet, Opus?)
- **Single benchmark**: HumanEval (coding tasks only)
- **Functional correctness**: Didn't measure security, maintainability, or quality
- **Single run**: No statistical variance analysis (deterministic execution)

These are experiments, not universal laws. Validate in your context.

---

## Future Research

Questions worth answering:

1. **Model comparison**: Does the 10x cost/12% improvement ratio hold for Sonnet and Opus?
2. **Security analysis**: Do iterated solutions introduce more vulnerabilities?
3. **Optimal iteration count**: Is there a point where quality degrades from over-iteration?
4. **Task type variation**: Does pattern hold for non-coding tasks (writing, analysis, planning)?

---

## Methodology Validated

This experiment proves the approach works:

1. **Measurable signal** — 12% difference, consistent across subsets
2. **Reproducible** — Pattern holds at multiple scales
3. **Actionable** — Clear decision framework emerges
4. **Honest about limits** — Identified ceiling (98.8%)

The scientific method applies to prompting strategies. We can test, measure, and decide based on evidence.

---

## Raw Data

Complete results available:

- [Full benchmark (164 problems)](../experiments/humaneval/results-haiku-full-164.json)
- [Easy subset (0-49)](../experiments/humaneval/results-haiku-50.json)
- [Hard subset (50-79)](../experiments/humaneval/results-haiku-hard-30.json)

All data is reproducible with the lab harness.

---

## The Bottom Line

**Iteration is insurance.**

It costs 10x tokens to recover 91% of the 13% of tasks at capability edge.

Do the math for your use case. Sometimes it's worth it. Sometimes it's not.

Now you have data to decide.
