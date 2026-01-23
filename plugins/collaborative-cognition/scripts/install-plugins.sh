#!/bin/bash
# Installs claude-1337 plugins as user-defined components in ~/.claude/
#
# This bypasses the plugin system by copying skills/, agents/, commands/, hooks/
# directly to ~/.claude/ as user-defined components.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGINS_DIR="$SCRIPT_DIR/../../"  # Go up to plugins/
CLAUDE_DIR="$HOME/.claude"

# Available plugins
PLUGINS=(
  "core-1337:Engineering excellence - reasoning verification, design principles"
  "terminal-1337:Modern terminal tools - ripgrep, fd, bat, eza, fzf"
  "rust-1337:Rust production patterns - async, crates, domains"
  "kotlin-1337:Kotlin patterns - coroutines, Flow, Spring, Android"
  "jvm-analysis-1337:JVM analysis - profiling, dead code, memory"
  "sensei-1337:Documentation methodology - Feynman, Diataxis"
  "eval-1337:LLM evaluation - DeepEval, Braintrust, RAGAS"
  "experience-1337:Frontend experience - animation, 3D, design systems"
  "1337-extension-builder:Build extensions with quality methodology"
)

usage() {
  echo "Usage: $0 [options] [plugin...]"
  echo ""
  echo "Installs claude-1337 plugins as user-defined components in ~/.claude/"
  echo ""
  echo "Options:"
  echo "  -a, --all      Install all plugins"
  echo "  -l, --list     List available plugins"
  echo "  -h, --help     Show this help"
  echo ""
  echo "Examples:"
  echo "  $0 --all                    # Install all plugins"
  echo "  $0 core-1337 rust-1337      # Install specific plugins"
  echo "  $0 --list                   # Show available plugins"
}

list_plugins() {
  echo "Available plugins:"
  echo ""
  for plugin_info in "${PLUGINS[@]}"; do
    name="${plugin_info%%:*}"
    desc="${plugin_info#*:}"
    printf "  %-25s %s\n" "$name" "$desc"
  done
}

install_plugin() {
  local plugin_name="$1"
  local plugin_dir="$PLUGINS_DIR/$plugin_name"

  if [ ! -d "$plugin_dir" ]; then
    echo "Error: Plugin '$plugin_name' not found at $plugin_dir"
    return 1
  fi

  echo "  === $plugin_name ==="

  # Install skills
  # Each plugin has one skill - use plugin name directly for cleaner naming
  if [ -d "$plugin_dir/skills" ]; then
    for skill_dir in "$plugin_dir/skills"/*/; do
      if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")
        target_name="$plugin_name"  # Use plugin name, not plugin--skill
        target_dir="$CLAUDE_DIR/skills/$target_name"

        echo "    skill: $skill_name → $target_name"
        rm -rf "$target_dir"
        cp -r "$skill_dir" "$target_dir"
      fi
    done
  fi

  # Install agents
  if [ -d "$plugin_dir/agents" ]; then
    for agent_file in "$plugin_dir/agents"/*.md; do
      if [ -f "$agent_file" ]; then
        agent_name=$(basename "$agent_file" .md)
        target_name="${plugin_name}--${agent_name}.md"
        target_file="$CLAUDE_DIR/agents/$target_name"

        echo "    agent: $agent_name → $target_name"
        cp "$agent_file" "$target_file"
      fi
    done
  fi

  # Install commands
  if [ -d "$plugin_dir/commands" ]; then
    for cmd_file in "$plugin_dir/commands"/*.md; do
      if [ -f "$cmd_file" ]; then
        cmd_name=$(basename "$cmd_file" .md)
        target_name="${plugin_name}--${cmd_name}.md"
        target_file="$CLAUDE_DIR/commands/$target_name"

        echo "    command: $cmd_name → $target_name"
        cp "$cmd_file" "$target_file"
      fi
    done
  fi

  # Install hooks
  if [ -d "$plugin_dir/hooks" ]; then
    shopt -s nullglob
    for hook_file in "$plugin_dir/hooks"/*.json "$plugin_dir/hooks"/*.md; do
      if [ -f "$hook_file" ]; then
        hook_name=$(basename "$hook_file")
        target_name="${plugin_name}--${hook_name}"
        target_file="$CLAUDE_DIR/hooks/$target_name"

        echo "    hook: $hook_name → $target_name"
        cp "$hook_file" "$target_file"
      fi
    done
    shopt -u nullglob
  fi
}

# Parse arguments
ALL=false
LIST=false
SELECTED=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -a|--all)
      ALL=true
      shift
      ;;
    -l|--list)
      LIST=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "Unknown option: $1"
      usage
      exit 1
      ;;
    *)
      SELECTED+=("$1")
      shift
      ;;
  esac
done

# Handle list
if [ "$LIST" = true ]; then
  list_plugins
  exit 0
fi

# Handle all
if [ "$ALL" = true ]; then
  for plugin_info in "${PLUGINS[@]}"; do
    SELECTED+=("${plugin_info%%:*}")
  done
fi

# Interactive selection if nothing specified
if [ ${#SELECTED[@]} -eq 0 ]; then
  echo "Select plugins to install (space-separated numbers, or 'all'):"
  echo ""

  i=1
  for plugin_info in "${PLUGINS[@]}"; do
    name="${plugin_info%%:*}"
    desc="${plugin_info#*:}"
    printf "  %2d) %-25s %s\n" "$i" "$name" "$desc"
    ((i++))
  done

  echo ""
  read -p "Enter selection: " selection

  if [ "$selection" = "all" ]; then
    for plugin_info in "${PLUGINS[@]}"; do
      SELECTED+=("${plugin_info%%:*}")
    done
  else
    for num in $selection; do
      if [[ "$num" =~ ^[0-9]+$ ]] && [ "$num" -ge 1 ] && [ "$num" -le ${#PLUGINS[@]} ]; then
        idx=$((num - 1))
        plugin_info="${PLUGINS[$idx]}"
        SELECTED+=("${plugin_info%%:*}")
      fi
    done
  fi
fi

# Validate selection
if [ ${#SELECTED[@]} -eq 0 ]; then
  echo "No plugins selected."
  exit 1
fi

# Create target directories
mkdir -p "$CLAUDE_DIR/skills"
mkdir -p "$CLAUDE_DIR/agents"
mkdir -p "$CLAUDE_DIR/commands"
mkdir -p "$CLAUDE_DIR/hooks"

# Install
echo ""
echo "Installing to $CLAUDE_DIR as user-defined components:"
echo ""

for plugin in "${SELECTED[@]}"; do
  install_plugin "$plugin"
  echo ""
done

echo "=== Installation Complete ==="
echo ""
echo "Components installed to:"
echo "  ~/.claude/skills/"
echo "  ~/.claude/agents/"
echo "  ~/.claude/commands/"
echo "  ~/.claude/hooks/"
echo ""
echo "Restart Claude Code to load components."
