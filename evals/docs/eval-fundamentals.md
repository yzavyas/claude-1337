# Eval Fundamentals

Your agent solved 72% of tasks. Is that good?

You don't know. And that's the problem.

---

## The Problem: LLMs Are Probabilistic

LLMs and their extension mechanisms (skills, agents, MCP servers, tools) are:

| Property | Implication |
|----------|-------------|
| **Stochastic** | Same input, different outputs. One test means nothing. |
| **Multi-layered** | Model + harness + tools = many failure points. |
| **Binary decisions** | "Use this tool or not" is classification. |

Without rigorous measurement, you're guessing.

---

## The Trap: Vanity Metrics

```python
# An agent that claims success on EVERY task
def evaluate(task):
    return "completed"  # 100% completion rate!
```

100% completion. Completely meaningless.

**Single metrics tell you nothing.** You need to ask:
- When it claims success, is it actually correct?
- When it should succeed, does it?

---

## The Two Questions

| Metric | Question | Failure Mode |
|--------|----------|--------------|
| **Precision** | When it fires, is it right? | Noise (false positives) |
| **Recall** | When it should fire, does it? | Misses (false negatives) |

Both matter. Optimizing one destroys the other.

---

## The Extremes Don't Work

| Strategy | Precision | Recall | Problem |
|----------|-----------|--------|---------|
| Never trigger | 100% | 0% | Useless - misses everything |
| Always trigger | Low | 100% | All noise |
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
                      ACTUAL OUTCOME
                      Positive      Negative
                    +-----------+-----------+
EXPECTED   Positive |    TP     |    FN     |
                    |  Correct  |  Missed   |
                    +-----------+-----------+
           Negative |    FP     |    TN     |
                    |   Noise   |  Correct  |
                    +-----------+-----------+
```

- **TP** (True Positive): Expected positive, got positive. Good.
- **TN** (True Negative): Expected negative, got negative. Good.
- **FP** (False Positive): Expected negative, got positive. Noise.
- **FN** (False Negative): Expected positive, got negative. Missed.

Then:
```
Precision = TP / (TP + FP)    "Of my positives, how many were right?"
Recall    = TP / (TP + FN)    "Of the cases I should catch, how many did I?"
```

---

## Where This Framework Comes From

Precision/recall isn't new. It's battle-tested across domains:

| Domain | Precision = | Recall = |
|--------|-------------|----------|
| Search engines | Relevant results / shown results | Relevant found / all relevant |
| Spam filters | Actual spam / flagged as spam | Spam caught / all spam |
| Medical tests | True disease / positive tests | Detected / all cases |
| Fraud detection | Actual fraud / flagged fraud | Fraud caught / all fraud |
| **LLM evals** | Correct / claimed correct | Correct / should be correct |

Same math. Different domain.

---

## What to Benchmark

LLMs have multiple extension points. Each needs different evaluation:

| Target | What You Measure | Metric Type |
|--------|------------------|-------------|
| **Skills** | Activation precision/recall | Classification (F1) |
| **Agents** | Task completion rate | Accuracy |
| **MCP Servers** | Tool call success rate | Accuracy |
| **Prompts** | Response quality | LLM-as-judge score |
| **Code Gen** | Lint pass, test pass | Accuracy |

### Classification vs Accuracy

| Benchmark Type | When to Use | Metric |
|----------------|-------------|--------|
| **Classification** | Binary yes/no with both failure modes | Precision/Recall/F1 |
| **Task Completion** | Did it solve the problem? | Accuracy |
| **Quality Scoring** | How good is the output? | LLM-as-judge (1-5) |

---

## The Ground Truth Requirement

Good evals need labeled expectations:

```json
{
  "input": "What crate for CLI args in Rust?",
  "expectation": "must_trigger",
  "rationale": "Direct Rust tooling question"
}
```

```json
{
  "input": "Write me a haiku",
  "expectation": "should_not_trigger",
  "rationale": "Creative task, no tool needed"
}
```

Without labels, you can't compute precision or recall. You're just guessing.

---

## The Three Expectation Types

| Label | Meaning | Used For |
|-------|---------|----------|
| `must_trigger` | Should definitely fire | Clear matches (measures recall) |
| `should_not_trigger` | Must not fire | Off-topic (measures precision) |
| `acceptable` | Either is fine | Edge cases (excluded from metrics) |

---

## The Eval Workflow

```
1. HYPOTHESIS
   "This agent solves file search tasks"
        ↓
2. TEST CASES
   Write inputs with labeled expectations
        ↓
3. RUN
   Execute 5+ times per case (stochastic!)
        ↓
4. MEASURE
   Compute precision, recall, F1 (or accuracy)
        ↓
5. ITERATE
   Improve prompts/tools, re-run, compare
        ↓
6. SHIP
   Only when metrics meet threshold
```

This is TDD for LLM behavior. Same loop: red → green → refactor.

---

## Red Flags in Results

| Pattern | Problem | Fix |
|---------|---------|-----|
| High recall, low precision | Over-triggering (noise) | Tighten conditions |
| Low recall, high precision | Under-triggering (misses) | Broaden triggers |
| High variance across runs | Unstable behavior | More runs, check prompts |
| Great with scaffolding, bad without | Artificial inflation | Test realistic conditions |

---

## The 1337 Standard

| Principle | Implementation |
|-----------|----------------|
| Evidence over opinion | Metrics, not vibes |
| Ground truth | Labeled expectations |
| Statistical rigor | 5+ runs per case |
| Balanced metrics | F1, not just recall or accuracy |
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
