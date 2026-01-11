#!/bin/bash
# Validate all plugins in the marketplace

set -e

PLUGINS_DIR="$(dirname "$0")/../plugins"
FAILED=0
PASSED=0

echo "Validating plugins..."
echo "====================="

for plugin_dir in "$PLUGINS_DIR"/*/; do
  plugin_name=$(basename "$plugin_dir")

  if [[ -f "$plugin_dir/.claude-plugin/plugin.json" ]]; then
    if claude plugin validate "$plugin_dir" > /dev/null 2>&1; then
      echo "✓ $plugin_name"
      ((PASSED++))
    else
      echo "✗ $plugin_name"
      claude plugin validate "$plugin_dir" 2>&1 | sed 's/^/  /'
      ((FAILED++))
    fi
  else
    echo "⊘ $plugin_name (no plugin.json)"
  fi
done

echo "====================="
echo "Passed: $PASSED, Failed: $FAILED"

if [[ $FAILED -gt 0 ]]; then
  exit 1
fi
