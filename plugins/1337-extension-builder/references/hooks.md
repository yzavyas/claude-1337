# Hooks

Templates, best practices, and observability for hook extensions.

---

## Template

```json
{
  "hooks": [
    {
      "event": "PreToolUse",
      "matcher": { "tool_name": "Bash" },
      "script": "./hooks/validate-bash.sh"
    }
  ]
}
```

### Script Template

```bash
#!/bin/bash
# hooks/validate-bash.sh

# Read input from stdin
input=$(cat)

# Parse with jq
tool_name=$(echo "$input" | jq -r '.tool_name')
command=$(echo "$input" | jq -r '.tool_input.command')

# Validation logic
if [[ "$command" == *"rm -rf"* ]]; then
    echo '{"error": "Dangerous command blocked"}' >&2
    exit 2  # Block
fi

exit 0  # Allow
```

---

## Events

| event | when | can block? | use case |
|-------|------|------------|----------|
| `PreToolUse` | before tool execution | yes | validate, transform |
| `PostToolUse` | after tool success | yes | log, notify |
| `UserPromptSubmit` | user sends message | yes | filter, augment |
| `Stop` | main agent finishes | yes | cleanup, summary |
| `SubagentStop` | subagent finishes | yes | aggregate |
| `PermissionRequest` | permission dialog | yes | auto-approve |
| `SessionStart` | session begins | no | init |
| `SessionEnd` | session terminates | no | cleanup |
| `PreCompact` | before context compaction | no | preserve |
| `Notification` | claude sends notification | no | forward |

### Exit Codes

| code | meaning | effect |
|------|---------|--------|
| 0 | success | action proceeds |
| 1 | non-blocking error | action proceeds, error logged |
| 2 | blocking error | action blocked |

---

## Best Practices

| practice | why |
|----------|-----|
| < 50 lines per script | Runs on every invocation |
| Validate all inputs | Security boundary |
| Quote shell variables | Prevent injection |
| Use `$CLAUDE_PROJECT_DIR` | Absolute paths |
| 60s timeout awareness | Default limit |
| Idempotent operations | May retry |
| JSON input/output | Structured communication |
| Stderr for errors | Stdout for data |

### Matchers

```json
{
  "matcher": {
    "tool_name": "Bash",
    "tool_input.command": ".*rm.*"
  }
}
```

---

## Observability

### Tracing

```python
def trigger_hook(event: str, payload: dict):
    with tracer.start_as_current_span("hook_trigger") as span:
        span.set_attribute("event_type", event)
        span.set_attribute("payload_size", len(str(payload)))

        handlers = get_handlers(event)
        span.set_attribute("handler_count", len(handlers))

        for handler in handlers:
            with tracer.start_as_current_span("hook_handler") as handler_span:
                handler_span.set_attribute("handler_name", handler.name)
                handler_span.set_attribute("script", handler.script)
                try:
                    result = handler.execute(payload)
                    handler_span.set_attribute("success", True)
                    handler_span.set_attribute("exit_code", result.code)
                except Exception as e:
                    handler_span.set_attribute("success", False)
                    handler_span.record_exception(e)
```

### Spans

| span | attributes |
|------|------------|
| `hook_trigger` | event_type, payload_size, handler_count |
| `hook_handler` | handler_name, script, success, exit_code, duration_ms |
| `hook_blocked` | event_type, handler_name, reason |

### Metrics

| metric | meaning |
|--------|---------|
| Trigger rate | Hooks triggered per session |
| Block rate | % of triggers that block |
| Handler latency | Script execution time |

---

## Quality Checklist

- [ ] < 50 lines per script
- [ ] Inputs validated
- [ ] Shell variables quoted
- [ ] Exit codes correct (0/1/2)
- [ ] Idempotent operations
- [ ] Error messages to stderr
- [ ] Tested with each event type
