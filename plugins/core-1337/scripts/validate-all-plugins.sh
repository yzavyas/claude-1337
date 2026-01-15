#!/bin/bash
# Validate All Plugins
# Runs validation on all plugins in the marketplace before commit

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGINS_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)/plugins"

# Path to plugin-dev validation scripts
PLUGIN_DEV_CACHE="$HOME/.claude/plugins/cache/claude-plugins-official/plugin-dev"
VALIDATE_AGENT=""
VALIDATE_HOOK=""

# Find the plugin-dev cache (version varies)
for dir in "$PLUGIN_DEV_CACHE"/*/; do
  if [ -f "${dir}skills/agent-development/scripts/validate-agent.sh" ]; then
    VALIDATE_AGENT="${dir}skills/agent-development/scripts/validate-agent.sh"
    VALIDATE_HOOK="${dir}skills/hook-development/scripts/validate-hook-schema.sh"
    break
  fi
done

if [ -z "$VALIDATE_AGENT" ]; then
  echo "⚠️  plugin-dev validation scripts not found"
  echo "   Install plugin-dev: /plugin install plugin-dev@claude-plugins-official"
  echo ""
  echo "Running basic validation only..."
  BASIC_ONLY=true
else
  BASIC_ONLY=false
fi

echo "🔍 Validating all plugins in: $PLUGINS_DIR"
echo ""

total_errors=0
total_warnings=0
plugins_checked=0
agents_checked=0
hooks_checked=0
skills_checked=0

# Validate each plugin
for plugin_dir in "$PLUGINS_DIR"/*/; do
  plugin_name=$(basename "$plugin_dir")
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📦 Plugin: $plugin_name"
  echo ""

  ((plugins_checked++))
  plugin_errors=0
  plugin_warnings=0

  # Check plugin.json exists
  if [ ! -f "$plugin_dir/.claude-plugin/plugin.json" ]; then
    echo "❌ Missing .claude-plugin/plugin.json"
    ((plugin_errors++))
  else
    echo "✅ plugin.json exists"
  fi

  # Validate agents
  if [ -d "$plugin_dir/agents" ]; then
    echo ""
    echo "Agents:"
    for agent_file in "$plugin_dir"/agents/*.md; do
      [ -e "$agent_file" ] || continue
      agent_name=$(basename "$agent_file")
      ((agents_checked++))

      if [ "$BASIC_ONLY" = true ]; then
        # Basic validation
        if grep -q '^name:' "$agent_file" && grep -q '^description:' "$agent_file" && grep -q '^model:' "$agent_file" && grep -q '^color:' "$agent_file"; then
          echo "  ✅ $agent_name (basic check)"
        else
          echo "  ❌ $agent_name missing required frontmatter fields"
          ((plugin_errors++))
        fi
      else
        # Full validation
        if "$VALIDATE_AGENT" "$agent_file" > /dev/null 2>&1; then
          echo "  ✅ $agent_name"
        else
          echo "  ❌ $agent_name (run validate-agent.sh for details)"
          ((plugin_errors++))
        fi
      fi
    done
  fi

  # Validate skills
  if [ -d "$plugin_dir/skills" ]; then
    echo ""
    echo "Skills:"
    for skill_dir in "$plugin_dir"/skills/*/; do
      [ -d "$skill_dir" ] || continue
      skill_name=$(basename "$skill_dir")
      ((skills_checked++))

      if [ -f "$skill_dir/SKILL.md" ]; then
        # Check frontmatter
        if head -1 "$skill_dir/SKILL.md" | grep -q '^---$'; then
          if grep -q '^name:' "$skill_dir/SKILL.md" && grep -q '^description:' "$skill_dir/SKILL.md"; then
            echo "  ✅ $skill_name"
          else
            echo "  ⚠️  $skill_name missing name or description in frontmatter"
            ((plugin_warnings++))
          fi
        else
          echo "  ⚠️  $skill_name SKILL.md missing frontmatter"
          ((plugin_warnings++))
        fi
      else
        echo "  ❌ $skill_name missing SKILL.md"
        ((plugin_errors++))
      fi
    done
  fi

  # Validate hooks
  if [ -d "$plugin_dir/hooks" ]; then
    echo ""
    echo "Hooks:"
    if [ -f "$plugin_dir/hooks/hooks.json" ]; then
      ((hooks_checked++))
      # Basic JSON validation
      if python3 -c "import json; json.load(open('$plugin_dir/hooks/hooks.json'))" 2>/dev/null; then
        echo "  ✅ hooks.json (valid JSON)"
      else
        echo "  ❌ hooks.json (invalid JSON)"
        ((plugin_errors++))
      fi
    fi
  fi

  total_errors=$((total_errors + plugin_errors))
  total_warnings=$((total_warnings + plugin_warnings))

  if [ $plugin_errors -eq 0 ] && [ $plugin_warnings -eq 0 ]; then
    echo ""
    echo "✅ $plugin_name: All checks passed"
  elif [ $plugin_errors -eq 0 ]; then
    echo ""
    echo "⚠️  $plugin_name: $plugin_warnings warning(s)"
  else
    echo ""
    echo "❌ $plugin_name: $plugin_errors error(s), $plugin_warnings warning(s)"
  fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Summary"
echo ""
echo "  Plugins checked: $plugins_checked"
echo "  Agents checked:  $agents_checked"
echo "  Skills checked:  $skills_checked"
echo "  Hooks checked:   $hooks_checked"
echo ""

if [ $total_errors -eq 0 ] && [ $total_warnings -eq 0 ]; then
  echo "✅ All validations passed!"
  exit 0
elif [ $total_errors -eq 0 ]; then
  echo "⚠️  Validation passed with $total_warnings warning(s)"
  exit 0
else
  echo "❌ Validation failed: $total_errors error(s), $total_warnings warning(s)"
  exit 1
fi
