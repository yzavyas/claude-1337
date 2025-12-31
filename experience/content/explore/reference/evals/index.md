# evals

evaluation framework for AI agents

## overview

- [why evals matter](why-evals-matter/) — philosophy, TDD parallel, scientific method
- [eval fundamentals](eval-fundamentals/) — objectives, metrics, workflow
- [reference](reference/) — CLI commands, schemas, modes

## quick start

```
cd evals
uv sync
uv run skill-test test "how do i search files?" -s terminal-1337 -n 3
```

## the problem

you install a skill. you ask a relevant question. the agent ignores it 80% of the time.

how do you know if a skill is valuable? how do you compare two approaches?

you need measurement. you need evals.

## the trap: vanity metrics

raw activation rate is meaningless:

```python
# A skill that activates on EVERY prompt has 100% "activation rate"
# But it's useless - it's all noise
if any_prompt:
    activate_skill()  # 100% activation rate!
```

## the real metrics

| question | metric |
|----------|--------|
| when it fires, is it right? | **precision** |
| when it should fire, does it? | **recall** |
| balanced score | **F1** |

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
