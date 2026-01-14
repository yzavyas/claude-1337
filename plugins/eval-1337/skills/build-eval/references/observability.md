# Analyzing Traces for Evaluation

Use observability data to assess agent behavior. This guide focuses on ANALYSIS — reading and extracting metrics from traces. For building observable extensions, see `extension-builder/references/observability.md`.

## Why Traces for Assessments

Traces provide ground truth about what actually happened:
- **What tools were called** (not just what was output)
- **Token usage** (cost and efficiency)
- **Timing** (latency bottlenecks)
- **Error patterns** (where failures occur)
- **Decision paths** (multi-step reasoning)

---

## Key Spans to Analyze

### Agent Assessment

| Span | Extract | Use |
|------|---------|-----|
| `agent_run` | total_steps, success | Task completion rate |
| `llm_call` | input_tokens, output_tokens | Cost efficiency |
| `tool_call` | tool_name, success, duration | Tool correctness |

```python
def extract_agent_metrics(trace):
    agent_spans = [s for s in trace.spans if s.name == "agent_run"]

    return {
        "task_completed": agent_spans[0].attributes.get("success", False),
        "total_steps": agent_spans[0].attributes.get("total_steps", 0),
        "total_tokens": sum(
            s.attributes.get("gen_ai.usage.input_tokens", 0) +
            s.attributes.get("gen_ai.usage.output_tokens", 0)
            for s in trace.spans if s.name == "llm_call"
        ),
        "tool_calls": [
            {
                "name": s.attributes.get("gen_ai.tool.name"),
                "success": s.attributes.get("success"),
                "duration_ms": s.duration_ms
            }
            for s in trace.spans if s.name == "tool_call"
        ]
    }
```

### Skill Assessment

| Span | Extract | Use |
|------|---------|-----|
| `skill_check` | activation_count | Over/under-activation |
| `skill_match` | skill_name, activated | Precision/recall |
| `skill_load` | load_time_ms | Performance |

```python
def extract_skill_metrics(traces, ground_truth):
    """
    ground_truth: dict mapping prompt -> expected_skills (list)
    """
    results = []

    for trace in traces:
        prompt = trace.attributes.get("prompt", "")
        expected = set(ground_truth.get(prompt, []))

        activated = set()
        for span in trace.spans:
            if span.name == "skill_match" and span.attributes.get("activated"):
                activated.add(span.attributes.get("skill_name"))

        tp = len(activated & expected)
        fp = len(activated - expected)
        fn = len(expected - activated)

        results.append({
            "prompt": prompt,
            "expected": list(expected),
            "activated": list(activated),
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn
        })

    return results
```

### MCP Server Assessment

| Span | Extract | Use |
|------|---------|-----|
| `mcp_server` | server_name | Server availability |
| `mcp_discover` | tool_count | Schema correctness |
| `mcp_call` | success, duration_ms | Reliability |

---

## Drift Detection

Track behavioral changes over time by comparing trace metrics against baselines.

```python
import json
from pathlib import Path
from statistics import mean, stdev

BASELINE_FILE = Path("./baselines.json")

def record_baseline(metric_name: str, value: float):
    """Update rolling baseline from recent observations."""
    baselines = json.loads(BASELINE_FILE.read_text()) if BASELINE_FILE.exists() else {}

    if metric_name not in baselines:
        baselines[metric_name] = {"values": [], "mean": 0, "std": 0}

    baselines[metric_name]["values"].append(value)
    values = baselines[metric_name]["values"][-100:]  # Keep last 100
    baselines[metric_name]["mean"] = mean(values)
    baselines[metric_name]["std"] = stdev(values) if len(values) > 1 else 0

    BASELINE_FILE.write_text(json.dumps(baselines, indent=2))

def check_drift(metric_name: str, current_value: float, threshold_std: float = 2.0):
    """Check if current value has drifted from baseline."""
    baselines = json.loads(BASELINE_FILE.read_text())

    if metric_name not in baselines:
        return False, "no baseline"

    baseline = baselines[metric_name]
    if baseline["std"] == 0:
        return False, "insufficient data"

    z_score = abs(current_value - baseline["mean"]) / baseline["std"]

    if z_score > threshold_std:
        return True, f"drift detected: z={z_score:.2f} (value={current_value}, baseline={baseline['mean']:.2f})"
    return False, f"within bounds: z={z_score:.2f}"
```

### Using Drift Detection in Assessments

```python
def assess_with_drift_check(test_cases):
    """Run assessment and check for drift on key metrics."""
    results = run_assessment(test_cases)

    metrics_to_track = [
        ("accuracy", results["accuracy"]),
        ("avg_latency_ms", results["avg_latency_ms"]),
        ("avg_tokens", results["avg_tokens"]),
        ("tool_call_success_rate", results["tool_success_rate"])
    ]

    drift_warnings = []
    for metric_name, value in metrics_to_track:
        drifted, msg = check_drift(metric_name, value)
        if drifted:
            drift_warnings.append(f"WARNING: {metric_name} {msg}")
        record_baseline(metric_name, value)

    return results, drift_warnings
```

---

## Phoenix Integration

Use Phoenix's assessment library to analyze traces locally.

### Setup

```bash
pip install arize-phoenix arize-phoenix-evals
```

```python
import phoenix as px
px.launch_app()  # localhost:6006

from phoenix.evals import llm_classify, OpenAIModel
```

### Response Quality Assessment

```python
from phoenix.evals import llm_classify

def assess_response_quality(responses: list[dict]):
    """Assess response quality using LLM-as-judge."""
    import pandas as pd

    assessment_model = OpenAIModel(model="gpt-4o-mini")

    results = llm_classify(
        dataframe=pd.DataFrame(responses),
        template="Is this response helpful and accurate? {response}",
        model=assessment_model,
        rails=["helpful", "unhelpful"],
    )
    return results
```

### RAG Relevance Assessment

```python
from phoenix.evals import run_relevance_eval

def assess_retrieval_relevance(queries_and_docs):
    """Assess if retrieved docs are relevant to queries."""
    import pandas as pd

    assessment_model = OpenAIModel(model="gpt-4o-mini")

    relevance_scores = run_relevance_eval(
        dataframe=pd.DataFrame(queries_and_docs),
        model=assessment_model,
        query_column="query",
        document_column="retrieved_doc",
    )
    return relevance_scores
```

---

## Extracting Metrics from Traces

### Token Efficiency

```python
def analyze_token_efficiency(traces):
    """Analyze token usage patterns."""
    token_data = []

    for trace in traces:
        for span in trace.spans:
            if span.name == "llm_call":
                input_tokens = span.attributes.get("gen_ai.usage.input_tokens", 0)
                output_tokens = span.attributes.get("gen_ai.usage.output_tokens", 0)
                token_data.append({
                    "trace_id": trace.trace_id,
                    "step": span.attributes.get("step"),
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total": input_tokens + output_tokens
                })

    return {
        "total_tokens": sum(d["total"] for d in token_data),
        "avg_per_call": mean(d["total"] for d in token_data) if token_data else 0,
        "max_single_call": max((d["total"] for d in token_data), default=0),
        "calls_count": len(token_data)
    }
```

### Tool Usage Patterns

```python
def analyze_tool_usage(traces):
    """Analyze tool call patterns for correctness assessment."""
    tool_calls = []

    for trace in traces:
        for span in trace.spans:
            if span.name == "tool_call":
                tool_calls.append({
                    "trace_id": trace.trace_id,
                    "tool_name": span.attributes.get("gen_ai.tool.name"),
                    "success": span.attributes.get("success"),
                    "duration_ms": span.duration_ms,
                    "error": span.attributes.get("error_type")
                })

    # Group by tool
    by_tool = {}
    for call in tool_calls:
        name = call["tool_name"]
        if name not in by_tool:
            by_tool[name] = {"total": 0, "success": 0, "durations": []}
        by_tool[name]["total"] += 1
        if call["success"]:
            by_tool[name]["success"] += 1
        by_tool[name]["durations"].append(call["duration_ms"])

    return {
        name: {
            "call_count": data["total"],
            "success_rate": data["success"] / data["total"] if data["total"] > 0 else 0,
            "avg_duration_ms": mean(data["durations"]) if data["durations"] else 0
        }
        for name, data in by_tool.items()
    }
```

### Latency Analysis

```python
def analyze_latency(traces):
    """Analyze latency distribution."""
    latencies = []

    for trace in traces:
        agent_spans = [s for s in trace.spans if s.name == "agent_run"]
        if agent_spans:
            latencies.append(agent_spans[0].duration_ms)

    if not latencies:
        return {}

    sorted_latencies = sorted(latencies)
    n = len(sorted_latencies)

    return {
        "p50": sorted_latencies[n // 2],
        "p90": sorted_latencies[int(n * 0.9)],
        "p99": sorted_latencies[int(n * 0.99)] if n > 100 else sorted_latencies[-1],
        "min": sorted_latencies[0],
        "max": sorted_latencies[-1],
        "mean": mean(sorted_latencies)
    }
```

---

## Connecting to Trace Sources

### From Phoenix

```python
import phoenix as px
from datetime import datetime, timedelta

# Get traces from Phoenix
client = px.Client()
traces = client.get_trace_data(
    project_name="my-agent",
    start_time=datetime.now() - timedelta(hours=24)
)
```

### From OTLP Collector

```python
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from opentelemetry.sdk.trace import ReadableSpan

class AssessmentCollector(SpanExporter):
    """Collect spans for assessment."""

    def __init__(self):
        self.spans = []

    def export(self, spans: list[ReadableSpan]):
        self.spans.extend(spans)
        return SpanExportResult.SUCCESS

    def get_traces(self):
        # Group spans by trace_id
        by_trace = {}
        for span in self.spans:
            tid = span.context.trace_id
            if tid not in by_trace:
                by_trace[tid] = []
            by_trace[tid].append(span)
        return by_trace
```

### From JSON Logs

```python
def load_traces_from_logs(log_dir: Path):
    """Load traces from JSON log files."""
    traces = []

    for log_file in log_dir.glob("*.json"):
        with open(log_file) as f:
            for line in f:
                event = json.loads(line)
                traces.append(event)

    return traces
```

---

## Unified Trace Schema

Standard schema for analysis:

```python
trace = {
    "trace_id": "uuid",
    "start_time": "2026-01-10T00:00:00Z",
    "end_time": "2026-01-10T00:00:01Z",
    "success": True,
    "spans": [
        {
            "span_id": "uuid",
            "parent_span_id": None,
            "name": "agent_run",
            "start_time": "...",
            "end_time": "...",
            "duration_ms": 1234,
            "attributes": {
                "task": "...",
                "total_steps": 5,
                "success": True
            }
        }
    ],
    "metrics": {
        "total_tokens": 1500,
        "latency_ms": 2340,
        "tool_calls": 3,
        "errors": 0
    }
}
```

---

## Sources

- [Phoenix](https://docs.arize.com/phoenix) - Local LLM observability UI
- [Phoenix Assessments](https://docs.arize.com/phoenix/evaluation) - LLM assessment library
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/) - Trace data structures
- [Anthropic Agent Assessment Guide](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) - Agent assessment best practices
