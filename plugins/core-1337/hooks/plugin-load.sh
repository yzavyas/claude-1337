#!/bin/bash
# SessionStart hook - inform Claude about marketplace since auto-discovery is broken
# GitHub issues #10568, #14815, #16575

# Check locations in precedence order: project > user > global
GLOBAL_PATH=$(cat ~/.claude/plugins/known_marketplaces.json 2>/dev/null | jq -r '.["claude-1337"].installLocation // empty')
USER_PATH="$HOME/.claude/plugins/marketplaces/claude-1337"
PROJECT_PATH=""

# Check if we're in the claude-1337 project directory
if [[ -f "${CLAUDE_PROJECT_DIR}/.claude-plugin/marketplace.json" ]]; then
  PROJECT_NAME=$(jq -r '.name // empty' "${CLAUDE_PROJECT_DIR}/.claude-plugin/marketplace.json" 2>/dev/null)
  if [[ "$PROJECT_NAME" == "claude-1337" ]]; then
    PROJECT_PATH="${CLAUDE_PROJECT_DIR}"
  fi
fi

# Determine active location (project takes precedence)
if [[ -n "$PROJECT_PATH" ]]; then
  MARKETPLACE_PATH="$PROJECT_PATH"
  LOCATION_TYPE="project"
elif [[ -n "$GLOBAL_PATH" && -d "$GLOBAL_PATH" ]]; then
  MARKETPLACE_PATH="$GLOBAL_PATH"
  LOCATION_TYPE="global"
else
  exit 0
fi

MARKETPLACE_JSON="${MARKETPLACE_PATH}/.claude-plugin/marketplace.json"

if [[ -f "$MARKETPLACE_JSON" ]]; then
  cat <<EOF
## 1337 Marketplace

Skill auto-discovery is broken (Claude Code bug #10568). Here are the available plugins:

**Precedence:** global -> user -> project (highest)
**Active:** ${LOCATION_TYPE} -> \`${MARKETPLACE_PATH}\`

| Plugin | Use when | SKILL.md |
|--------|----------|----------|
EOF

  # Parse marketplace.json and output each plugin (backticks added via sed)
  jq -r '.plugins[] | "| \(.name) | \(.description | split("Use when:")[1] // "always" | split(".")[0] | ltrimstr(" ")) | plugins/\(.name)/SKILL.md |"' "$MARKETPLACE_JSON" | sed 's/| plugins/| `plugins/g; s/SKILL.md |/SKILL.md` |/g'

  cat <<EOF

Load via \`/plugin-name:skill\` (e.g., \`/rust-1337:rust\`) or read the SKILL.md directly.
EOF
fi
