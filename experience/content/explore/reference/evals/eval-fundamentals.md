# eval fundamentals

your agent solved 72% of tasks. is that good?

you don't know. and that's the problem.

---

## the five evaluation objectives

what you measure depends on what you're evaluating:

| objective | question | how to measure |
|-----------|----------|----------------|
| **task completion** | did it achieve the goal? | success rate, pass/fail |
| **tool correctness** | did it use tools correctly? | correct tools called, valid inputs |
| **output quality** | is the output good? | LLM-as-judge, rubrics, rules |
| **reliability** | is it consistent? | variance across runs |
| **robustness** | does it handle variations? | stress testing, perturbations |

---

## matching objectives to targets

### agents

| what to measure | metric | example |
|-----------------|--------|---------|
| task completion | success rate | 84% of GitHub issues resolved |
| tool correctness | tool accuracy | called right tools with valid inputs |
| output quality | LLM-as-judge | code passes review criteria |
| reliability | consistency | similar results across 5 runs |

### skills

| what to measure | metric | example |
|-----------------|--------|---------|
| activation | precision/recall/F1 | triggers on right prompts, ignores wrong ones |
| content quality | LLM-as-judge | loaded content is useful |

### MCP servers

| what to measure | metric | example |
|-----------------|--------|---------|
| tool correctness | success rate | 95% of calls return valid response |
| schema compliance | validation rate | inputs/outputs match schema |
| reliability | error rate | low failure rate over time |

### prompts

| what to measure | metric | example |
|-----------------|--------|---------|
| output quality | LLM-as-judge (1-5) | responses score 4.2/5 on rubric |
| rule compliance | pass rate | output follows format requirements |
| reliability | variance | consistent quality across runs |

---

## the three metric types

### 1. accuracy (task completion)

binary pass/fail. did it work?

```
Accuracy = Correct / Total
```

**use for:** SWE-bench, code execution, test pass rates

### 2. classification (precision/recall/F1)

when you have both false positives AND false negatives.

```
Precision = TP / (TP + FP)    "when it fires, is it right?"
Recall    = TP / (TP + FN)    "when it should fire, does it?"
F1        = 2×(P×R)/(P+R)     "balanced score"
```

**use for:** skill activation, trigger detection, classification tasks

### 3. quality scoring (LLM-as-judge)

subjective quality on a scale.

```
Score = LLM rates output against rubric (1-5 or 1-10)
```

**use for:** prompt quality, response evaluation, code review

---

## task completion

the simplest metric: did it work?

```
Success Rate = (Tasks Completed Successfully) / (Total Tasks)
```

| benchmark | task | success criteria |
|-----------|------|------------------|
| SWE-bench | fix GitHub issue | tests pass |
| HumanEval | write function from docstring | tests pass |
| custom agent | complete user request | defined success state reached |

**limitations:**
- doesn't measure HOW it succeeded (quality, efficiency)
- binary - no partial credit
- depends on test quality

---

## tool correctness

did the agent use the right tools with correct inputs?

| level | what's checked |
|-------|----------------|
| basic | correct tool name called |
| strict | + correct input parameters |
| full | + correct output handling |

```python
# expected: search_web("latest rust async patterns")
# actual: search_web("rust async")

# basic: PASS (correct tool)
# strict: FAIL (wrong query)
```

---

## output quality

is the output good? three approaches:

### LLM-as-judge

```python
prompt = f"""
Rate this code review on a scale of 1-5:

{output}

Criteria:
- Identifies real issues
- Provides actionable feedback
- Appropriate tone
"""
```

### rubric-based

| score | criteria |
|-------|----------|
| 5 | exceeds requirements, no issues |
| 4 | meets requirements, minor issues |
| 3 | partially meets requirements |
| 2 | significant gaps |
| 1 | fails requirements |

### rules-based

deterministic checks:
- output contains required fields
- code passes linter
- response under token limit
- no forbidden content

---

## reliability

is it consistent across runs?

LLMs are stochastic. run the same task 5 times:

```
Run 1: SUCCESS
Run 2: SUCCESS
Run 3: FAIL
Run 4: SUCCESS
Run 5: SUCCESS

Reliability = 4/5 = 80%
```

**why it matters:**
- production systems need predictability
- high variance = unreliable
- enterprise contexts require deterministic behavior

**measuring it:**
- run 5+ times per test case
- compute variance/standard deviation
- report confidence intervals

---

## classification (precision/recall/F1)

use when you have TWO failure modes:
- **false positive**: triggered when it shouldn't (noise)
- **false negative**: didn't trigger when it should (miss)

### the confusion matrix

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

### why F1?

| precision | recall | regular avg | F1 |
|-----------|--------|-------------|-----|
| 100% | 0% | 50% | **0%** |
| 100% | 50% | 75% | **67%** |
| 80% | 80% | 80% | **80%** |

you can't game F1 by going extreme.

**when to use:**
- skill activation (should it trigger?)
- spam detection
- any binary classification with asymmetric costs

---

## the eval workflow

```
1. DEFINE
   What objective? (task completion, quality, reliability?)
   What target? (agent, skill, MCP, prompt?)
        ↓
2. DESIGN
   Create test cases with expected outcomes
        ↓
3. RUN
   Execute 5+ times per case (stochastic!)
        ↓
4. MEASURE
   Compute appropriate metric for objective
        ↓
5. ITERATE
   Improve based on failures, re-run, compare
        ↓
6. SHIP
   Only when metrics meet threshold
```

---

## ground truth requirement

good evals need labeled expectations:

```json
// for task completion
{"task": "fix login bug", "expected": "tests pass"}

// for classification
{"input": "What crate for CLI?", "expected": "must_trigger"}
{"input": "Write a haiku", "expected": "should_not_trigger"}

// for quality
{"input": "Review this code", "rubric": ["accuracy", "actionable", "tone"]}
```

---

## red flags

| pattern | problem | fix |
|---------|---------|-----|
| high variance across runs | unreliable | more runs, check prompts |
| great with scaffolding, bad without | artificial inflation | test realistic conditions |
| high recall, low precision | too noisy | tighten conditions |
| high task completion, low quality | passing but bad | add quality metrics |

---

## the 1337 standard

| principle | implementation |
|-----------|----------------|
| match metric to objective | task completion, quality, reliability - not just one |
| ground truth | labeled expectations, not vibes |
| statistical rigor | 5+ runs per case |
| reproducibility | same suite, comparable results |

---

## quick reference

```
TASK COMPLETION
  Accuracy = Correct / Total
  Use for: SWE-bench, pass/fail tasks

CLASSIFICATION
  Precision = TP / (TP + FP)
  Recall = TP / (TP + FN)
  F1 = 2×(P×R)/(P+R)
  Use for: skill activation, triggers

QUALITY
  LLM-as-judge, rubrics, rules
  Use for: output evaluation, review
```

---

## further reading

- [why-evals-matter](why-evals-matter/) - philosophy, TDD parallel
- [reference](reference/) - CLI commands, schemas, modes

---

## sources

- [Evaluation and Benchmarking of LLM Agents: A Survey](https://arxiv.org/abs/2507.21504)
- [DeepEval: Task Completion Metric](https://deepeval.com/docs/metrics-task-completion)
- [DeepEval: Tool Correctness Metric](https://deepeval.com/docs/metrics-tool-correctness)

---

*"If you can't measure it, you can't improve it."* — Peter Drucker
