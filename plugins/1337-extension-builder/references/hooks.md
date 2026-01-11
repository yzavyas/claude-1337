# Hooks

Templates, best practices, and observability for hook extensions.

---

## Template

```json
{
  "description": "Brief description of hook purpose",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/validate-bash.sh"
          }
        ]
      }
    ]
  }
}
```

### Script Template

```bash
#!/bin/bash
# hooks/validate-bash.sh

set -euo pipefail

# Read input from stdin
input=$(cat)

# Parse with jq
tool_name=$(echo "$input" | jq -r '.tool_name')
command=$(echo "$input" | jq -r '.tool_input.command')

# Validation logic
if [[ "$command" == *"rm -rf"* ]]; then
    echo '{"decision": "deny", "reason": "Dangerous command blocked"}' >&2
    exit 2  # Block
fi

exit 0  # Allow
```

---

## CRITICAL: Correct Format

The `hooks` field must be an **object with event names as keys**, not an array.

```json
// ❌ WRONG — array format (will fail to load)
{
  "hooks": [
    { "event": "PreToolUse", "script": "./test.sh" }
  ]
}

// ✅ CORRECT — nested object format
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/test.sh" }
        ]
      }
    ]
  }
}
```

### Structure Breakdown

```
hooks.json
├── description (optional): string
└── hooks: object
    └── EventName: array of hook entries
        └── each entry:
            ├── matcher (optional): string (tool name pattern)
            └── hooks: array of actions
                └── each action:
                    ├── type: "command" | "prompt"
                    ├── command: string (for type=command)
                    ├── prompt: string (for type=prompt)
                    └── timeout (optional): number (seconds)
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

## Hook Types

### Command Hooks

Execute bash scripts for deterministic checks:

```json
{
  "type": "command",
  "command": "${CLAUDE_PLUGIN_ROOT}/hooks/validate.sh",
  "timeout": 60
}
```

### Prompt Hooks

Use LLM-driven decision making:

```json
{
  "type": "prompt",
  "prompt": "Evaluate if this tool use is appropriate: $TOOL_INPUT",
  "timeout": 30
}
```

Supported events: `Stop`, `SubagentStop`, `UserPromptSubmit`, `PreToolUse`

---

## Best Practices

| practice | why |
|----------|-----|
| < 50 lines per script | Runs on every invocation |
| Validate all inputs | Security boundary |
| Quote shell variables | Prevent injection |
| Use `${CLAUDE_PLUGIN_ROOT}` | Portable paths |
| 60s timeout awareness | Default limit |
| Idempotent operations | May retry |
| JSON input/output | Structured communication |
| Stderr for errors | Stdout for data |

### Matchers

Tool name matching patterns:

```json
// Exact match
{ "matcher": "Write" }

// Multiple tools (OR)
{ "matcher": "Read|Write|Edit" }

// All tools
{ "matcher": "*" }

// Regex patterns
{ "matcher": "mcp__.*__delete.*" }
```

---

## Environment Variables

Available in all command hooks:

| variable | description |
|----------|-------------|
| `$CLAUDE_PROJECT_DIR` | Project root path |
| `$CLAUDE_PLUGIN_ROOT` | Plugin directory (use for portable paths) |
| `$CLAUDE_ENV_FILE` | SessionStart only: persist env vars here |
| `$CLAUDE_CODE_REMOTE` | Set if running in remote context |

**Always use `${CLAUDE_PLUGIN_ROOT}` for portable hook scripts.**

---

## Complete Examples

### SessionStart (load context)

```json
{
  "description": "Load project context at session start",
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/load-context.sh"
          }
        ]
      }
    ]
  }
}
```

### PreToolUse (validate writes)

```json
{
  "description": "Validate file writes for security",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/validate-write.sh"
          }
        ]
      }
    ]
  }
}
```

### Multiple events

```json
{
  "description": "Terminal tool suggestions and validation",
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/load-context.sh" }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/validate-bash.sh" }
        ]
      }
    ]
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

- [ ] Uses correct nested object format (not array)
- [ ] Uses `${CLAUDE_PLUGIN_ROOT}` for all paths
- [ ] < 50 lines per script
- [ ] Inputs validated
- [ ] Shell variables quoted
- [ ] Exit codes correct (0/1/2)
- [ ] Idempotent operations
- [ ] Error messages to stderr
- [ ] Tested with each event type
