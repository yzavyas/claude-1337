# Observability for Claude Code Extensions

Make extension behavior measurable, debuggable, and controllable. No cloud required.

## Why Observability Matters

Extensions become part of how users think and work. Without observability:
- You can't debug when things go wrong
- You can't measure if changes help or hurt
- Users can't understand what's happening

**The goal**: Every extension should emit structured telemetry that answers:
- What happened?
- How long did it take?
- Did it succeed?
- Why did it fail?

---

## Claude Code Native Telemetry

Claude Code has built-in OpenTelemetry support. Enable it with environment variables:

```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

**Events emitted natively:**

| Event | Description |
|-------|-------------|
| `claude_code.user_prompt` | User submits prompt |
| `claude_code.tool_result` | Tool completes |
| `claude_code.api_request` | API call made |
| `claude_code.api_error` | API call failed |
| `claude_code.tool_decision` | Permission decision |

**Architecture insight:** Claude Agent SDK uses IPC/WebSocket to communicate with Claude Code CLI, not direct HTTP to api.anthropic.com. Traditional HTTP monitoring tools are blind to this layer — you need hook-based or SDK-level observability.

---

## Hook-Based Observability

The most flexible approach for Claude Code plugins. Use hooks to capture events in real-time.

### Configuration

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "",
      "hooks": [
        { "type": "command", "command": "python .claude/hooks/pre_tool_use.py" },
        { "type": "command", "command": "python .claude/hooks/send_event.py --event-type PreToolUse" }
      ]
    }],
    "PostToolUse": [{
      "matcher": "",
      "hooks": [
        { "type": "command", "command": "python .claude/hooks/post_tool_use.py" },
        { "type": "command", "command": "python .claude/hooks/send_event.py --event-type PostToolUse" }
      ]
    }]
  }
}
```

### Hook Events

| Event | When | Payload |
|-------|------|---------|
| `PreToolUse` | Before tool execution | tool_name, tool_input |
| `PostToolUse` | After tool success | tool_name, tool_result |
| `Stop` | Session ends | reason |
| `SubagentStop` | Subagent completes | agent_id, result |
| `UserPromptSubmit` | User sends prompt | prompt |
| `SessionStart` | Session begins | config |
| `Notification` | Alert raised | message, level |

### Hook Observer Pattern

```python
#!/usr/bin/env python3
"""Hook observer that emits OTel spans for Claude Code events."""
import json
import sys
from datetime import datetime
from opentelemetry import trace

tracer = trace.get_tracer("claude-code-hooks")

def observe_hook(event_type: str, payload: dict):
    with tracer.start_as_current_span(f"hook_{event_type.lower()}") as span:
        span.set_attribute("event_type", event_type)
        span.set_attribute("timestamp", datetime.utcnow().isoformat())

        if event_type == "PreToolUse":
            span.set_attribute("tool_name", payload.get("tool_name", ""))
            span.set_attribute("tool_input_size", len(str(payload.get("tool_input", ""))))
        elif event_type == "PostToolUse":
            span.set_attribute("tool_name", payload.get("tool_name", ""))
            span.set_attribute("success", not payload.get("error"))
            span.set_attribute("result_size", len(str(payload.get("tool_result", ""))))

        # Always output valid JSON for Claude Code
        print(json.dumps({"continue": True}))

if __name__ == "__main__":
    payload = json.loads(sys.stdin.read())
    event_type = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
    observe_hook(event_type, payload)
```

---

## OpenTelemetry Implementation

OTel is the recommended implementation for structured telemetry.

### Quick Setup

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("my-extension")
```

### Local UI with Phoenix

```python
import phoenix as px
px.launch_app()  # localhost:6006

from openinference.instrumentation.anthropic import AnthropicInstrumentor
AnthropicInstrumentor().instrument()
```

### GenAI Semantic Conventions

Use OTel's standardized attribute names (v1.37+) for vendor interoperability:

| Attribute | Description | Example |
|-----------|-------------|---------|
| `gen_ai.system` | Provider | `anthropic` |
| `gen_ai.request.model` | Model ID | `claude-sonnet-4-20250514` |
| `gen_ai.usage.input_tokens` | Input tokens | `1500` |
| `gen_ai.usage.output_tokens` | Output tokens | `500` |
| `gen_ai.tool.name` | Tool/function name | `read_file` |
| `gen_ai.tool.call.id` | Unique call identifier | `call_abc123` |
| `gen_ai.response.finish_reason` | Why stopped | `stop`, `max_tokens` |

### Cardinality Guidelines

**Default limit:** OTel has a cardinality limit of 2000 per metric.

| Attribute Type | Where | Why |
|----------------|-------|-----|
| Low cardinality (http.method, tool_name) | Metrics | Safe for aggregation |
| High cardinality (user_id, trace_id) | Spans/logs only | Avoid metric explosion |
| Unbounded (prompt text, full response) | Truncate to 500 chars | Attribute size limits |

**Rule:** High-cardinality details belong in span attributes, not metric labels.

---

## Instrumentation by Extension Type

### Skills

Skills are triggered by user prompts. Trace activation and content loading.

```python
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

### Agents

Agents are autonomous task executors. Trace the full loop.

```python
def run_agent(task: str):
    with tracer.start_as_current_span("agent_run") as agent_span:
        agent_span.set_attribute("task", task)
        agent_span.set_attribute("gen_ai.system", "anthropic")

        step = 0
        while not done:
            step += 1

            # LLM call
            with tracer.start_as_current_span("llm_call") as llm_span:
                llm_span.set_attribute("step", step)
                response = call_llm(messages)
                llm_span.set_attribute("gen_ai.usage.input_tokens", response.usage.input)
                llm_span.set_attribute("gen_ai.usage.output_tokens", response.usage.output)
                llm_span.set_attribute("gen_ai.request.model", response.model)

            # Tool calls
            for tool_call in response.tool_calls:
                with tracer.start_as_current_span("tool_call") as tool_span:
                    tool_span.set_attribute("gen_ai.tool.name", tool_call.name)
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
| `agent_run` | task, total_steps, success, gen_ai.system |
| `llm_call` | step, model, input_tokens, output_tokens |
| `tool_call` | tool_name, tool_args, success, result_size |

### Commands

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

        span.set_attribute("duration_ms", elapsed_ms())
        return result
```

**Key spans:**

| Span | Attributes |
|------|------------|
| `command` | command_name, arg_count, duration_ms |
| `command_parse` | valid, error_message |
| `command_execute` | success, output_size |

### Hooks

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

**Key spans:**

| Span | Attributes |
|------|------------|
| `hook_trigger` | event_type, handler_count, handlers_succeeded |
| `hook_handler` | handler_name, success, modified |

### MCP Servers

MCP servers expose tools to agents. Trace tool registration and calls.

```python
def trace_mcp_server(server: MCPServer):
    with tracer.start_as_current_span("mcp_server") as span:
        span.set_attribute("server_name", server.name)
        span.set_attribute("server_url", server.url)

        with tracer.start_as_current_span("mcp_discover") as discover_span:
            tools = server.list_tools()
            discover_span.set_attribute("tool_count", len(tools))
            discover_span.set_attribute("tool_names", [t.name for t in tools])

        return tools

def trace_mcp_call(server: str, tool: str, args: dict):
    with tracer.start_as_current_span("mcp_call") as span:
        span.set_attribute("server_name", server)
        span.set_attribute("gen_ai.tool.name", tool)
        span.set_attribute("args", str(args)[:500])

        try:
            result = call_mcp_tool(server, tool, args)
            span.set_attribute("success", True)
            span.set_attribute("result_size", len(str(result)))
        except Exception as e:
            span.set_attribute("success", False)
            span.set_attribute("error_type", type(e).__name__)
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

### SDK Apps

For full agent applications using Claude Agent SDK.

**Enable native telemetry:**
```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

**Integration options:**

| Platform | Use Case |
|----------|----------|
| [Langfuse](https://langfuse.com/integrations/frameworks/claude-agent-sdk) | Open source, self-hostable |
| [LangSmith](https://docs.langchain.com/langsmith/trace-claude-agent-sdk) | LangChain ecosystem |
| [MLflow](https://mlflow.org/blog/mlflow-autolog-claude-agents-sdk) | Experiment tracking |
| [Phoenix](https://docs.arize.com/phoenix) | Local-first, no cloud |

---

## Session-Level Tracing

For multi-turn conversations:

```python
def start_session(user_id: str):
    session_span = tracer.start_span("session")
    session_span.set_attribute("user_id", user_id)
    session_span.set_attribute("session_id", generate_id())
    return session_span

def trace_turn(session_span, user_input: str):
    with tracer.start_as_current_span("turn", parent=session_span) as turn_span:
        turn_span.set_attribute("user_input", user_input[:200])
        response = agent.run(user_input)
        turn_span.set_attribute("response", response[:200])
        turn_span.set_attribute("turn_tokens", response.usage.total)
    return response

def end_session(session_span, outcome: str):
    session_span.set_attribute("outcome", outcome)
    session_span.set_attribute("total_turns", turn_count)
    session_span.end()
```

---

## Backend Options

| Backend | Type | Best For |
|---------|------|----------|
| [Phoenix](https://docs.arize.com/phoenix) | Local UI | Development, no cloud required |
| [Langfuse](https://langfuse.com/) | Self-hosted | Production, open source |
| [Datadog](https://www.datadoghq.com/blog/llm-otel-semantic-convention/) | Cloud | Enterprise, native GenAI support |
| [Honeycomb](https://www.honeycomb.io/) | Cloud | High-cardinality queries |
| Console exporter | Debug | Quick debugging, no setup |

---

## Common Gotchas

| Trap | Fix |
|------|-----|
| Missing parent spans | Always set parent for nested spans |
| Attribute size limits | Truncate large values (500 chars) |
| Not ending spans | Use context managers or try/finally |
| Missing errors | Always `record_exception()` on failures |
| No session correlation | Pass session_id through all spans |
| Cardinality explosion | High-cardinality in spans, not metrics |
| HTTP monitoring blind spot | Use hooks or SDK-level tracing |

---

## Sources

- [Claude Code Monitoring](https://code.claude.com/docs/en/monitoring-usage) - Native OTel support
- [Claude Code Hooks](https://code.claude.com/docs/en/hooks) - Hook event reference
- [OpenTelemetry](https://opentelemetry.io/) - Official specification
- [OpenTelemetry GenAI](https://opentelemetry.io/blog/2025/ai-agent-observability/) - Semantic conventions for AI agents
- [OpenInference](https://github.com/Arize-ai/openinference) - LLM-specific instrumentation
- [OpenLLMetry](https://github.com/traceloop/openllmetry) - Auto-instrumentation for GenAI
- [Phoenix](https://docs.arize.com/phoenix) - Local LLM observability UI
- [claude-code-hooks-multi-agent-observability](https://github.com/disler/claude-code-hooks-multi-agent-observability) - Hook-based monitoring
- [claude_telemetry](https://github.com/TechNickAI/claude_telemetry) - OTel wrapper for Claude Code CLI
- [Langfuse Claude Agent SDK](https://langfuse.com/integrations/frameworks/claude-agent-sdk) - Integration guide
