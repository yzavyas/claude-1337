# Why Evals Matter

An explanation of evaluation methodology for AI agents.

---

## The Problem: Agents Are Unreliable

You install a skill. You ask a relevant question. The agent ignores it.

This happens about 80% of the time. Not because the skill is broken, but because the agent doesn't reliably recognize when to use it.

Now imagine you're building a marketplace of skills. How do you know if a skill is valuable? How do you know if it activates when it should? How do you compare two approaches?

You need measurement. You need evals.

## What Is an Eval?

An eval (evaluation) is a test that measures behavior.

```
Input: "What crate should I use for CLI arguments in Rust?"
Expected: The rust-1337 skill should activate
Actual: (run the test and observe)
```

Simple concept. Hard to get right.

## The Trap: Vanity Metrics

Your first instinct might be:

> "Let's measure activation rate! If the skill activates 100% of the time, it's working!"

This is wrong. Here's why:

```python
# A skill that activates on EVERY prompt has 100% "activation rate"
# But it's useless - it's all noise
if any_prompt:
    activate_skill()  # 100% activation rate!
```

Raw activation rate is a **vanity metric**. It tells you nothing about quality.

## The Real Questions

What we actually need to know:

| Question | Metric |
|----------|--------|
| When the skill activates, is it actually relevant? | **Precision** |
| When the skill should activate, does it? | **Recall** |
| How do we balance both? | **F1 Score** |

This is the same framework used in:
- Search engines (relevant results)
- Spam filters (catch spam, don't block real email)
- Medical tests (detect disease, minimize false positives)

## The Confusion Matrix

Every test result falls into one of four boxes:

```
                        ACTUAL BEHAVIOR
                        Activated    Didn't Activate
                      +-----------+-----------+
SHOULD        Yes     |    TP     |    FN     |
ACTIVATE              | (correct) | (missed)  |
                      +-----------+-----------+
              No      |    FP     |    TN     |
                      | (noise)   | (correct) |
                      +-----------+-----------+
```

- **True Positive (TP)**: Should activate, did activate. Good.
- **True Negative (TN)**: Shouldn't activate, didn't. Good.
- **False Positive (FP)**: Shouldn't activate, but did. Noise.
- **False Negative (FN)**: Should activate, but didn't. Missed opportunity.

## Why Both Precision and Recall?

Optimizing for one destroys the other:

| Strategy | Precision | Recall | Problem |
|----------|-----------|--------|---------|
| Never activate | 100% (0/0) | 0% | Useless |
| Always activate | Low | 100% | All noise |
| Balanced | High | High | This is the goal |

**F1 Score** is the harmonic mean of precision and recall. It penalizes extremes.

## Connection to TDD

Test-Driven Development (TDD) follows a cycle:

```
1. Write a failing test
2. Make it pass
3. Refactor
4. Repeat
```

Evals are TDD for agent behavior:

```
1. Write test cases with expected outcomes
2. Run the eval, observe failures
3. Improve the skill (description, prompts, hooks)
4. Re-run eval to verify improvement
5. Repeat
```

The parallel is exact:

| TDD Concept | Eval Equivalent |
|-------------|-----------------|
| Unit test | Test case with expectation |
| Test suite | Labeled prompt corpus |
| Assertion | Outcome (TP/FP/TN/FN) |
| Coverage | Diversity of test cases |
| Green bar | High F1 score |

## Connection to Scientific Method

Evals are applied science:

| Scientific Method | Eval Workflow |
|-------------------|---------------|
| Hypothesis | "Forced eval hooks improve activation" |
| Prediction | "F1 should increase by 20%" |
| Experiment | Run suite with and without hooks |
| Observation | Record precision, recall, F1 |
| Conclusion | "Hooks improved recall but hurt precision" |

Without evals, you're guessing. With evals, you're experimenting.

## Why This Matters for Plugins

The claude-1337 marketplace has a philosophy:

> **Decisions, not catalogs. Evidence, not opinion.**

How do we know which plugins to build? How do we know if they're effective?

Evals answer these questions:

| Without Evals | With Evals |
|---------------|------------|
| "This skill seems good" | "This skill has 85% F1" |
| "Users probably need this" | "This skill activates correctly for 90% of relevant prompts" |
| "I think we should add X" | "Adding X improved recall by 15% without hurting precision" |

## The Eval-Driven Plugin Lifecycle

```
1. HYPOTHESIS: "Users need help with X"
   |
   v
2. BUILD: Create skill with description
   |
   v
3. EVAL: Run test suite, measure F1
   |
   v
4. ITERATE: Improve description based on failures
   |
   v
5. SHIP: Only when F1 meets threshold
   |
   v
6. MONITOR: Track real-world activation patterns
```

This is the scientific method applied to plugin development.

## What Makes a Good Eval?

| Principle | Implementation |
|-----------|----------------|
| Ground truth | Human-labeled expectations |
| Diversity | Direct, indirect, off-topic, edge cases |
| Sample size | 5+ runs per case (agents are stochastic) |
| Negative cases | Test that skills DON'T activate incorrectly |
| Reproducibility | Same suite, same conditions, comparable results |

## The Composability Principle

Evals compose just like plugins:

```
marketplace/
├── plugins/
│   ├── terminal-1337/     # Has its own test suite
│   ├── rust-1337/         # Has its own test suite
│   └── ...
└── evals/
    └── suites/
        ├── terminal-suite.json
        ├── rust-suite.json
        └── integration-suite.json  # Tests skill interactions
```

Each plugin is independently testable. Combined behavior is separately testable. This is modular quality assurance.

## Standing on the Shoulders of Giants

This methodology isn't new. We're applying:

| Field | Contribution |
|-------|--------------|
| Information Retrieval | Precision/recall framework |
| Machine Learning | Confusion matrices, F1 score |
| Software Engineering | TDD, test suites |
| Philosophy of Science | Hypothesis testing, falsifiability |

By using established frameworks, we:
1. Benefit from decades of refinement
2. Speak a common language with other practitioners
3. Avoid reinventing flawed approaches

## The Journey Ahead

This is alpha. We're learning. Open questions:

- What's the right F1 threshold for shipping a skill?
- How do we weight precision vs recall for different skill types?
- Can we automate corpus generation?
- How do we measure skill quality over time?

The eval framework gives us the tools to explore these questions systematically.

## Summary

| Concept | Key Insight |
|---------|-------------|
| Vanity metrics | Activation rate alone is meaningless |
| Precision/Recall | Measure both false positives and negatives |
| F1 Score | Balanced metric that penalizes extremes |
| TDD parallel | Evals are TDD for agent behavior |
| Scientific method | Hypothesis, experiment, observe, conclude |
| Composability | Plugins and evals are independently testable |

---

*"If you can't measure it, you can't improve it."* — Peter Drucker

*"The first principle is that you must not fool yourself — and you are the easiest person to fool."* — Richard Feynman
