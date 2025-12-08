#!/bin/bash
# claude-1337: Install ripgrep
# Part of terminal-1337 skill

set -e

echo "📦 Installing ripgrep..."
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
        brew install ripgrep
        ;;
    linux)
        echo "🐧 Installing on Linux..."

        # Try apt first (Ubuntu/Debian)
        if command -v apt &> /dev/null; then
            echo "Using apt..."
            sudo apt update
            sudo apt install -y ripgrep

        # Try dnf (Fedora/RHEL)
        elif command -v dnf &> /dev/null; then
            echo "Using dnf..."
            sudo dnf install -y ripgrep

        # Fallback to cargo if package not in repos
        elif command -v cargo &> /dev/null; then
            echo "Using cargo..."
            cargo install ripgrep

        else
            echo "❌ No supported package manager found"
            echo "Install Rust toolchain: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
            exit 1
        fi
        ;;
esac

# Verify installation
if command -v rg &> /dev/null; then
    echo ""
    echo "✅ ripgrep installed successfully!"
    echo ""
    rg --version
    echo ""
    echo "📚 Quick start:"
    echo "  rg 'pattern' .       # Search in current dir"
    echo "  rg -tpy 'foo'        # Search in Python files"
    echo ""
    echo "📖 Full documentation: references/ripgrep.md"
else
    echo ""
    echo "❌ Installation failed. ripgrep command not found."
    exit 1
fi
