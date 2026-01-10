#!/bin/bash
# PreToolUse hook - suggests modern alternatives to legacy commands
# Follows collaborative agency: suggest, don't block

# Opt-out: skip suggestions if env var is set
if [[ -n "$TERMINAL_1337_SKIP_SUGGESTIONS" ]]; then
  echo '{"decision": "allow"}'
  exit 0
fi

# Read the tool input from stdin
input=$(cat)

# Extract the command from the Bash tool input
command=$(echo "$input" | jq -r '.tool_input.command // empty')

# Check for rm - suggest rip as recoverable alternative
if echo "$command" | grep -qE '(^|[;&|])\s*rm\s'; then
  cat <<'SUGGESTION'
{"decision": "allow", "message": "[terminal-1337] Consider using rip for recoverable deletion:\n\n  rip <file>     # delete (recoverable from graveyard)\n  rip -u         # undo last deletion\n\nInstall: brew install rip2\n\nProceeding with rm as requested."}
SUGGESTION
  exit 0
fi

# Allow the command
echo '{"decision": "allow"}'
