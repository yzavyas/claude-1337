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

## OpenTelemetry for Agents

Instrument agents with OTel for local tracing.

### Setup (Python)

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

# Local console export (or use Phoenix)
provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("agent")
```

### Instrument Agent Loop

```python
def run_agent(task: str, max_steps: int = 10):
    with tracer.start_as_current_span("agent_run") as agent_span:
        agent_span.set_attribute("task", task)
        agent_span.set_attribute("max_steps", max_steps)

        messages = [{"role": "user", "content": task}]
        step = 0

        while step < max_steps:
            step += 1

            # Trace LLM call
            with tracer.start_as_current_span(f"llm_call_{step}") as llm_span:
                response = call_llm(messages)
                llm_span.set_attribute("input_tokens", response.usage.input)
                llm_span.set_attribute("output_tokens", response.usage.output)

            # Check for tool calls
            if response.tool_calls:
                for tool_call in response.tool_calls:
                    with tracer.start_as_current_span("tool_call") as tool_span:
                        tool_span.set_attribute("tool_name", tool_call.name)
                        tool_span.set_attribute("tool_args", str(tool_call.args))

                        result = execute_tool(tool_call)

                        tool_span.set_attribute("tool_result", str(result)[:500])
                        tool_span.set_attribute("success", not result.error)

                    messages.append({"role": "tool", "content": result})
            else:
                # Agent done
                agent_span.set_attribute("final_output", response.content[:500])
                agent_span.set_attribute("total_steps", step)
                return response.content

        agent_span.set_attribute("status", "max_steps_exceeded")
        return None
```

### Setup (TypeScript/Bun)

```typescript
import { trace } from "@opentelemetry/api";
import { NodeTracerProvider } from "@opentelemetry/sdk-trace-node";
import { SimpleSpanProcessor, ConsoleSpanExporter } from "@opentelemetry/sdk-trace-base";

const provider = new NodeTracerProvider();
provider.addSpanProcessor(new SimpleSpanProcessor(new ConsoleSpanExporter()));
provider.register();

const tracer = trace.getTracer("agent");

async function runAgent(task: string, maxSteps = 10) {
  return tracer.startActiveSpan("agent_run", async (agentSpan) => {
    agentSpan.setAttribute("task", task);
    let step = 0;

    while (step < maxSteps) {
      step++;

      const response = await tracer.startActiveSpan(`llm_call_${step}`, async (llmSpan) => {
        const res = await callLLM(messages);
        llmSpan.setAttribute("tokens", res.usage.total);
        llmSpan.end();
        return res;
      });

      if (response.toolCalls) {
        for (const toolCall of response.toolCalls) {
          await tracer.startActiveSpan("tool_call", async (toolSpan) => {
            toolSpan.setAttribute("tool_name", toolCall.name);
            const result = await executeTool(toolCall);
            toolSpan.setAttribute("success", !result.error);
            toolSpan.end();
          });
        }
      } else {
        agentSpan.setAttribute("total_steps", step);
        agentSpan.end();
        return response.content;
      }
    }
    agentSpan.end();
  });
}
```

### Phoenix Visualization

```python
import phoenix as px

# Launch local UI at localhost:6006
px.launch_app()

# Auto-instrument (works with OpenAI, Anthropic, etc.)
from openinference.instrumentation.openai import OpenAIInstrumentor
OpenAIInstrumentor().instrument()

# Or for Anthropic
from openinference.instrumentation.anthropic import AnthropicInstrumentor
AnthropicInstrumentor().instrument()

# Now run your agent - traces appear automatically
result = run_agent("Fix the bug in auth.py")
```

**Install:**
```bash
pip install arize-phoenix openinference-instrumentation-openai openinference-instrumentation-anthropic
```

### DeepEval Tracing

DeepEval has built-in tracing that works with their metrics:

```python
from deepeval.tracing import observe, Tracer

# Initialize local tracer
Tracer.init()

@observe(type="agent")
def my_agent(task):
    # Nested observations auto-captured
    docs = retrieve(task)
    return generate(task, docs)

@observe(type="retriever")
def retrieve(query):
    return search(query)

@observe(type="llm")
def generate(task, docs):
    return llm(task, docs)

# Run and get trace
result = my_agent("Fix the bug")
trace = Tracer.get_trace()
```

### What to Trace

| Span | Attributes |
|------|------------|
| `agent_run` | task, max_steps, total_steps, final_output |
| `llm_call` | model, input_tokens, output_tokens, latency_ms |
| `tool_call` | tool_name, tool_args, tool_result, success |
| `retrieve` | query, doc_count, latency_ms |
| `error` | error_type, error_message, stack_trace |

### Trace Analysis for Evals

```python
def analyze_agent_trace(trace):
    spans = trace.get_spans()

    metrics = {
        "total_steps": 0,
        "tool_calls": 0,
        "tool_failures": 0,
        "total_tokens": 0,
        "total_latency_ms": 0,
    }

    for span in spans:
        if span.name.startswith("llm_call"):
            metrics["total_steps"] += 1
            metrics["total_tokens"] += span.attributes.get("input_tokens", 0)
            metrics["total_tokens"] += span.attributes.get("output_tokens", 0)

        if span.name == "tool_call":
            metrics["tool_calls"] += 1
            if not span.attributes.get("success", True):
                metrics["tool_failures"] += 1

    metrics["tool_success_rate"] = (
        (metrics["tool_calls"] - metrics["tool_failures"]) / metrics["tool_calls"]
        if metrics["tool_calls"] > 0 else 1.0
    )

    return metrics
```

## Gotchas

| Trap | Fix |
|------|-----|
| Testing happy path only | Add failure cases, edge cases |
| Single run per test | 5+ runs (stochastic) |
| Task completion only | Add tool correctness, quality |
| Missing baseline | Compare against no-agent baseline |
| No tracing | Add OTel spans for debugging |
| Missing tool failures | Track success/failure per tool call |
