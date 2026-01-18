#!/bin/bash
# Detects debugging loops and triggers Mr. Wolf
# Called by PostToolUse hook on Bash tool
# Opt-out: SKIP_MRWOLF_HOOKS=1

# Check for opt-out
if [[ "${SKIP_MRWOLF_HOOKS:-}" == "1" ]]; then
    echo '{"decision": "allow"}'
    exit 0
fi

# Get tool result from stdin
TOOL_OUTPUT=$(cat)

# State file to track consecutive failures (use parent PID for session consistency)
STATE_FILE="/tmp/claude-mrwolf-state-${PPID:-$$}"

# Initialize state if doesn't exist
if [[ ! -f "$STATE_FILE" ]]; then
    echo "0" > "$STATE_FILE"
fi

FAIL_COUNT=$(cat "$STATE_FILE")

# Check if this looks like a failure
if echo "$TOOL_OUTPUT" | grep -qiE "(error|failed|exception|not found|permission denied|command not found|no such file|cannot|unable to|fatal|panic|traceback)"; then
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo "$FAIL_COUNT" > "$STATE_FILE"

    # After 3 consecutive failures, trigger Mr. Wolf
    if [[ $FAIL_COUNT -ge 3 ]]; then
        # Reset counter
        echo "0" > "$STATE_FILE"

        cat << 'EOF'
{
  "decision": "allow",
  "message": "🐺 DEBUGGING LOOP DETECTED (3 consecutive failures). You MUST now: 1) Tell the user: 'This isn't converging. Bringing in Mr. Wolf.' 2) Spawn the `mrwolf` agent to break down the problem systematically. Do not continue debugging yourself."
}
EOF
        exit 0
    fi
else
    # Success - reset counter
    echo "0" > "$STATE_FILE"
fi

# No intervention needed
echo '{"decision": "allow"}'
