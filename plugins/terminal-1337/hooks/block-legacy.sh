#!/bin/bash
# PreToolUse hook - blocks legacy commands, enforces modern alternatives

# Read the tool input from stdin
input=$(cat)

# Extract the command from the Bash tool input
command=$(echo "$input" | jq -r '.tool_input.command // empty')

# Check for rm
if echo "$command" | grep -qE '(^|[;&|])\s*rm\s'; then
  cat <<'BLOCK'
{"decision": "block", "reason": "BLOCKED: rm is not allowed. Use rip instead:\n\n  rip <file>     # delete (recoverable)\n  rip -u         # undo last deletion\n\nInstall: brew install rip2"}
BLOCK
  exit 0
fi

# Allow the command
echo '{"decision": "allow"}'
