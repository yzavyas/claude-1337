#!/bin/bash
# SessionStart hook - enforce modern terminal tools

cat <<'EOF'
TERMINAL-1337: Tool Replacements Active

MANDATORY replacements for this session:

| Legacy | Use Instead | Why |
|--------|-------------|-----|
| rm     | rip         | recoverable deletion |
| cat    | bat         | syntax highlighting |
| ls     | eza         | better output, git status |
| find   | fd          | faster, simpler syntax |
| grep   | rg          | ripgrep, much faster |

If a tool isn't installed, offer to install it first.
EOF
