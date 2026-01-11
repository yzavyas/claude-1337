#!/bin/bash
# SessionStart hook - inform Claude about marketplace since auto-discovery is broken
# GitHub issues #10568, #16575

cat <<'EOF'
## 1337 Marketplace

Skill auto-discovery is broken (Claude Code bug #10568).

**To find available skills:** Read `${CLAUDE_PROJECT_DIR}/.claude-plugin/marketplace.json`
- Each plugin has a description with "Use when:" — that's your activation signal
- Plugin content at `${CLAUDE_PROJECT_DIR}/plugins/<name>/`
- Components: SKILL.md, commands/, agents/, hooks/ (convention-based)

Load what you need, when you need it.
EOF
