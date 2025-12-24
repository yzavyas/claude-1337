# Eval Frameworks

Choosing the right framework for your eval target.

## Decision Matrix

| Target | Framework | Why |
|--------|-----------|-----|
| Python agents | **DeepEval** | TaskCompletionMetric, full trace analysis |
| TypeScript/Node | **Braintrust** | Identical API, production adoption |
| RAG pipelines | **RAGAS** | Context metrics, ToolCallF1 |
| Skill activation | **Custom** | Precision/recall with labeled expectations |
| Red teaming | **Promptfoo** | Security focus, YAML config |

## DeepEval (Python)

**Best for:** Agent evaluation, component-level metrics

**Key Metrics:**
| Metric | Level | Purpose |
|--------|-------|---------|
| TaskCompletionMetric | End-to-end | Did agent complete task? |
| ToolCorrectnessMetric | Component | Right tools called? |
| StepEfficiencyMetric | End-to-end | Optimal path taken? |
| ArgumentCorrectnessMetric | Component | Correct parameters? |

**Install:**
```bash
pip install deepeval
```

**Usage:**
```python
from deepeval.metrics import TaskCompletionMetric
from deepeval.tracing import observe

@observe(type="agent")
def my_agent(input):
    return process(input)

metric = TaskCompletionMetric(threshold=0.7)
```

**Strengths:**
- Comprehensive agent metrics
- Trace-based evaluation
- Component vs end-to-end distinction

---

## Braintrust AutoEvals (TypeScript/Python)

**Best for:** Cross-language teams, quality scoring

**Key Scorers:**
- Factuality - factual consistency
- AnswerRelevancy - addresses input
- Custom LLM-as-judge

**Install:**
```bash
npm install autoevals braintrust
# or
pip install autoevals braintrust
```

**Usage:**
```typescript
import { Factuality } from "autoevals";
import { Eval } from "braintrust";

Eval("MyEval", {
  data: () => testCases,
  task: async (input) => await llm(input),
  scores: [Factuality],
});
```

**Strengths:**
- Identical Python/TypeScript API
- Production adoption (Notion, Stripe, Vercel)
- Built-in CI/CD integration

---

## RAGAS (Python)

**Best for:** RAG evaluation, tool call metrics

**Key Metrics:**
| Metric | Purpose |
|--------|---------|
| ToolCallAccuracy | Exact match of tool calls |
| ToolCallF1 | Precision/recall of calls |
| AgentGoalAccuracy | Binary goal achievement |
| TopicAdherence | Stayed on domain? |

**Install:**
```bash
pip install ragas
```

**Usage:**
```python
from ragas.metrics import ToolCallAccuracy
from ragas import evaluate

result = evaluate(
    dataset=my_dataset,
    metrics=[ToolCallAccuracy()]
)
```

**Strengths:**
- F1-based metrics for iteration
- Strong RAG metrics (faithfulness, relevancy)
- NVIDIA/industry adoption

---

## Promptfoo (CLI)

**Best for:** Security testing, YAML-based config

**Key Features:**
- Red teaming and adversarial testing
- YAML configuration
- CI/CD integration

**Install:**
```bash
npm install -g promptfoo
```

**Usage:**
```yaml
# promptfooconfig.yaml
prompts:
  - "Answer: {{query}}"
providers:
  - openai:gpt-4
tests:
  - vars:
      query: "What is 2+2?"
    assert:
      - type: contains
        value: "4"
```

**Strengths:**
- Security-focused
- YAML over code
- Built-in red teaming

---

## Custom Framework (Skill Activation)

**Best for:** Skill activation precision/recall

See the existing `evals/` directory in claude-1337.

**Key Features:**
- Labeled expectations (must_trigger, should_not_trigger)
- Precision/recall/F1 calculation
- Multiple modes (baseline, smart, forced)

**Usage:**
```bash
cd evals
uv run skill-test suite suites/rigorous-v1.json -m baseline
```

---

## Framework Comparison

| Feature | DeepEval | Braintrust | RAGAS | Promptfoo |
|---------|----------|------------|-------|-----------|
| Language | Python | Python + TS | Python | YAML/CLI |
| Agent metrics | Excellent | Good | Good | Limited |
| RAG metrics | Limited | Limited | Excellent | Limited |
| Security | Limited | Limited | Limited | Excellent |
| Trace analysis | Yes | Limited | No | No |
| CI/CD | Good | Excellent | Good | Excellent |

## When to Combine

Use multiple frameworks:

```
1. DeepEval      → Agent task completion, tool correctness
2. Braintrust    → Output quality scoring (LLM-as-judge)
3. RAGAS         → RAG-specific metrics (if applicable)
4. Promptfoo     → Security/red-teaming (before production)
```
