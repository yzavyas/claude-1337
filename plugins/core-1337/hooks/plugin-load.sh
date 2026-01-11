#!/bin/bash
# SessionStart hook - inform Claude about marketplace since auto-discovery is broken
# GitHub issues #10568, #14815, #16575

# Check if claude-1337 marketplace is installed
MARKETPLACE_PATH=$(cat ~/.claude/plugins/known_marketplaces.json 2>/dev/null | jq -r '.["claude-1337"].installLocation // empty')

if [[ -n "$MARKETPLACE_PATH" && -d "$MARKETPLACE_PATH" ]]; then
  MARKETPLACE_JSON="${MARKETPLACE_PATH}/.claude-plugin/marketplace.json"

  if [[ -f "$MARKETPLACE_JSON" ]]; then
    cat <<EOF
## 1337 Marketplace

Skill auto-discovery is broken (Claude Code bug #10568). Here are the available plugins:

| Plugin | Use when | Location |
|--------|----------|----------|
EOF

    # Parse marketplace.json and output each plugin
    jq -r '.plugins[] | "| \(.name) | \(.description | split("Use when:")[1] // "always" | split(".")[0] | ltrimstr(" ")) | `'"${MARKETPLACE_PATH}"'/plugins/\(.name)/SKILL.md` |"' "$MARKETPLACE_JSON"

    cat <<EOF

Load via \`/plugin-name:skill\` (e.g., \`/rust-1337:rust\`).
EOF
  fi
fi
