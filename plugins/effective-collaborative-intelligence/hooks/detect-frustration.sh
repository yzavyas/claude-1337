#!/bin/bash
# Detects user frustration and triggers Mr. Wolf
# Called by UserPromptSubmit hook
# Opt-out: SKIP_MRWOLF_HOOKS=1

# Check for opt-out
if [[ "${SKIP_MRWOLF_HOOKS:-}" == "1" ]]; then
    echo '{"decision": "allow"}'
    exit 0
fi

# Get user prompt from stdin
USER_PROMPT=$(cat)

# Convert to lowercase for matching
PROMPT_LOWER=$(echo "$USER_PROMPT" | tr '[:upper:]' '[:lower:]')

# Frustration patterns
FRUSTRATED=false

# Check for frustration phrases
if echo "$PROMPT_LOWER" | grep -qE "(still not working|still doesn't work|still broken|tried everything|nothing works|keeps failing|why won't|why doesn't|what am i missing|this is broken|doesn't make sense|going crazy|so frustrated|ugh|argh|wtf|ffs)"; then
    FRUSTRATED=true
fi

# Check for "tried X, Y, Z" patterns (listing multiple attempts)
if echo "$PROMPT_LOWER" | grep -qE "tried .+,.+,.+|i've tried|already tried"; then
    FRUSTRATED=true
fi

# Check for repeated "why" questions about same thing
if echo "$PROMPT_LOWER" | grep -qE "why (is this|does this|won't|doesn't|can't) .* (still|again|keep)"; then
    FRUSTRATED=true
fi

if [[ "$FRUSTRATED" == "true" ]]; then
    cat << 'EOF'
{
  "decision": "allow",
  "message": "🐺 USER FRUSTRATION DETECTED. You MUST now: 1) Acknowledge: 'I hear you. This needs Mr. Wolf.' 2) Spawn the `mrwolf` agent immediately to break this down. Do not attempt more fixes yourself — Mr. Wolf takes over."
}
EOF
else
    echo '{"decision": "allow"}'
fi
