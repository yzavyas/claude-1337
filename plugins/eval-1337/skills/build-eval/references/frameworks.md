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
5. Phoenix Evals → Local LLM-as-judge, drift detection
```

---

## Phoenix Evals (Local)

**Best for:** Local LLM-as-judge, no cloud dependency

**Key Features:**
- Runs entirely local (localhost:6006)
- LLM-as-judge classification
- RAG relevance scoring
- Drift detection

**Install:**
```bash
pip install arize-phoenix-evals
```

**Usage:**
```python
from phoenix.evals import llm_classify, OpenAIModel
import pandas as pd

eval_model = OpenAIModel(model="gpt-4o-mini")

# Classify responses
results = llm_classify(
    dataframe=pd.DataFrame(responses),
    template="Is this response helpful? {response}",
    model=eval_model,
    rails=["helpful", "unhelpful"],
)

# RAG relevance
from phoenix.evals import run_relevance_eval

relevance = run_relevance_eval(
    dataframe=df,
    model=eval_model,
    query_column="query",
    document_column="retrieved_doc",
)
```

**Strengths:**
- No cloud dependency
- Integrates with Phoenix tracing
- Supports custom eval templates

---

## Sources

- [DeepEval Docs](https://deepeval.com/docs) - Metrics reference, tracing API
- [Braintrust AutoEvals](https://github.com/braintrustdata/autoevals) - Scorer implementations
- [RAGAS Docs](https://docs.ragas.io/en/stable/) - Agent and RAG metrics
- [Promptfoo Docs](https://promptfoo.dev/docs/intro) - YAML config, red teaming
- [Phoenix Evals](https://github.com/Arize-ai/phoenix) - Local evaluation library
- [LLM Agent Evaluation Survey](https://arxiv.org/abs/2507.21504) - KDD 2025, comprehensive taxonomy
