# OpenTelemetry for Claude Code Plugins

Instrument every plugin type with OTel. All local, no cloud.

## Quick Setup

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("claude-plugin")
```

Or with Phoenix UI:
```python
import phoenix as px
px.launch_app()  # localhost:6006

from openinference.instrumentation.anthropic import AnthropicInstrumentor
AnthropicInstrumentor().instrument()
```

## Plugin Type: Skills

Skills are triggered by user prompts. Trace activation and content loading.

```python
# Skill activation tracing
def trace_skill_activation(prompt: str, skills: list[Skill]):
    with tracer.start_as_current_span("skill_check") as span:
        span.set_attribute("prompt", prompt[:200])
        span.set_attribute("available_skills", len(skills))

        activated = []
        for skill in skills:
            with tracer.start_as_current_span("skill_match") as skill_span:
                skill_span.set_attribute("skill_name", skill.name)
                matches = skill.matches(prompt)
                skill_span.set_attribute("activated", matches)
                if matches:
                    activated.append(skill.name)

        span.set_attribute("activated_skills", activated)
        span.set_attribute("activation_count", len(activated))
        return activated
```

**Key spans:**
| Span | Attributes |
|------|------------|
| `skill_check` | prompt, available_skills, activation_count |
| `skill_match` | skill_name, activated, match_score |
| `skill_load` | skill_name, content_size, load_time_ms |

**Metrics to extract:**
- Activation rate per skill
- False positive rate (activated but not used)
- Content load latency

## Plugin Type: Agents

Agents are autonomous task executors. Trace the full loop.

```python
def run_agent(task: str):
    with tracer.start_as_current_span("agent") as agent_span:
        agent_span.set_attribute("task", task)
        agent_span.set_attribute("agent_type", "task_executor")

        step = 0
        while not done:
            step += 1

            # LLM call
            with tracer.start_as_current_span(f"llm_call") as llm_span:
                llm_span.set_attribute("step", step)
                response = call_llm(messages)
                llm_span.set_attribute("input_tokens", response.usage.input)
                llm_span.set_attribute("output_tokens", response.usage.output)
                llm_span.set_attribute("model", response.model)

            # Tool calls
            for tool_call in response.tool_calls:
                with tracer.start_as_current_span("tool_call") as tool_span:
                    tool_span.set_attribute("tool_name", tool_call.name)
                    tool_span.set_attribute("tool_args", str(tool_call.args)[:500])

                    result = execute_tool(tool_call)

                    tool_span.set_attribute("success", not result.error)
                    tool_span.set_attribute("result_size", len(str(result)))

        agent_span.set_attribute("total_steps", step)
        agent_span.set_attribute("success", True)
```

**Key spans:**
| Span | Attributes |
|------|------------|
| `agent` | task, agent_type, total_steps, success |
| `llm_call` | step, model, input_tokens, output_tokens |
| `tool_call` | tool_name, tool_args, success, result_size |

## Plugin Type: Commands

Slash commands are user-invoked actions. Trace invocation and execution.

```python
def execute_command(command: str, args: list[str]):
    with tracer.start_as_current_span("command") as span:
        span.set_attribute("command_name", command)
        span.set_attribute("arg_count", len(args))

        # Parse phase
        with tracer.start_as_current_span("command_parse") as parse_span:
            parsed = parse_args(args)
            parse_span.set_attribute("valid", parsed.valid)

        # Execute phase
        with tracer.start_as_current_span("command_execute") as exec_span:
            result = run_command(command, parsed)
            exec_span.set_attribute("success", result.success)
            exec_span.set_attribute("output_size", len(result.output))

        span.set_attribute("total_time_ms", elapsed_ms())
        return result
```

**Key spans:**
| Span | Attributes |
|------|------------|
| `command` | command_name, arg_count, total_time_ms |
| `command_parse` | valid, error_message |
| `command_execute` | success, output_size |

## Plugin Type: Hooks

Hooks are event-triggered callbacks. Trace the event and handler.

```python
def trigger_hook(event: str, payload: dict):
    with tracer.start_as_current_span("hook_trigger") as span:
        span.set_attribute("event_type", event)
        span.set_attribute("payload_size", len(str(payload)))

        handlers = get_handlers(event)
        span.set_attribute("handler_count", len(handlers))

        results = []
        for handler in handlers:
            with tracer.start_as_current_span("hook_handler") as handler_span:
                handler_span.set_attribute("handler_name", handler.name)
                handler_span.set_attribute("hook_type", handler.type)

                try:
                    result = handler.execute(payload)
                    handler_span.set_attribute("success", True)
                    handler_span.set_attribute("modified", result.modified)
                except Exception as e:
                    handler_span.set_attribute("success", False)
                    handler_span.set_attribute("error", str(e))
                    handler_span.record_exception(e)

                results.append(result)

        span.set_attribute("handlers_succeeded", sum(r.success for r in results))
        return results
```

**Hook event types:**
| Event | Payload |
|-------|---------|
| `PreToolUse` | tool_name, tool_input |
| `PostToolUse` | tool_name, tool_result |
| `Notification` | message, level |
| `Stop` | reason |

**Key spans:**
| Span | Attributes |
|------|------------|
| `hook_trigger` | event_type, handler_count, handlers_succeeded |
| `hook_handler` | handler_name, hook_type, success, modified |

## Plugin Type: MCP Servers

MCP servers expose tools to agents. Trace tool registration and calls.

```python
def trace_mcp_server(server: MCPServer):
    with tracer.start_as_current_span("mcp_server") as span:
        span.set_attribute("server_name", server.name)
        span.set_attribute("server_url", server.url)

        # Tool discovery
        with tracer.start_as_current_span("mcp_discover") as discover_span:
            tools = server.list_tools()
            discover_span.set_attribute("tool_count", len(tools))
            discover_span.set_attribute("tool_names", [t.name for t in tools])

        return tools

def trace_mcp_call(server: str, tool: str, args: dict):
    with tracer.start_as_current_span("mcp_call") as span:
        span.set_attribute("server_name", server)
        span.set_attribute("tool_name", tool)
        span.set_attribute("args", str(args)[:500])

        try:
            result = call_mcp_tool(server, tool, args)
            span.set_attribute("success", True)
            span.set_attribute("result_size", len(str(result)))
        except Exception as e:
            span.set_attribute("success", False)
            span.set_attribute("error_type", type(e).__name__)
            span.set_attribute("error_message", str(e))
            span.record_exception(e)
            raise

        return result
```

**Key spans:**
| Span | Attributes |
|------|------------|
| `mcp_server` | server_name, server_url |
| `mcp_discover` | tool_count, tool_names |
| `mcp_call` | server_name, tool_name, args, success, result_size |

## Claude Agent SDK Native Tracing

Enable built-in OTel:
```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

**Events emitted:**
| Event | Description |
|-------|-------------|
| `claude_code.user_prompt` | User submits prompt |
| `claude_code.tool_result` | Tool completes |
| `claude_code.api_request` | API call made |
| `claude_code.api_error` | API call failed |
| `claude_code.tool_decision` | Permission decision |

**SDK hooks for custom tracing:**
```python
from claude_code import hooks

@hooks.on_tool_call
def trace_tool(tool_name, tool_input):
    with tracer.start_as_current_span("sdk_tool_call") as span:
        span.set_attribute("tool_name", tool_name)
        # SDK handles the rest
```

## Google ADK Native Tracing

Enable built-in OTel:
```python
from google.adk import AdkApp

app = AdkApp(enable_tracing=True)
```

Or with CLI:
```bash
adk deploy agent_engine --trace_to_cloud
```

**Spans emitted:**
| Span | Description |
|------|-------------|
| `invocation` | Full agent invocation |
| `agent_run` | Agent execution loop |
| `call_llm` | LLM API call |
| `execute_tool` | Tool execution |

**Route to Phoenix locally:**
```python
import phoenix as px
px.launch_app()

from google.adk import AdkApp
app = AdkApp(enable_tracing=True)
# Traces appear in Phoenix UI
```

## Session-Level Tracing

For multi-turn conversations, wrap at session level:

```python
def start_session(user_id: str):
    session_span = tracer.start_span("session")
    session_span.set_attribute("user_id", user_id)
    session_span.set_attribute("session_id", generate_id())
    return session_span

def trace_turn(session_span, user_input: str):
    with tracer.start_as_current_span("turn", parent=session_span) as turn_span:
        turn_span.set_attribute("user_input", user_input[:200])

        # Agent processes turn
        response = agent.run(user_input)

        turn_span.set_attribute("response", response[:200])
        turn_span.set_attribute("turn_tokens", response.usage.total)

    return response

def end_session(session_span, outcome: str):
    session_span.set_attribute("outcome", outcome)
    session_span.set_attribute("total_turns", turn_count)
    session_span.end()
```

**Session metrics:**
| Metric | Description |
|--------|-------------|
| `total_turns` | Conversation length |
| `total_tokens` | All tokens in session |
| `outcome` | success, abandoned, error |
| `session_duration_ms` | Wall clock time |

## Drift Detection

Track behavioral changes over time:

```python
from collections import defaultdict
import json
from pathlib import Path

BASELINE_FILE = Path("./baselines.json")

def record_baseline(metric_name: str, value: float):
    baselines = json.loads(BASELINE_FILE.read_text()) if BASELINE_FILE.exists() else {}
    if metric_name not in baselines:
        baselines[metric_name] = {"values": [], "mean": 0, "std": 0}

    baselines[metric_name]["values"].append(value)
    values = baselines[metric_name]["values"][-100:]  # Keep last 100
    baselines[metric_name]["mean"] = sum(values) / len(values)
    baselines[metric_name]["std"] = std_dev(values)

    BASELINE_FILE.write_text(json.dumps(baselines, indent=2))

def check_drift(metric_name: str, current_value: float, threshold_std: float = 2.0):
    baselines = json.loads(BASELINE_FILE.read_text())
    if metric_name not in baselines:
        return False, "no baseline"

    baseline = baselines[metric_name]
    z_score = abs(current_value - baseline["mean"]) / baseline["std"]

    if z_score > threshold_std:
        return True, f"drift detected: z={z_score:.2f}"
    return False, f"within bounds: z={z_score:.2f}"

# Usage in eval
def eval_with_drift_check(test_cases):
    results = run_eval(test_cases)

    # Check for drift
    metrics = ["accuracy", "latency_p50", "token_usage"]
    for metric in metrics:
        drifted, msg = check_drift(metric, results[metric])
        if drifted:
            print(f"WARNING: {metric} {msg}")

        # Update baseline
        record_baseline(metric, results[metric])

    return results
```

## Phoenix Evals Integration

Use Phoenix's eval library locally:

```python
from phoenix.evals import llm_classify, OpenAIModel

# Local eval model (or use Anthropic)
eval_model = OpenAIModel(model="gpt-4o-mini")

# Evaluate responses
def eval_response_quality(responses: list[dict]):
    results = llm_classify(
        dataframe=pd.DataFrame(responses),
        template="Is this response helpful and accurate? {response}",
        model=eval_model,
        rails=["helpful", "unhelpful"],
    )
    return results

# RAG relevance eval
from phoenix.evals import run_relevance_eval

relevance_scores = run_relevance_eval(
    dataframe=df,
    model=eval_model,
    query_column="query",
    document_column="retrieved_doc",
)
```

**Install:**
```bash
pip install arize-phoenix-evals
```

## Unified Trace Schema

Standard schema for all plugin types:

```python
trace = {
    "trace_id": "uuid",
    "plugin_type": "skill|agent|command|hook|mcp",
    "plugin_name": "my-plugin",
    "start_time": "2024-12-25T00:00:00Z",
    "end_time": "2024-12-25T00:00:01Z",
    "success": True,
    "spans": [
        {
            "span_id": "uuid",
            "parent_span_id": None,
            "name": "agent_run",
            "attributes": {...}
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

## Gotchas

| Trap | Fix |
|------|-----|
| Missing parent spans | Always set parent for nested spans |
| Attribute size limits | Truncate large values (500 chars) |
| Not ending spans | Use context managers or try/finally |
| Missing errors | Always record_exception() on failures |
| No session correlation | Pass session_id through all spans |

## Sources

- [OpenTelemetry](https://opentelemetry.io/) - Official specification and SDKs
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/) - Python SDK docs
- [OpenTelemetry JS](https://opentelemetry.io/docs/languages/js/) - Node/Bun SDK docs
- [OpenInference](https://github.com/Arize-ai/openinference) - LLM-specific instrumentation
- [Phoenix](https://docs.arize.com/phoenix) - Local LLM observability UI
- [Claude Code Monitoring](https://code.claude.com/docs/en/monitoring-usage) - Native OTel support
- [Google ADK Tracing](https://google.github.io/adk-docs/observability/cloud-trace/) - Native OTel support
- [AI Agent Observability](https://opentelemetry.io/blog/2025/ai-agent-observability/) - OTel semantic conventions
