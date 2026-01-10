#!/bin/bash
# SessionStart hook - suggest modern terminal tools
# Follows collaborative agency: inform, don't mandate

# Opt-out: skip message if env var is set
if [[ -n "$TERMINAL_1337_SKIP_SUGGESTIONS" ]]; then
  exit 0
fi

cat <<'EOF'
[terminal-1337] Modern CLI Tools Available

Suggested alternatives (if installed):

| Legacy | Modern | Why |
|--------|--------|-----|
| rm     | rip    | recoverable deletion (graveyard) |
| cat    | bat    | syntax highlighting |
| ls     | eza    | better output, git status |
| find   | fd     | faster, simpler syntax |
| grep   | rg     | ripgrep, parallel search |

Use `command -v <tool>` to check availability.
Fallback to legacy tools is always fine.

Disable these suggestions: export TERMINAL_1337_SKIP_SUGGESTIONS=1
EOF
