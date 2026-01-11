#!/bin/sh
# Outputs plugin triggers from claude-1337 marketplace
# POSIX-compliant

MARKETPLACES_FILE="$HOME/.claude/plugins/known_marketplaces.json"

# Get install location if marketplace exists
if [ -f "$MARKETPLACES_FILE" ]; then
  INSTALL_LOC=$(grep -A5 '"claude-1337"' "$MARKETPLACES_FILE" 2>/dev/null | grep 'installLocation' | sed 's/.*: *"\([^"]*\)".*/\1/')
fi

# Always output core-1337 instruction
echo "## claude-1337"
echo ""
echo "**Load now:** \`$INSTALL_LOC/plugins/core-1337/SKILL.md\`"

# If we have the marketplace, show the trigger table
if [ -n "$INSTALL_LOC" ] && [ -f "$INSTALL_LOC/.claude-plugin/marketplace.json" ]; then
  echo ""
  echo "**Other plugins** (load when relevant):"
  echo ""

  awk -F'"' -v loc="$INSTALL_LOC" '
    /"name":/ { name = $4 }
    /"description":/ && /Use when:/ {
      desc = $4
      sub(/.*Use when: /, "", desc)
      sub(/\..*/, "", desc)
      if (name != "core-1337" && name != "") {
        print "- **" name "** → " desc " → `" loc "/plugins/" name "/SKILL.md`"
      }
    }
  ' "$INSTALL_LOC/.claude-plugin/marketplace.json"
fi
