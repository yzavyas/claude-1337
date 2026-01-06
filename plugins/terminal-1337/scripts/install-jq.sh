#!/bin/bash
# claude-1337: Install jq
# Part of terminal-1337 skill

set -e

echo "📦 Installing jq..."
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
        brew install jq
        ;;
    linux)
        echo "🐧 Installing on Linux..."

        # Try apt first (Ubuntu/Debian)
        if command -v apt &> /dev/null; then
            echo "Using apt..."
            sudo apt update
            sudo apt install -y jq

        # Try dnf (Fedora/RHEL)
        elif command -v dnf &> /dev/null; then
            echo "Using dnf..."
            sudo dnf install -y jq

        # Fallback to cargo if package not in repos (jq is C, so cargo install jq-rs? No.)
        # We will just fail if no package manager.
        
        else
            echo "❌ No supported package manager found"
            exit 1
        fi
        ;;
esac

# Verify installation
if command -v jq &> /dev/null; then
    echo ""
    echo "✅ jq installed successfully!"
    echo ""
    jq --version
    echo ""
    echo "📚 Quick start:"
    echo "  echo '{\"a\":1}' | jq .a    # Extract value"
    echo "  cat data.json | jq .         # Pretty print"
    echo ""
    echo "📖 Full documentation: references/jq.md"
else
    echo ""
    echo "❌ Installation failed. jq command not found."
    exit 1
fi
