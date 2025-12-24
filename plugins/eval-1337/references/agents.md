# Agent Evaluation

Measuring whether agents complete tasks and use tools correctly.

## Primary Metrics

| Metric | Question | Type |
|--------|----------|------|
| Task Completion | Did it achieve the goal? | Accuracy |
| Tool Correctness | Did it call right tools? | Accuracy |
| Step Efficiency | Optimal path taken? | Score |
| Reliability | Consistent across runs? | Variance |

## DeepEval Implementation

### Task Completion

```python
from deepeval.metrics import TaskCompletionMetric
from deepeval.tracing import observe

@observe(type="agent")
def my_agent(user_input):
    # Agent logic here
    return result

# Evaluate
metric = TaskCompletionMetric(threshold=0.7)
# Uses LLM-as-judge to score task vs outcome alignment
```

**How it works:**
- Extracts "task" from input
- Extracts "outcome" from trace
- LLM judges alignment
- Returns score 0-1

### Tool Correctness

```python
from deepeval.metrics import ToolCorrectnessMetric
from deepeval.test_case import LLMTestCase, ToolCall

metric = ToolCorrectnessMetric()

test_case = LLMTestCase(
    input="Book cheapest flight NYC to LA",
    actual_output="Booked FL456 for $380",
    tools_called=[ToolCall(name="search_flights"), ToolCall(name="book_flight")],
    expected_tools=[ToolCall(name="search_flights"), ToolCall(name="book_flight")],
)
```

**Strictness Levels:**
| Level | Checks |
|-------|--------|
| Basic | Tool name matches |
| Strict | + Input parameters match |
| Full | + Output handling correct |

## End-to-End vs Component

| Type | Metrics | Scope |
|------|---------|-------|
| End-to-end | TaskCompletion, StepEfficiency | Full agent trace |
| Component | ToolCorrectness, ArgumentCorrectness | Single component |

```python
# End-to-end: pass to evals_iterator
evals_iterator(metrics=[TaskCompletionMetric()])

# Component: attach to @observe
@observe(metrics=[ToolCorrectnessMetric()])
def tool_component():
    pass
```

## SWE-bench Pattern

Task completion benchmark for code agents:

```
Input: GitHub issue + repo
Output: Generated patch
Success: Tests pass

Accuracy = (Issues resolved) / (Total issues)
```

**Variants:**
- Full (2,294) - noisy
- Verified (500) - human-validated
- Pro (1,865) - anti-contamination

## Gotchas

| Trap | Fix |
|------|-----|
| Testing happy path only | Add failure cases, edge cases |
| Single run per test | 5+ runs (stochastic) |
| Task completion only | Add tool correctness, quality |
| Missing baseline | Compare against no-agent baseline |
