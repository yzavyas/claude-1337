#!/usr/bin/env bash
# Writing style validator for claude-1337
# Checks for em dash overuse and false dichotomies
#
# Usage: check-style.sh [file|directory]
# Exit: 0 = clean, 1 = issues found

set -euo pipefail

TARGET="${1:-.}"
ISSUES=0

# Colors (disabled if not tty)
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    YELLOW='\033[0;33m'
    GREEN='\033[0;32m'
    NC='\033[0m'
else
    RED='' YELLOW='' GREEN='' NC=''
fi

warn() { echo -e "${YELLOW}warning:${NC} $1"; }
error() { echo -e "${RED}error:${NC} $1"; }
ok() { echo -e "${GREEN}ok:${NC} $1"; }

# Use rg if available, otherwise grep
if command -v rg &> /dev/null; then
    SEARCH="rg"
else
    SEARCH="grep"
    warn "ripgrep not found, using grep (slower)"
fi

echo "Checking: $TARGET (using $SEARCH)"
echo "─────────────────────────────────────"

# ─────────────────────────────────────────
# Em Dash Overuse
# ─────────────────────────────────────────
echo -e "\n## Em dash usage"

if [[ "$SEARCH" == "rg" ]]; then
    EM_COUNT=$(rg -c "—" --type md "$TARGET" 2>/dev/null | awk -F: '{sum+=$2} END {print sum+0}')
else
    EM_COUNT=$(grep -r -o "—" --include="*.md" "$TARGET" 2>/dev/null | wc -l | tr -d ' ')
fi

if [[ "$EM_COUNT" -gt 50 ]]; then
    error "Em dash overuse: $EM_COUNT"
    echo "Prose patterns to fix:"
    if [[ "$SEARCH" == "rg" ]]; then
        rg -n "[a-z] — [a-z]" --type md "$TARGET" 2>/dev/null | head -10 || true
    else
        grep -rn "[a-z] — [a-z]" --include="*.md" "$TARGET" 2>/dev/null | head -10 || true
    fi
    ISSUES=$((ISSUES + 1))
elif [[ "$EM_COUNT" -gt 20 ]]; then
    warn "Em dashes: $EM_COUNT (consider reducing)"
else
    ok "Em dashes: $EM_COUNT"
fi

# ─────────────────────────────────────────
# False Dichotomies
# ─────────────────────────────────────────
echo -e "\n## False dichotomies"

# Pattern: "isn't about X" or "isn't X, it's Y"
if [[ "$SEARCH" == "rg" ]]; then
    DICHOT_HITS=$(rg -n "isn't .*(it's|its)" --type md "$TARGET" 2>/dev/null | head -10 || true)
else
    DICHOT_HITS=$(grep -rn "isn't .*(it's|its)" --include="*.md" "$TARGET" 2>/dev/null | head -10 || true)
fi

if [[ -n "$DICHOT_HITS" ]]; then
    warn "Potential false dichotomies:"
    echo "$DICHOT_HITS"
    echo "  → Falsification test: Can it be both X and Y?"
else
    ok "No obvious false dichotomies"
fi

# ─────────────────────────────────────────
# Summary
# ─────────────────────────────────────────
echo -e "\n─────────────────────────────────────"
if [[ "$ISSUES" -gt 0 ]]; then
    error "Failed: $ISSUES blocker(s)"
    exit 1
else
    ok "Style check passed"
    exit 0
fi
