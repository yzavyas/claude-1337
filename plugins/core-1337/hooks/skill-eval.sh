#!/bin/bash
# SessionStart hook for 1337 marketplace awareness
# Dynamically reads from marketplace.json

MARKETPLACE_FILE="${CLAUDE_PROJECT_DIR}/.claude-plugin/marketplace.json"

cat <<'EOF'
## 1337 Marketplace

Marketplace skills may not auto-discover (Claude Code bug #10568). Each plugin has a `/command` to load it explicitly.
EOF

# List installed plugins dynamically
if [ -f "$MARKETPLACE_FILE" ]; then
  echo ""
  echo "**Installed:**"
  jq -r '.plugins[] | "- \(.name)"' "$MARKETPLACE_FILE" 2>/dev/null || echo "- (could not parse marketplace.json)"
  echo ""
  echo "Run \`/help\` or check \`plugins/*/commands/\` for available commands."
  echo ""
fi

cat <<'EOF'
**Standards:** Evidence with recommendations. Commit to positions. Acknowledge uncertainty.
EOF
