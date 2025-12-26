# Eval Fundamentals

Your agent solved 72% of tasks. Is that good?

You don't know. And that's the problem.

---

## The Five Evaluation Objectives

What you measure depends on what you're evaluating:

| Objective | Question | How to Measure |
|-----------|----------|----------------|
| **Task Completion** | Did it achieve the goal? | Success rate, pass/fail |
| **Tool Correctness** | Did it use tools correctly? | Correct tools called, valid inputs |
| **Output Quality** | Is the output good? | LLM-as-judge, rubrics, rules |
| **Reliability** | Is it consistent? | Variance across runs |
| **Robustness** | Does it handle variations? | Stress testing, perturbations |

---

## Matching Objectives to Targets

### Agents

| What to Measure | Metric | Example |
|-----------------|--------|---------|
| Task completion | Success rate | 84% of GitHub issues resolved |
| Tool correctness | Tool accuracy | Called right tools with valid inputs |
| Output quality | LLM-as-judge | Code passes review criteria |
| Reliability | Consistency | Similar results across 5 runs |

### Skills

| What to Measure | Metric | Example |
|-----------------|--------|---------|
| Activation | Precision/Recall/F1 | Triggers on right prompts, ignores wrong ones |
| Content quality | LLM-as-judge | Loaded content is useful |

### MCP Servers

| What to Measure | Metric | Example |
|-----------------|--------|---------|
| Tool correctness | Success rate | 95% of calls return valid response |
| Schema compliance | Validation rate | Inputs/outputs match schema |
| Reliability | Error rate | Low failure rate over time |

### Prompts

| What to Measure | Metric | Example |
|-----------------|--------|---------|
| Output quality | LLM-as-judge (1-5) | Responses score 4.2/5 on rubric |
| Rule compliance | Pass rate | Output follows format requirements |
| Reliability | Variance | Consistent quality across runs |

---

## The Three Metric Types

### 1. Accuracy (Task Completion)

Binary pass/fail. Did it work?

```
Accuracy = Correct / Total
```

**Use for:** SWE-bench, code execution, test pass rates

### 2. Classification (Precision/Recall/F1)

When you have both false positives AND false negatives.

```
Precision = TP / (TP + FP)    "when it fires, is it right?"
Recall    = TP / (TP + FN)    "when it should fire, does it?"
F1        = 2×(P×R)/(P+R)     "balanced score"
```

**Use for:** Skill activation, trigger detection, classification tasks

### 3. Quality Scoring (LLM-as-Judge)

Subjective quality on a scale.

```
Score = LLM rates output against rubric (1-5 or 1-10)
```

**Use for:** Prompt quality, response evaluation, code review

---

## Task Completion

The simplest metric: did it work?

```
Success Rate = (Tasks Completed Successfully) / (Total Tasks)
```

| Benchmark | Task | Success Criteria |
|-----------|------|------------------|
| SWE-bench | Fix GitHub issue | Tests pass |
| HumanEval | Write function from docstring | Tests pass |
| Custom agent | Complete user request | Defined success state reached |

**Limitations:**
- Doesn't measure HOW it succeeded (quality, efficiency)
- Binary - no partial credit
- Depends on test quality

---

## Tool Correctness

Did the agent use the right tools with correct inputs?

| Level | What's Checked |
|-------|----------------|
| Basic | Correct tool name called |
| Strict | + Correct input parameters |
| Full | + Correct output handling |

```python
# expected: search_web("latest rust async patterns")
# actual: search_web("rust async")

# basic: PASS (correct tool)
# strict: FAIL (wrong query)
```

---

## Output Quality

Is the output good? Three approaches:

### LLM-as-Judge

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

### Rubric-Based

| Score | Criteria |
|-------|----------|
| 5 | Exceeds requirements, no issues |
| 4 | Meets requirements, minor issues |
| 3 | Partially meets requirements |
| 2 | Significant gaps |
| 1 | Fails requirements |

### Rules-Based

Deterministic checks:
- Output contains required fields
- Code passes linter
- Response under token limit
- No forbidden content

---

## Reliability

Is it consistent across runs?

LLMs are stochastic. Run the same task 5 times:

```
Run 1: SUCCESS
Run 2: SUCCESS
Run 3: FAIL
Run 4: SUCCESS
Run 5: SUCCESS

Reliability = 4/5 = 80%
```

**Why it matters:**
- Production systems need predictability
- High variance = unreliable
- Enterprise contexts require deterministic behavior

**Measuring it:**
- Run 5+ times per test case
- Compute variance/standard deviation
- Report confidence intervals

---

## Classification (Precision/Recall/F1)

Use when you have TWO failure modes:
- **False positive**: Triggered when it shouldn't (noise)
- **False negative**: Didn't trigger when it should (miss)

### The Confusion Matrix

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

### Why F1?

| Precision | Recall | Regular Avg | F1 |
|-----------|--------|-------------|-----|
| 100% | 0% | 50% | **0%** |
| 100% | 50% | 75% | **67%** |
| 80% | 80% | 80% | **80%** |

You can't game F1 by going extreme.

**When to use:**
- Skill activation (should it trigger?)
- Spam detection
- Any binary classification with asymmetric costs

---

## The Eval Workflow

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

## Ground Truth Requirement

Good evals need labeled expectations:

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

## Red Flags

| Pattern | Problem | Fix |
|---------|---------|-----|
| High variance across runs | Unreliable | More runs, check prompts |
| Great with scaffolding, bad without | Artificial inflation | Test realistic conditions |
| High recall, low precision | Too noisy | Tighten conditions |
| High task completion, low quality | Passing but bad | Add quality metrics |

---

## The 1337 Standard

| Principle | Implementation |
|-----------|----------------|
| Match metric to objective | Task completion, quality, reliability - not just one |
| Ground truth | Labeled expectations, not vibes |
| Statistical rigor | 5+ runs per case |
| Reproducibility | Same suite, comparable results |

---

## Quick Reference

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

## Further Reading

- [why-evals-matter.md](why-evals-matter.md) - Philosophy, TDD parallel
- [reference.md](reference.md) - CLI commands, schemas, modes

---

## Sources

- [Evaluation and Benchmarking of LLM Agents: A Survey](https://arxiv.org/abs/2507.21504)
- [DeepEval: Task Completion Metric](https://deepeval.com/docs/metrics-task-completion)
- [DeepEval: Tool Correctness Metric](https://deepeval.com/docs/metrics-tool-correctness)

---

*"If you can't measure it, you can't improve it."* — Peter Drucker
