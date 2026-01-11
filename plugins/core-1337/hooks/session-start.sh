#!/bin/bash
cat << 'EOF'
## 1337 Marketplace

Skill auto-discovery is broken (Claude Code bug #10568).

**To find available plugins:**
1. Read `~/.claude/plugins/known_marketplaces.json` → get `installLocation` for "claude-1337"
2. Read `{installLocation}/.claude-plugin/marketplace.json` → each plugin has "Use when:" trigger
3. Plugin content at `{installLocation}/plugins/<name>/`

Load skills when their trigger matches the user's task.
EOF
