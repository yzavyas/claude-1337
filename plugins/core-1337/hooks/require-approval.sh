#!/bin/bash
# Block external posts - require explicit user approval

input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // ""')

# Patterns that post to external services
if [[ "$command" =~ gh\ (issue|pr|api).*(comment|create|edit|delete) ]] || \
   [[ "$command" =~ curl.*-X\ (POST|PUT|PATCH|DELETE) ]]; then
  echo "BLOCKED: This command posts to an external service. User approval required." >&2
  exit 2
fi

exit 0
