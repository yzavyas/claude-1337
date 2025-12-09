#!/bin/bash
# claude-1337: Terminal Tools Installation Script
# Installs elite terminal tools for terminal-1337 skill

set -e

echo "🚀 claude-1337: Installing elite terminal tools"
echo ""

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
fi

echo "📦 Detected OS: $OS"
echo ""

# Check if Homebrew is available (works on both macOS and Linux)
if command -v brew &> /dev/null; then
    PACKAGE_MANAGER="brew"
    echo "✅ Using Homebrew"
elif command -v apt &> /dev/null; then
    PACKAGE_MANAGER="apt"
    echo "✅ Using apt"
elif command -v dnf &> /dev/null; then
    PACKAGE_MANAGER="dnf"
    echo "✅ Using dnf"
else
    echo "❌ No supported package manager found (brew, apt, dnf)"
    exit 1
fi

echo ""
echo "Installing tools..."
echo ""

# Install based on package manager
case $PACKAGE_MANAGER in
    brew)
        echo "📦 Installing via Homebrew..."
        brew install ripgrep fd bat eza fzf jq xh atuin
        ;;
    apt)
        echo "📦 Installing via apt..."
        sudo apt update
        sudo apt install -y ripgrep fd-find bat fzf jq

        # eza, xh, atuin not in apt repos - install via cargo
        if ! command -v cargo &> /dev/null; then
            echo "⚠️  cargo not found. Installing rustup..."
            curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
            source "$HOME/.cargo/env"
        fi

        echo "📦 Installing eza, xh via cargo..."
        cargo install eza xh

        echo "📦 Installing atuin via script..."
        bash <(curl https://raw.githubusercontent.com/atuinsh/atuin/main/install.sh)
        ;;
    dnf)
        echo "📦 Installing via dnf..."
        sudo dnf install -y ripgrep fd-find bat fzf jq

        # eza, xh, atuin not in dnf repos - install via cargo
        if ! command -v cargo &> /dev/null; then
            echo "⚠️  cargo not found. Installing rustup..."
            curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
            source "$HOME/.cargo/env"
        fi

        echo "📦 Installing eza, xh via cargo..."
        cargo install eza xh

        echo "📦 Installing atuin via script..."
        bash <(curl https://raw.githubusercontent.com/atuinsh/atuin/main/install.sh)
        ;;
esac

echo ""
echo "✅ Installation complete!"
echo ""
echo "🔧 Post-installation steps:"
echo ""
echo "1. Add atuin to your shell config (~/.zshrc or ~/.bashrc):"
echo "   eval \"\$(atuin init zsh)\"  # for zsh"
echo "   eval \"\$(atuin init bash)\" # for bash"
echo ""
echo "2. Reload your shell:"
echo "   source ~/.zshrc  # or source ~/.bashrc"
echo ""
echo "3. Import existing history:"
echo "   atuin import auto"
echo ""
echo "4. Verify installations:"
echo "   rg --version && fd --version && bat --version && eza --version"
echo "   fzf --version && jq --version && xh --version && atuin --version"
echo ""
echo "🎉 You're now ready to use terminal-1337 with Claude Code!"
