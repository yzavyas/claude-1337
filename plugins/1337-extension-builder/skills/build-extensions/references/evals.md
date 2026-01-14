# Evals

How to evaluate extensions. Match metric to what you're measuring.

For comprehensive eval guidance, see the `eval-1337` skill.

---

## Match Metric to Target

| Target | What to Measure | Metric | Framework |
|--------|-----------------|--------|-----------|
| **Skills** | Activation (L1) | Precision/Recall/F1 | Custom |
| **Skills** | Methodology (L2) | LLM-as-judge rubric | DeepEval GEval |
| **Agents** | Task completion | Accuracy (pass/fail) | DeepEval |
| **Agents** | Tool usage | ToolCorrectnessMetric | DeepEval |
| **MCP** | Tool calls | ToolCallAccuracy | RAGAS |
| **Commands** | Behavior | Custom assertions | Pytest |
| **Hooks** | Exit codes | Unit tests | Pytest |
| **SDK Apps** | End-to-end | TaskCompletionMetric | DeepEval |

---

## The Core Problem

```python
# This tells you NOTHING
activation_rate = 100%  # Activates on every prompt = useless
```

Single metrics lie. You need to measure BOTH failure modes.

---

## Classification Metrics (F1)

Use when you have TWO failure modes:

```
                      ACTUAL
                      Yes         No
                  +-----------+-----------+
EXPECTED    Yes   |    TP     |    FN     |
                  |  Correct  |  Missed   |
                  +-----------+-----------+
            No    |    FP     |    TN     |
                  |   Noise   |  Correct  |
                  +-----------+-----------+

Precision = TP / (TP + FP)   "when it fires, is it right?"
Recall    = TP / (TP + FN)   "when it should fire, does it?"
F1        = 2×(P×R)/(P+R)    "balanced score"
```

---

## Labeled Test Cases

```json
{"input": "How do I use ripgrep?", "expectation": "must_trigger"}
{"input": "Write a haiku", "expectation": "should_not_trigger"}
{"input": "Explain ownership", "expectation": "acceptable"}
```

| Label | Meaning | Measures |
|-------|---------|----------|
| `must_trigger` | Should definitely fire | Recall (misses) |
| `should_not_trigger` | Must not fire | Precision (noise) |
| `acceptable` | Either outcome fine | Excluded |

---

## Skill Activation Eval

```python
from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk.types import AssistantMessage, ToolUseBlock

async def test_skill_activation(prompt: str, expected_skill: str) -> bool:
    """Test if a skill activates for a given prompt."""
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(allowed_tools=["Skill"])
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    if block.name == "Skill":
                        return block.input.get("skill") == expected_skill
    return False

# Run 5+ times per case (LLMs are stochastic)
results = [await test_skill_activation("How do I use grep?", "terminal-1337") for _ in range(5)]
activation_rate = sum(results) / len(results)
```

---

## Methodology Eval (Level 2)

Use LLM-as-judge to score responses against a rubric.

```python
from deepeval.metrics import GEval

methodology_metric = GEval(
    name="MethodologyAdherence",
    criteria="""
    Score how well the response follows methodology:
    1. Evidence: Does it cite sources? (production > blogs)
    2. WHY: Does it explain reasoning, not just answers?
    3. Verification: Does it check its own work?
    4. Honesty: Does it acknowledge uncertainty?
    """,
    threshold=0.7
)
```

### Rubric

| Criterion | 0 (Absent) | 1 (Partial) | 2 (Full) |
|-----------|------------|-------------|----------|
| **Evidence** | No sources | Source mentioned | Production source with context |
| **WHY** | Just answer | Some reasoning | Full reasoning chain |
| **Verification** | No checking | Self-review noted | Explicit verification |
| **Honesty** | Overconfident | Sometimes hedges | Calibrated confidence |

---

## Production Gotchas

| Trap | Fix |
|------|-----|
| Single test run | **5+ runs per case** - LLMs are stochastic |
| Measuring recall only | **Add precision** - high recall + low precision = noise |
| "Forced eval" inflation | **Test realistic conditions** |
| No ground truth | **Label expectations** |
| Wrong metric for target | **Match to objective** |

---

## The Eval Workflow

```
1. DEFINE   → What objective? What target?
2. DESIGN   → Create labeled test cases
3. RUN      → Execute 5+ times per case
4. MEASURE  → Compute appropriate metric
5. ITERATE  → Improve based on failures
6. SHIP     → Only when metrics meet threshold
```

---

## Observability for Evals

```python
from opentelemetry import trace

tracer = trace.get_tracer("eval-runner")

async def run_eval_case(test_case: dict):
    with tracer.start_as_current_span("eval_case") as span:
        span.set_attribute("prompt", test_case["input"][:200])
        span.set_attribute("expectation", test_case["expectation"])

        result = await test_skill_activation(
            test_case["input"],
            test_case.get("skill")
        )

        span.set_attribute("activated", result)
        span.set_attribute("correct",
            (result and test_case["expectation"] == "must_trigger") or
            (not result and test_case["expectation"] == "should_not_trigger")
        )
        return result
```

### Spans

| span | attributes |
|------|------------|
| `eval_suite` | suite_name, total_cases, precision, recall, f1 |
| `eval_case` | prompt, expectation, activated, correct |

---

## Framework Decision

| Situation | Use |
|-----------|-----|
| Python agent evals | **DeepEval** |
| TypeScript/Node | **Braintrust** |
| RAG pipelines | **RAGAS** |
| Skill activation | **Custom F1** |

---

## Quality Checklist

- [ ] Labeled expectations (must/should_not/acceptable)
- [ ] 5+ runs per case
- [ ] Both precision AND recall measured
- [ ] Tested in realistic conditions (not forced)
- [ ] Threshold defined before shipping
- [ ] Negative test cases included

---

## Sources

- [eval-1337 SKILL.md](../../eval-1337/SKILL.md) — full eval methodology
- [DeepEval](https://deepeval.com/) — Python eval framework
- [Braintrust](https://www.braintrust.dev/) — TypeScript eval framework
- [RAGAS](https://docs.ragas.io/) — RAG evaluation
- [Scott Spence Study](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably) — 200+ activation tests
