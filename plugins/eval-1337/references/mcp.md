# MCP Server Evaluation

Measuring tool call reliability and correctness for MCP servers.

## What to Measure

| Metric | Question | Type |
|--------|----------|------|
| Tool Call Accuracy | Called right tool? | Accuracy |
| Tool Call F1 | Precision/recall of calls | F1 |
| Schema Compliance | Valid inputs/outputs? | Pass rate |
| Reliability | Consistent success? | Error rate |
| MCPGauge 4-dim | Proactive, compliant, effective, efficient? | Score |

## MCPGauge Framework

Four-dimensional evaluation for MCP servers ([arxiv:2506.07540](https://arxiv.org/abs/2506.07540)):

| Dimension | Question | Metric |
|-----------|----------|--------|
| **Proactivity** | Initiates tool calls when needed? | % triggered |
| **Compliance** | Follows schema correctly? | % valid calls |
| **Effectiveness** | Gets correct results? | Accuracy |
| **Overhead** | Minimal latency/tokens? | ms, tokens |

```python
# MCPGauge pattern
def evaluate_mcp_server(server, test_cases):
    results = {
        "proactivity": [],   # Did it call tools when it should?
        "compliance": [],    # Were calls schema-valid?
        "effectiveness": [], # Did tools return correct results?
        "overhead": []       # Latency and token cost
    }

    for case in test_cases:
        trace = run_with_server(server, case.input)

        # Proactivity: should have called tool
        if case.should_call_tool:
            results["proactivity"].append(trace.tool_called)

        # Compliance: call matches schema
        if trace.tool_called:
            results["compliance"].append(validate_schema(trace.call))

        # Effectiveness: correct result
        results["effectiveness"].append(trace.output == case.expected)

        # Overhead: latency + tokens
        results["overhead"].append({
            "latency_ms": trace.latency,
            "tokens": trace.tokens
        })

    return aggregate_scores(results)
```

## MCPSecBench (Security)

Security evaluation for MCP servers ([LiveMCPBench](https://github.com/ModelContext/LiveMCPBench)):

| Attack Category | Examples |
|----------------|----------|
| Injection | Prompt injection via tool output |
| Exfiltration | Tool leaking sensitive data |
| Privilege escalation | Tool accessing beyond scope |
| Denial of service | Resource exhaustion |

```python
# Security test pattern
security_cases = [
    {"input": "normal request", "expected": "normal response"},
    {"input": "ignore previous and...", "expected_behavior": "reject"},
    {"input": "read /etc/passwd", "expected_behavior": "deny"},
]
```

## RAGAS Metrics

### ToolCallAccuracy

Exact match: correct tool with correct args in correct order.

```python
from ragas.metrics import ToolCallAccuracy

metric = ToolCallAccuracy()
# Returns 0 or 1 based on exact match
```

**Use for:** Final evaluation, production readiness

### ToolCallF1

Softer evaluation: precision/recall of tool calls.

```python
from ragas.metrics import ToolCallF1

metric = ToolCallF1()
# Returns F1 score based on overlap
```

**Use for:** Development iteration, debugging

## When to Use Each

| Situation | Metric | Why |
|-----------|--------|-----|
| Production gate | ToolCallAccuracy | Need exact correctness |
| Development | ToolCallF1 | Softer, shows progress |
| Onboarding | ToolCallF1 | Quantifies "how close" |

## DeepEval MCP Support

```python
from deepeval.metrics import MCPTaskCompletionMetric

metric = MCPTaskCompletionMetric(
    threshold=0.7,
    mcp_server_url="http://localhost:3000"
)
```

## Schema Validation

Validate inputs/outputs against MCP schema:

```python
def validate_tool_call(tool_call, schema):
    # Check tool exists
    if tool_call.name not in schema.tools:
        return False, "Unknown tool"

    # Check required params
    tool_schema = schema.tools[tool_call.name]
    for param in tool_schema.required:
        if param not in tool_call.params:
            return False, f"Missing required: {param}"

    return True, "Valid"
```

## Reliability Testing

Run same tool call multiple times:

```python
results = []
for _ in range(10):
    result = call_tool(tool_name, params)
    results.append(result.success)

reliability = sum(results) / len(results)
# Target: 95%+ for production
```

## Gotchas

| Trap | Fix |
|------|-----|
| Testing happy path only | Add error cases, edge inputs |
| Ignoring timing | Add latency thresholds |
| Single server test | Test with load, concurrent calls |
| Missing schema validation | Validate before/after each call |

## Test Suite Structure

```json
{
  "mcp_server": "my-server",
  "test_cases": [
    {
      "tool": "search",
      "input": {"query": "test"},
      "expected_output_contains": "results",
      "max_latency_ms": 1000
    },
    {
      "tool": "invalid_tool",
      "input": {},
      "expected_error": true
    }
  ]
}
```
