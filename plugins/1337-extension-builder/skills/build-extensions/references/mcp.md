# MCP Servers

Templates, best practices, and observability for MCP (Model Context Protocol) extensions.

---

## Configuration Template

```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["./mcp/server.js"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

---

## Server Template (TypeScript)

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "my-server",
  version: "1.0.0"
}, {
  capabilities: { tools: {} }
});

// List available tools
server.setRequestHandler("tools/list", async () => ({
  tools: [{
    name: "my_tool",
    description: "What it does. Use when: [trigger].",
    inputSchema: {
      type: "object",
      properties: {
        param: { type: "string", description: "What this is" }
      },
      required: ["param"]
    }
  }]
}));

// Handle tool calls
server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "my_tool") {
    try {
      const result = await doThing(args.param);
      return { content: [{ type: "text", text: result }] };
    } catch (error) {
      return {
        content: [{ type: "text", text: `Error: ${error.message}` }],
        isError: true
      };
    }
  }

  throw new Error(`Unknown tool: ${name}`);
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

---

## Server Template (Python)

```python
from mcp import Server, Tool
from mcp.server.stdio import stdio_server

server = Server("my-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="my_tool",
            description="What it does. Use when: [trigger].",
            inputSchema={
                "type": "object",
                "properties": {
                    "param": {"type": "string", "description": "What this is"}
                },
                "required": ["param"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "my_tool":
        result = await do_thing(arguments["param"])
        return [{"type": "text", "text": result}]

    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as streams:
        await server.run(*streams)
```

---

## Best Practices

| practice | why |
|----------|-----|
| Minimal surface | Only expose what's needed |
| Validate all inputs | Security boundary |
| Local scope for credentials | Don't commit secrets |
| Graceful degradation | Handle service unavailability |
| Token limits awareness | 10k warn, 25k max |
| "Use when:" in descriptions | Helps Claude decide |
| Structured errors | Clear failure messages |

### Token Limits

| threshold | effect |
|-----------|--------|
| 10k tokens | Warning logged |
| 25k tokens | Output truncated |

Configure with `MAX_MCP_OUTPUT_TOKENS` environment variable.

### Security

| practice | implementation |
|----------|----------------|
| Input validation | Schema validation before processing |
| Credential scope | `env` in config, not in code |
| Error sanitization | Don't leak internal details |
| Rate limiting | Prevent abuse |

---

## Observability

### Tracing

```python
def trace_mcp_call(server: str, tool: str, args: dict):
    with tracer.start_as_current_span("mcp_call") as span:
        span.set_attribute("server_name", server)
        span.set_attribute("tool_name", tool)
        span.set_attribute("args", str(args)[:500])

        try:
            start = time.time()
            result = call_mcp_tool(server, tool, args)

            span.set_attribute("success", True)
            span.set_attribute("result_size", len(str(result)))
            span.set_attribute("duration_ms", (time.time() - start) * 1000)

        except Exception as e:
            span.set_attribute("success", False)
            span.set_attribute("error_type", type(e).__name__)
            span.set_attribute("error_message", str(e))
            span.record_exception(e)
            raise

        return result
```

### Spans

| span | attributes |
|------|------------|
| `mcp_server_start` | server_name, version |
| `mcp_discover` | server_name, tool_count, tool_names |
| `mcp_call` | server_name, tool_name, args, success, result_size, duration_ms |
| `mcp_error` | server_name, tool_name, error_type, error_message |

### Metrics

| metric | meaning |
|--------|---------|
| Tool call rate | Calls per minute |
| Success rate | % of calls successful |
| Latency p50/p99 | Performance distribution |
| Token output | Average result size |

---

## Quality Checklist

- [ ] Minimal tool surface
- [ ] "Use when:" in tool descriptions
- [ ] Input schema validation
- [ ] Credentials in env, not code
- [ ] Graceful error handling
- [ ] Token output under limits
- [ ] Tested with representative inputs
