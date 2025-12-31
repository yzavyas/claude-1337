# why evals matter

an explanation of evaluation methodology for AI agents.

---

## the problem: agents are unreliable

you install a skill. you ask a relevant question. the agent ignores it.

this happens about 80% of the time — the agent doesn't reliably recognize when to use it.

now imagine you're building a marketplace of skills. how do you know if a skill is valuable? how do you know if it activates when it should? how do you compare two approaches?

you need measurement. you need evals.

## what is an eval?

an eval (evaluation) is a test that measures behavior.

```
Input: "What crate should I use for CLI arguments in Rust?"
Expected: The rust-1337 skill should activate
Actual: (run the test and observe)
```

simple concept. hard to get right.

## the trap: vanity metrics

your first instinct might be:

> "Let's measure activation rate! If the skill activates 100% of the time, it's working!"

this is wrong. here's why:

```python
# A skill that activates on EVERY prompt has 100% "activation rate"
# But it's useless - it's all noise
if any_prompt:
    activate_skill()  # 100% activation rate!
```

raw activation rate is a **vanity metric**. it tells you nothing about quality.

## the real questions

what we actually need to know:

| question | metric |
|----------|--------|
| when the skill activates, is it actually relevant? | **precision** |
| when the skill should activate, does it? | **recall** |
| how do we balance both? | **F1 score** |

this is the same framework used in:
- search engines (relevant results)
- spam filters (catch spam, don't block real email)
- medical tests (detect disease, minimize false positives)

## the confusion matrix

every test result falls into one of four boxes:

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

- **True Positive (TP)**: should activate, did activate. good.
- **True Negative (TN)**: shouldn't activate, didn't. good.
- **False Positive (FP)**: shouldn't activate, but did. noise.
- **False Negative (FN)**: should activate, but didn't. missed opportunity.

## why both precision and recall?

optimizing for one destroys the other:

| strategy | precision | recall | problem |
|----------|-----------|--------|---------|
| never activate | 100% (0/0) | 0% | useless |
| always activate | low | 100% | all noise |
| balanced | high | high | this is the goal |

**F1 Score** is the harmonic mean of precision and recall. it penalizes extremes.

## connection to TDD

test-driven development (TDD) follows a cycle:

```
1. Write a failing test
2. Make it pass
3. Refactor
4. Repeat
```

evals are TDD for agent behavior:

```
1. Write test cases with expected outcomes
2. Run the eval, observe failures
3. Improve the skill (description, prompts, hooks)
4. Re-run eval to verify improvement
5. Repeat
```

the parallel is exact:

| TDD concept | eval equivalent |
|-------------|-----------------|
| unit test | test case with expectation |
| test suite | labeled prompt corpus |
| assertion | outcome (TP/FP/TN/FN) |
| coverage | diversity of test cases |
| green bar | high F1 score |

## connection to scientific method

evals are applied science:

| scientific method | eval workflow |
|-------------------|---------------|
| hypothesis | "forced eval hooks improve activation" |
| prediction | "F1 should increase by 20%" |
| experiment | run suite with and without hooks |
| observation | record precision, recall, F1 |
| conclusion | "hooks improved recall but hurt precision" |

without evals, you're guessing. with evals, you're experimenting.

## why this matters for plugins

the claude-1337 marketplace has a philosophy:

> **decisions, not catalogs. evidence, not opinion.**

how do we know which plugins to build? how do we know if they're effective?

evals answer these questions:

| without evals | with evals |
|---------------|------------|
| "this skill seems good" | "this skill has 85% F1" |
| "users probably need this" | "this skill activates correctly for 90% of relevant prompts" |
| "i think we should add X" | "adding X improved recall by 15% without hurting precision" |

## the eval-driven plugin lifecycle

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

this is the scientific method applied to plugin development.

## what makes a good eval?

| principle | implementation |
|-----------|----------------|
| ground truth | human-labeled expectations |
| diversity | direct, indirect, off-topic, edge cases |
| sample size | 5+ runs per case (agents are stochastic) |
| negative cases | test that skills DON'T activate incorrectly |
| reproducibility | same suite, same conditions, comparable results |

## the composability principle

evals compose just like plugins:

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

each plugin is independently testable. combined behavior is separately testable. this is modular quality assurance.

## standing on the shoulders of giants

this methodology applies established frameworks:

| field | contribution |
|-------|--------------|
| information retrieval | precision/recall framework |
| machine learning | confusion matrices, F1 score |
| software engineering | TDD, test suites |
| philosophy of science | hypothesis testing, falsifiability |

by using established frameworks, we:
1. benefit from decades of refinement
2. speak a common language with other practitioners
3. avoid reinventing flawed approaches

## the journey ahead

this is alpha. we're learning. open questions:

- what's the right F1 threshold for shipping a skill?
- how do we weight precision vs recall for different skill types?
- can we automate corpus generation?
- how do we measure skill quality over time?

the eval framework gives us the tools to explore these questions systematically.

## summary

| concept | key insight |
|---------|-------------|
| vanity metrics | activation rate alone is meaningless |
| precision/recall | measure both false positives and negatives |
| F1 score | balanced metric that penalizes extremes |
| TDD parallel | evals are TDD for agent behavior |
| scientific method | hypothesis, experiment, observe, conclude |
| composability | plugins and evals are independently testable |

---

*"If you can't measure it, you can't improve it."* — Peter Drucker

*"The first principle is that you must not fool yourself — and you are the easiest person to fool."* — Richard Feynman
