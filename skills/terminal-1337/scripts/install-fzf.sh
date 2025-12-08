#!/bin/bash
# claude-1337: Install fzf
# Part of terminal-1337 skill

set -e

echo "📦 Installing fzf..."
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

# Install based on OS
case $OS in
    macos)
        echo "🍎 Installing on macOS via Homebrew..."
        if ! command -v brew &> /dev/null; then
            echo "❌ Homebrew not found. Install from: https://brew.sh"
            exit 1
        fi
        brew install fzf
        # Run the install script to set up keybindings if needed
        $(brew --prefix)/opt/fzf/install --all --no-bash --no-zsh --no-fish || true
        ;;
    linux)
        echo "🐧 Installing on Linux..."

        # Try apt first (Ubuntu/Debian)
        if command -v apt &> /dev/null; then
            echo "Using apt..."
            sudo apt update
            sudo apt install -y fzf

        # Try dnf (Fedora/RHEL)
        elif command -v dnf &> /dev/null; then
            echo "Using dnf..."
            sudo dnf install -y fzf

        # Fallback to cargo if package not in repos (fzf is usually Go, but...)
        # fzf is not in cargo. It's written in Go.
        # We can try git clone if all else fails?
        # But following template, we can fallback to git?
        # Template says "Fallback to cargo...". I'll remove cargo fallback for fzf and suggest git.
        
        else
            echo "❌ No supported package manager found"
            echo "Install manually: git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf && ~/.fzf/install"
            exit 1
        fi
        ;;
esac

# Verify installation
if command -v fzf &> /dev/null; then
    echo ""
    echo "✅ fzf installed successfully!"
    echo ""
    fzf --version
    echo ""
    echo "📚 Quick start:"
    echo "  Ctrl+R               # Search history"
    echo "  Ctrl+T               # Search files"
    echo "  kill <tab>           # Fuzzy kill"
    echo ""
    echo "⚡️ Setup:"
    echo "  To enable keybindings, add this to your shell config:"
    echo "  [ -f ~/.fzf.zsh ] && source ~/.fzf.zsh"
    echo ""
    echo "📖 Full documentation: references/fzf.md"
else
    echo ""
    echo "❌ Installation failed. fzf command not found."
    exit 1
fi
