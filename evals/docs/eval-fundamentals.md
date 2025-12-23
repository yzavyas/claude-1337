# Eval Fundamentals

Your skill activates 84% of the time. Is that good?

You don't know. And that's the problem.

---

## The Trap: Vanity Metrics

```python
# A skill that activates on EVERY prompt
if any_prompt:
    activate()  # 100% activation rate!
```

100% activation. Completely useless.

**Activation rate alone tells you nothing.** You need to know:
- When it activates, is it actually relevant?
- When it should activate, does it?

---

## The Two Questions

| Metric | Question | Failure Mode |
|--------|----------|--------------|
| **Precision** | When it fires, is it right? | Noise (false alarms) |
| **Recall** | When it should fire, does it? | Misses (silent failures) |

Both matter. Optimizing one destroys the other.

---

## The Extremes Don't Work

| Strategy | Precision | Recall | Problem |
|----------|-----------|--------|---------|
| Never activate | 100% | 0% | Useless |
| Always activate | ~10% | 100% | All noise |
| **Balanced** | 85% | 80% | **This is the goal** |

---

## F1: The Balancing Metric

F1 is the harmonic mean of precision and recall:

```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

Why harmonic mean? It punishes imbalance.

| Precision | Recall | Regular Avg | F1 |
|-----------|--------|-------------|-----|
| 100% | 0% | 50% | **0%** |
| 100% | 50% | 75% | **67%** |
| 80% | 80% | 80% | **80%** |

You can't game F1 by going extreme.

---

## The Confusion Matrix

Every test result lands in one box:

```
                      ACTUALLY ACTIVATED
                        Yes         No
                    +-----------+-----------+
SHOULD        Yes   |    TP     |    FN     |
ACTIVATE            |  Correct  |  Missed   |
                    +-----------+-----------+
              No    |    FP     |    TN     |
                    |   Noise   |  Correct  |
                    +-----------+-----------+
```

- **TP** (True Positive): Should activate, did. Good.
- **TN** (True Negative): Shouldn't activate, didn't. Good.
- **FP** (False Positive): Shouldn't activate, but did. Noise.
- **FN** (False Negative): Should activate, but didn't. Missed.

Then:
```
Precision = TP / (TP + FP)    "Of my activations, how many were right?"
Recall    = TP / (TP + FN)    "Of the cases I should catch, how many did I?"
```

---

## Where This Framework Comes From

F1 isn't new. It's battle-tested across domains:

| Domain | Precision = | Recall = |
|--------|-------------|----------|
| Search engines | Relevant results / shown results | Relevant found / all relevant |
| Spam filters | Actual spam / flagged as spam | Spam caught / all spam |
| Medical tests | True disease / positive tests | Detected / all cases |
| Fraud detection | Actual fraud / flagged fraud | Fraud caught / all fraud |
| **Skill activation** | Relevant / activated | Caught / should activate |

Same math. Different domain.

---

## Why LLMs Need This

LLMs are:

| Property | Implication |
|----------|-------------|
| **Stochastic** | Same input, different outputs. One test means nothing. |
| **Binary decisions** | "Use skill or not" is classification. |
| **Asymmetric costs** | Missing knowledge ≠ false activation. |

This is why we run 5+ tests per prompt. Probabilistic systems need statistical rigor.

---

## What to Benchmark

| Target | What You Measure | Why It Matters |
|--------|------------------|----------------|
| **Skills** | Activation precision/recall | Right knowledge at right time? |
| **Agents** | Task completion rate | Does it solve the problem? |
| **MCP Servers** | Tool call success rate | Reliable integration? |
| **Prompts** | Response quality (LLM-as-judge) | Good outputs? |
| **Code Gen** | Lint pass, test pass | Correct code? |

Each has different metrics, but the same principle: **measure both false positives and false negatives**.

---

## The Ground Truth Requirement

Good evals need labeled expectations:

```json
{
  "prompt": "What crate for CLI args in Rust?",
  "expectation": "must_activate",
  "rationale": "Direct Rust tooling question"
}
```

```json
{
  "prompt": "Write me a haiku",
  "expectation": "should_not_activate",
  "rationale": "Creative task, no skill needed"
}
```

Without labels, you can't compute precision or recall. You're just guessing.

---

## The Three Expectation Types

| Label | Meaning | Used For |
|-------|---------|----------|
| `must_activate` | Should definitely fire | Clear matches (measures recall) |
| `should_not_activate` | Must not fire | Off-topic (measures precision) |
| `acceptable` | Either is fine | Edge cases (excluded from metrics) |

---

## The Eval Workflow

```
1. HYPOTHESIS
   "This skill triggers on Rust CLI questions"
        ↓
2. TEST CASES
   Write prompts with labeled expectations
        ↓
3. RUN
   Execute 5+ times per case (stochastic!)
        ↓
4. MEASURE
   Compute precision, recall, F1
        ↓
5. ITERATE
   Fix description, re-run, compare
        ↓
6. SHIP
   Only when F1 meets threshold
```

This is TDD for agent behavior. Same loop: red → green → refactor.

---

## Red Flags in Results

| Pattern | Problem | Fix |
|---------|---------|-----|
| High recall, low precision | Over-activating (noise) | Tighten description |
| Low recall, high precision | Under-activating (misses) | Broaden triggers |
| High variance across runs | Unstable behavior | More runs, check prompt |
| Great with "forced", bad without | Artificial inflation | Use "smart" mode |

---

## The 1337 Standard

| Principle | Implementation |
|-----------|----------------|
| Evidence over opinion | Metrics, not vibes |
| Ground truth | Labeled expectations |
| Statistical rigor | 5+ runs per case |
| Balanced metrics | F1, not just recall |
| Reproducibility | Same suite, comparable results |

---

## Quick Reference

**Precision** = When it fires, is it right?
```
TP / (TP + FP)
```

**Recall** = When it should fire, does it?
```
TP / (TP + FN)
```

**F1** = Balanced score
```
2 × (P × R) / (P + R)
```

**Good F1**: 0.8+
**Acceptable F1**: 0.6-0.8
**Needs work**: < 0.6

---

## Further Reading

- [why-evals-matter.md](why-evals-matter.md) - Philosophy, TDD parallel
- [reference.md](reference.md) - CLI commands, schemas, modes

---

*"If you can't measure it, you can't improve it."* — Peter Drucker
