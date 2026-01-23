#!/bin/bash
# Installs the workaround hook for claude-1337 marketplace

SETTINGS_FILE="$HOME/.claude/settings.json"
MARKETPLACE_DIR="$HOME/.claude/plugins/marketplaces/claude-1337"

if [ ! -d "$MARKETPLACE_DIR" ]; then
  echo "Error: Marketplace not installed. Run first:"
  echo "  /plugin marketplace add yzavyas/claude-1337"
  exit 1
fi

HOOK_JSON='{
  "SessionStart": [
    {
      "hooks": [
        {
          "type": "prompt",
          "prompt": "A marketplace of plugins is available at `~/.claude/plugins/marketplaces/claude-1337/plugins/`. Review the installed plugins - they contain skills, agents, and hooks that may be useful."
        }
      ]
    }
  ]
}'

if [ ! -f "$SETTINGS_FILE" ]; then
  # No settings file - create one
  echo '{"hooks":'"$HOOK_JSON"'}' > "$SETTINGS_FILE"
  echo "Created $SETTINGS_FILE with workaround hook"
elif ! command -v jq &> /dev/null; then
  # No jq - can't merge safely
  echo "Error: jq required to merge into existing settings.json"
  echo "Install jq or manually add hooks to $SETTINGS_FILE"
  echo ""
  echo "Hook to add:"
  echo "$HOOK_JSON"
  exit 1
else
  # Merge using jq
  TEMP_FILE=$(mktemp)
  jq --argjson hook "$HOOK_JSON" '.hooks = (.hooks // {}) + $hook' "$SETTINGS_FILE" > "$TEMP_FILE"
  mv "$TEMP_FILE" "$SETTINGS_FILE"
  echo "Added workaround hook to $SETTINGS_FILE"
fi
