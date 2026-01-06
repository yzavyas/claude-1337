# Hooks

Hooks execute shell commands in response to Claude Code events.

## Why Use Hooks

Hooks inject context at the right moment. Instead of hoping Claude remembers instructions, you inject them when relevant.

**Example**: Rather than putting skill guidance in CLAUDE.md (which may be overlooked), `core-1337` uses a SessionStart hook to explain skill value at the start of every session.

## Hook Types

| Hook | When | Use For |
|------|------|---------|
| `SessionStart` | New conversation begins | Inject session-wide context |
| `PreToolUse` | Before a tool executes | Validate, augment, or block |
| `PostToolUse` | After a tool executes | React to results, chain actions |
| `Stop` | Before Claude stops | Final checks, cleanup |

## Structure

```
plugin-name/
└── hooks/
    ├── hooks.json      # Hook definitions
    └── my-hook.sh      # Hook script
```

### hooks.json

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/hooks/session-start.sh"
      }
    ]
  }
}
```

### Hook Script

```bash
#!/bin/bash
# Output is injected as context

cat <<'EOF'
## Context Injection

This text becomes part of Claude's context.
Use it to provide guidance, not commands.
EOF
```

## Design Principles

### Motivation Over Commands

Following the autonomy principle, hooks should explain *why* not demand *what*.

**Less effective:**
```
You MUST check skills before responding.
```

**More effective:**
```
Skills contain curated knowledge from production experience.
Activating relevant skills helps you give better, faster answers.
```

### Keep It Focused

Hook output adds to context. Long outputs waste tokens and attention.

- SessionStart: 200-400 tokens ideal
- PreToolUse: 50-100 tokens
- PostToolUse: Vary based on need

### Fail Gracefully

Hooks can block operations. Use sparingly and with clear feedback.

```bash
if [[ "$TOOL_NAME" == "Write" && "$FILE_PATH" == *.md ]]; then
  echo "Consider: Does this need a skill update too?"
fi
```

## Example: core-1337

The `core-1337` SessionStart hook:
1. Explains why skills are valuable
2. Describes how to evaluate and activate
3. Sets quality standards for the session

It doesn't force activation - it provides understanding that leads to better decisions.
