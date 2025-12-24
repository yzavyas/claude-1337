# Observability and Interpretability

Tracing, debugging, and understanding agent behavior.

## What to Measure

| Metric | Question | Tool |
|--------|----------|------|
| Trace spans | What steps did the agent take? | Phoenix |
| Latency breakdown | Where is time spent? | Phoenix |
| Token flow | How do tokens flow through? | Langfuse |
| Decision points | Why did it make this choice? | Manual |

## Phoenix (Arize)

[Phoenix](https://docs.arize.com/phoenix) provides LLM observability:

```python
import phoenix as px
from phoenix.trace import SpanEvaluator

# Launch Phoenix
session = px.launch_app()

# Instrument your agent
from openinference.instrumentation import instrument
instrument()

# Now run your agent - traces appear automatically
result = my_agent("input")

# Query traces
traces = px.Client().get_traces()
```

**Key Features:**
- Automatic trace collection
- Span visualization
- Latency breakdown
- Token usage per span

## Tracing Pattern

```python
from opentelemetry import trace

tracer = trace.get_tracer("agent-eval")

def my_agent(input):
    with tracer.start_as_current_span("agent") as span:
        span.set_attribute("input", input)

        with tracer.start_as_current_span("retrieve") as retrieve_span:
            docs = retrieve(input)
            retrieve_span.set_attribute("doc_count", len(docs))

        with tracer.start_as_current_span("generate") as gen_span:
            output = generate(input, docs)
            gen_span.set_attribute("output_length", len(output))

        span.set_attribute("output", output)
        return output
```

## Langfuse Tracing

```python
from langfuse.decorators import observe, langfuse_context

@observe()
def my_agent(input):
    docs = retrieve(input)
    langfuse_context.update_current_trace(
        metadata={"doc_count": len(docs)}
    )

    output = generate(input, docs)
    return output

# View in Langfuse dashboard
# https://cloud.langfuse.com
```

**TypeScript:**
```typescript
import { Langfuse } from "langfuse";

const langfuse = new Langfuse();

async function myAgent(input: string) {
  const trace = langfuse.trace({ name: "my-agent" });

  const retrieveSpan = trace.span({ name: "retrieve" });
  const docs = await retrieve(input);
  retrieveSpan.end({ output: { docCount: docs.length } });

  const generateSpan = trace.span({ name: "generate" });
  const output = await generate(input, docs);
  generateSpan.end({ output: { length: output.length } });

  return output;
}
```

## Debugging Failed Evals

When an eval fails, trace analysis helps understand why:

```python
def analyze_failure(trace):
    # 1. Find the failing step
    for span in trace.spans:
        if span.status == "error":
            print(f"Failed at: {span.name}")
            print(f"Error: {span.error}")

    # 2. Check token usage
    for span in trace.spans:
        if span.tokens > 10000:
            print(f"High token usage at: {span.name} ({span.tokens})")

    # 3. Check latency
    for span in trace.spans:
        if span.latency_ms > 5000:
            print(f"Slow step: {span.name} ({span.latency_ms}ms)")

    # 4. Inspect decision points
    for span in trace.spans:
        if "tool_call" in span.name:
            print(f"Tool: {span.attributes.get('tool_name')}")
            print(f"Args: {span.attributes.get('tool_args')}")
```

## Interpretability Techniques

### Attention Analysis

For understanding what the model focuses on:

```python
# Requires model that exposes attention weights
# Most API models don't - local models only
from transformers import AutoModel

model = AutoModel.from_pretrained("model", output_attentions=True)
outputs = model(**inputs)
attention = outputs.attentions  # List of attention matrices
```

### Token Attribution

Understanding which input tokens influenced output:

```python
# SHAP-style attribution (approximate for LLMs)
def token_attribution(input_tokens, output):
    attributions = []
    for i, token in enumerate(input_tokens):
        # Mask token and measure output change
        masked_input = mask_token(input_tokens, i)
        masked_output = model(masked_input)
        importance = diff(output, masked_output)
        attributions.append((token, importance))
    return sorted(attributions, key=lambda x: -x[1])
```

## Trace Schema

Standard trace structure for evals:

```python
trace = {
    "trace_id": "uuid",
    "start_time": "2024-12-24T00:00:00Z",
    "end_time": "2024-12-24T00:00:01Z",
    "spans": [
        {
            "span_id": "uuid",
            "parent_span_id": null,
            "name": "agent",
            "start_time": "...",
            "end_time": "...",
            "attributes": {
                "input": "...",
                "output": "...",
                "tokens": 1500
            }
        },
        {
            "span_id": "uuid",
            "parent_span_id": "parent-uuid",
            "name": "tool_call",
            "attributes": {
                "tool_name": "search",
                "tool_args": {"query": "..."}
            }
        }
    ]
}
```

## Gotchas

| Trap | Fix |
|------|-----|
| Too much logging | Log decision points, not every token |
| Missing context | Include relevant input in spans |
| No baselines | Compare traces of success vs failure |
| Ignoring async | Trace async calls correctly |

## Tool Comparison

| Tool | Strengths | Weaknesses |
|------|-----------|------------|
| Phoenix | Visualization, spans | Requires instrumentation |
| Langfuse | SaaS, easy setup | Less customizable |
| OpenTelemetry | Standard, portable | More setup work |
| LangSmith | LangChain native | Vendor lock-in |
