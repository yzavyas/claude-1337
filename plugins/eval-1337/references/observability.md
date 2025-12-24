# Observability and Interpretability

Tracing, debugging, and understanding agent behavior. All local, no cloud.

## What to Measure

| Metric | Question | Tool |
|--------|----------|------|
| Trace spans | What steps did the agent take? | Phoenix (local) |
| Latency breakdown | Where is time spent? | Phoenix |
| Token flow | How do tokens flow through? | OpenTelemetry |
| Decision points | Why did it make this choice? | Manual logging |

## Phoenix (Local)

[Phoenix](https://docs.arize.com/phoenix) runs entirely on your machine:

```python
import phoenix as px

# Launch local Phoenix UI (opens browser at localhost:6006)
session = px.launch_app()

# Instrument your agent
from openinference.instrumentation import instrument
instrument()

# Run your agent - traces appear in local UI
result = my_agent("input")

# Query traces programmatically
traces = px.Client().get_traces()
```

**Install:**
```bash
pip install arize-phoenix openinference-instrumentation
```

**Key Features:**
- Runs locally on localhost:6006
- Automatic trace collection
- Span visualization
- Latency breakdown
- Token usage per span
- No data leaves your machine

## OpenTelemetry (Standard)

Framework-agnostic tracing with OpenTelemetry:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

# Setup local exporter (console or file)
provider = TracerProvider()
processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

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

**Install:**
```bash
pip install opentelemetry-sdk opentelemetry-exporter-otlp
```

## TypeScript: OpenTelemetry

```typescript
import { trace } from "@opentelemetry/api";
import { NodeTracerProvider } from "@opentelemetry/sdk-trace-node";
import { SimpleSpanProcessor, ConsoleSpanExporter } from "@opentelemetry/sdk-trace-base";

const provider = new NodeTracerProvider();
provider.addSpanProcessor(new SimpleSpanProcessor(new ConsoleSpanExporter()));
provider.register();

const tracer = trace.getTracer("agent-eval");

async function myAgent(input: string) {
  return tracer.startActiveSpan("agent", async (span) => {
    span.setAttribute("input", input);

    const docs = await tracer.startActiveSpan("retrieve", async (retrieveSpan) => {
      const result = await retrieve(input);
      retrieveSpan.setAttribute("doc_count", result.length);
      retrieveSpan.end();
      return result;
    });

    const output = await tracer.startActiveSpan("generate", async (genSpan) => {
      const result = await generate(input, docs);
      genSpan.setAttribute("output_length", result.length);
      genSpan.end();
      return result;
    });

    span.setAttribute("output", output);
    span.end();
    return output;
  });
}
```

**Install:**
```bash
bun add @opentelemetry/api @opentelemetry/sdk-trace-node @opentelemetry/sdk-trace-base
```

## File-Based Tracing (Minimal)

Simplest local tracing - JSON to file:

```python
import json
import time
from pathlib import Path

TRACE_DIR = Path("./traces")
TRACE_DIR.mkdir(exist_ok=True)

def trace_agent(func):
    def wrapper(input):
        trace = {
            "input": input,
            "start_time": time.time(),
            "spans": []
        }

        result = func(input, trace)

        trace["end_time"] = time.time()
        trace["output"] = result
        trace["duration_ms"] = (trace["end_time"] - trace["start_time"]) * 1000

        # Save to local file
        trace_file = TRACE_DIR / f"trace_{int(time.time())}.json"
        trace_file.write_text(json.dumps(trace, indent=2))

        return result
    return wrapper

@trace_agent
def my_agent(input, trace):
    # Add spans manually
    trace["spans"].append({"name": "retrieve", "start": time.time()})
    docs = retrieve(input)
    trace["spans"][-1]["end"] = time.time()

    return generate(input, docs)
```

## Debugging Failed Evals

When an eval fails, trace analysis helps understand why:

```python
def analyze_failure(trace):
    # 1. Find the failing step
    for span in trace["spans"]:
        if span.get("status") == "error":
            print(f"Failed at: {span['name']}")
            print(f"Error: {span.get('error')}")

    # 2. Check token usage
    for span in trace["spans"]:
        tokens = span.get("tokens", 0)
        if tokens > 10000:
            print(f"High token usage at: {span['name']} ({tokens})")

    # 3. Check latency
    for span in trace["spans"]:
        latency = span.get("end", 0) - span.get("start", 0)
        if latency > 5:
            print(f"Slow step: {span['name']} ({latency*1000:.0f}ms)")

    # 4. Inspect decision points
    for span in trace["spans"]:
        if "tool_call" in span.get("name", ""):
            print(f"Tool: {span.get('tool_name')}")
            print(f"Args: {span.get('tool_args')}")
```

## Interpretability Techniques

### Attention Analysis (Local Models)

For understanding what the model focuses on:

```python
# Requires local model that exposes attention weights
# API models don't expose this
from transformers import AutoModel

model = AutoModel.from_pretrained("model", output_attentions=True)
outputs = model(**inputs)
attention = outputs.attentions  # List of attention matrices
```

### Token Attribution

Understanding which input tokens influenced output:

```python
# SHAP-style attribution (approximate for LLMs)
def token_attribution(input_tokens, output, model):
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
            "parent_span_id": None,
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

| Tool | Local | Strengths |
|------|-------|-----------|
| **Phoenix** | Yes | UI, visualization, LLM-native |
| **OpenTelemetry** | Yes | Standard, portable, any backend |
| **File logging** | Yes | Zero deps, full control |
| Jaeger | Yes | Mature, battle-tested |
