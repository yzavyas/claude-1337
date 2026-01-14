#!/bin/bash
# Copies selected 1337 plugins to ~/.claude/plugins/ for direct use
# This bypasses the marketplace system entirely

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGINS_DIR="$SCRIPT_DIR/plugins"
TARGET_DIR="$HOME/.claude/plugins"

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
  local name="$1"
  local source="$PLUGINS_DIR/$name"
  local target="$TARGET_DIR/$name"

  if [ ! -d "$source" ]; then
    echo "Error: Plugin '$name' not found at $source"
    return 1
  fi

  # Create target directory
  mkdir -p "$TARGET_DIR"

  # Remove existing if present
  if [ -d "$target" ]; then
    echo "  Updating $name..."
    rm -rf "$target"
  else
    echo "  Installing $name..."
  fi

  # Copy plugin
  cp -r "$source" "$target"

  echo "  ✓ $name installed to $target"
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

# Install
echo ""
echo "Installing to $TARGET_DIR:"
echo ""

for plugin in "${SELECTED[@]}"; do
  install_plugin "$plugin"
done

echo ""
echo "Done. Restart Claude Code to load plugins."
echo ""
echo "To verify: ls $TARGET_DIR"
