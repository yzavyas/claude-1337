#!/bin/bash
# claude-1337: Terminal Tools Installation Script
# Installs elite terminal tools via cargo (cross-platform)

set -e

echo "🚀 claude-1337: Installing elite terminal tools"
echo ""

# Ensure cargo is available
if ! command -v cargo &> /dev/null; then
    echo "📦 Installing Rust toolchain..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
fi

echo "✅ Using cargo $(cargo --version)"
echo ""

# Install all tools
echo "📦 Installing tools..."
cargo install ripgrep fd-find bat eza xh atuin

# fzf and jq are not Rust - handle separately
echo ""
echo "📦 Installing fzf..."
if command -v brew &> /dev/null; then
    brew install fzf jq
elif command -v apt &> /dev/null; then
    sudo apt install -y fzf jq
elif command -v dnf &> /dev/null; then
    sudo dnf install -y fzf jq
elif command -v scoop &> /dev/null; then
    scoop install fzf jq
elif command -v choco &> /dev/null; then
    choco install fzf jq -y
else
    echo "⚠️  Install fzf manually: https://github.com/junegunn/fzf#installation"
    echo "⚠️  Install jq manually: https://jqlang.github.io/jq/download/"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "🔧 Add atuin to your shell:"
echo "   eval \"\$(atuin init zsh)\"   # zsh"
echo "   eval \"\$(atuin init bash)\"  # bash"
echo ""
echo "   Then: atuin import auto"
echo ""
echo "🎉 Ready for terminal-1337!"
