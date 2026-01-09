# SDK Apps (Agent SDK)

Templates, best practices, and observability for Claude Agent SDK applications.

The Agent SDK gives you the same tools, agent loop, and context management that power Claude Code, programmable in Python and TypeScript.

---

## Python Template

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Your task here",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Bash"],
            permission_mode="acceptEdits",
            cwd="/path/to/project"
        )
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

---

## TypeScript Template

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Your task here",
  options: {
    allowedTools: ["Read", "Edit", "Bash"],
    permissionMode: "acceptEdits"
  }
})) {
  if ("result" in message) console.log(message.result);
}
```

---

## ClaudeSDKClient vs query()

| Feature | `query()` | `ClaudeSDKClient` |
|---------|-----------|-------------------|
| Session | New each call | Maintains across calls |
| Conversation | Single exchange | Multi-turn context |
| Interrupts | Not supported | Supported |
| Hooks | Not supported | Supported |
| Custom Tools | Not supported | Supported |
| Use Case | One-off tasks | Interactive apps |

### Continuous Conversation Pattern

```python
from claude_agent_sdk import ClaudeSDKClient, AssistantMessage, TextBlock

async def main():
    async with ClaudeSDKClient() as client:
        # First question
        await client.query("What's the capital of France?")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

        # Follow-up - Claude remembers context
        await client.query("What's the population of that city?")
        async for message in client.receive_response():
            # Claude knows "that city" = Paris
            ...
```

---

## Built-in Tools

| Tool | What it does |
|------|--------------|
| **Read** | Read any file in working directory |
| **Write** | Create new files |
| **Edit** | Make precise edits |
| **Bash** | Run terminal commands |
| **Glob** | Find files by pattern |
| **Grep** | Search file contents |
| **WebSearch** | Search the web |
| **WebFetch** | Fetch and parse web pages |
| **AskUserQuestion** | Ask clarifying questions |
| **Task** | Spawn subagents |

---

## Custom Tools (MCP)

```python
from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeAgentOptions

@tool("greet", "Greet a user", {"name": str})
async def greet(args):
    return {
        "content": [{"type": "text", "text": f"Hello, {args['name']}!"}]
    }

server = create_sdk_mcp_server(
    name="my-tools",
    version="1.0.0",
    tools=[greet]
)

options = ClaudeAgentOptions(
    mcp_servers={"my": server},
    allowed_tools=["mcp__my__greet"]
)
```

---

## Subagents

```python
from claude_agent_sdk import ClaudeAgentOptions, AgentDefinition

options = ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Task"],
    agents={
        "code-reviewer": AgentDefinition(
            description="Expert code reviewer.",
            prompt="Analyze code quality and suggest improvements.",
            tools=["Read", "Glob", "Grep"]
        )
    }
)
```

**Critical**: Subagents cannot spawn other subagents.

---

## Hooks

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, HookMatcher

async def log_tool_use(input_data, tool_use_id, context):
    print(f"Tool used: {input_data.get('tool_name')}")
    return {}

async def block_dangerous(input_data, tool_use_id, context):
    command = input_data.get('tool_input', {}).get('command', '')
    if 'rm -rf /' in command:
        return {
            'hookSpecificOutput': {
                'hookEventName': 'PreToolUse',
                'permissionDecision': 'deny',
                'permissionDecisionReason': 'Dangerous command blocked'
            }
        }
    return {}

options = ClaudeAgentOptions(
    hooks={
        'PreToolUse': [
            HookMatcher(matcher='Bash', hooks=[block_dangerous]),
            HookMatcher(hooks=[log_tool_use])
        ]
    }
)
```

---

## Permission Modes

| Mode | Effect |
|------|--------|
| `default` | Standard permission behavior |
| `acceptEdits` | Auto-accept file edits |
| `plan` | Planning mode - no execution |
| `bypassPermissions` | Bypass all checks (caution) |

---

## Best Practices

| practice | why |
|----------|-----|
| Use `ClaudeSDKClient` for multi-turn | Maintains context across exchanges |
| Limit `allowed_tools` | Security + focus |
| Set `cwd` explicitly | Clear working directory |
| Handle errors with try/except | CLINotFoundError, ProcessError |
| Use `permission_mode="acceptEdits"` for automation | Avoid approval prompts |
| Include `Task` in tools for subagents | Required for delegation |

### Error Handling

```python
from claude_agent_sdk import (
    query,
    CLINotFoundError,
    ProcessError,
    CLIJSONDecodeError
)

try:
    async for message in query(prompt="Hello"):
        print(message)
except CLINotFoundError:
    print("Install Claude Code: npm install -g @anthropic-ai/claude-code")
except ProcessError as e:
    print(f"Process failed: {e.exit_code}")
except CLIJSONDecodeError as e:
    print(f"Parse error: {e}")
```

---

## Observability

The Agent SDK has native OpenTelemetry support.

### Phoenix Integration

```python
import phoenix as px
px.launch_app()  # localhost:6006

from openinference.instrumentation.anthropic import AnthropicInstrumentor
AnthropicInstrumentor().instrument()
```

### Custom Tracing

```python
from opentelemetry import trace

tracer = trace.get_tracer("my-agent-app")

async def run_agent(task: str):
    with tracer.start_as_current_span("agent_task") as span:
        span.set_attribute("task", task)

        async for message in query(prompt=task, options=options):
            if hasattr(message, "result"):
                span.set_attribute("success", True)
                return message.result

        span.set_attribute("success", False)
```

### Spans

| span | attributes |
|------|------------|
| `agent_task` | task, success, duration_ms |
| `llm_call` | model, input_tokens, output_tokens |
| `tool_call` | tool_name, success |
| `subagent` | agent_name, task |

---

## Message Types

| Type | Description |
|------|-------------|
| `UserMessage` | User input |
| `AssistantMessage` | Claude response with content blocks |
| `SystemMessage` | System metadata |
| `ResultMessage` | Final result with cost/usage |

### Content Blocks

| Block | Description |
|-------|-------------|
| `TextBlock` | Text content |
| `ThinkingBlock` | Reasoning (thinking models) |
| `ToolUseBlock` | Tool call request |
| `ToolResultBlock` | Tool execution result |

---

## Quality Checklist

- [ ] `allowed_tools` explicitly set
- [ ] Error handling for CLI errors
- [ ] `ClaudeSDKClient` for multi-turn
- [ ] Hooks for security validation
- [ ] Subagents have limited tools
- [ ] Permission mode appropriate for use case
- [ ] Observability instrumented
- [ ] Tested with representative tasks

---

## Sources

- [Agent SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Python SDK Reference](https://platform.claude.com/docs/en/agent-sdk/python)
- [TypeScript SDK](https://github.com/anthropics/claude-agent-sdk-typescript)
- [SDK Demos](https://github.com/anthropics/claude-agent-sdk-demos)
