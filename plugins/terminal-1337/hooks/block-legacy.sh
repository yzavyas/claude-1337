#!/bin/bash
# PreToolUse hook - suggests modern alternatives to legacy commands
# Follows collaborative agency: suggest, don't block
#
# Output contract (current Claude Code hook schema):
#   - Neutral (no opinion): emit nothing, exit 0. The normal permission flow runs.
#   - Advisory: hookSpecificOutput.additionalContext carries the suggestion.
#
# Deliberately NOT permissionDecision:"allow" — this hook matches every Bash
# call, so returning "allow" would auto-approve all of them and bypass the
# permission prompt, including for the very rm we are commenting on. Advisory
# hooks stay neutral and let the user decide.

# Opt-out: skip suggestions if env var is set
if [[ -n "$TERMINAL_1337_SKIP_SUGGESTIONS" ]]; then
  exit 0
fi

# Read the tool input from stdin
input=$(cat)

# Extract the command from the Bash tool input
command=$(echo "$input" | jq -r '.tool_input.command // empty')

# Check for rm - suggest rip as recoverable alternative
if echo "$command" | grep -qE '(^|[;&|])\s*rm\s'; then
  jq -nc '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      additionalContext: "[terminal-1337] Consider rip for recoverable deletion: `rip <file>` (recoverable from graveyard), `rip -u` (undo last deletion). Install: brew install rip2 / cargo install rm-improved."
    }
  }'
  exit 0
fi

# No opinion on this command.
exit 0
