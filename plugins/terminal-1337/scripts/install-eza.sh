#!/bin/bash
# claude-1337: Install eza
# Part of terminal-1337 skill

set -e

echo "📦 Installing eza..."
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
        brew install eza
        ;;
    linux)
        echo "🐧 Installing on Linux..."

        # Prioritize Cargo for eza as it's often not in default repos
        if command -v cargo &> /dev/null; then
            echo "Using cargo (recommended for eza)..."
            cargo install eza

        # Try apt (Ubuntu/Debian)
        elif command -v apt &> /dev/null; then
            echo "Using apt (note: might require custom gpg keys, trying default)..."
            sudo apt update
            # eza might not be in default apt, but we try.
            if ! sudo apt install -y eza; then
                 echo "❌ eza not found in apt sources."
                 echo "💡 Recommendation: Install Rust/Cargo to install eza easily."
                 exit 1
            fi

        # Try dnf (Fedora/RHEL)
        elif command -v dnf &> /dev/null; then
            echo "Using dnf..."
            sudo dnf install -y eza

        else
            echo "❌ No supported package manager found"
            echo "Install Rust toolchain: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
            exit 1
        fi
        ;;
esac

# Verify installation
if command -v eza &> /dev/null; then
    echo ""
    echo "✅ eza installed successfully!"
    echo ""
    eza --version
    echo ""
    echo "📚 Quick start:"
    echo "  eza -l               # Long listing"
    echo "  eza --tree           # Tree view"
    echo "  eza --icons          # Show icons"
    echo ""
    echo "📖 Full documentation: references/eza.md"
else
    echo ""
    echo "❌ Installation failed. eza command not found."
    exit 1
fi
