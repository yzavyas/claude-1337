#!/bin/bash
# claude-1337: Install xh
# Part of terminal-1337 skill

set -e

echo "📦 Installing xh..."
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
        brew install xh
        ;;
    linux)
        echo "🐧 Installing on Linux..."

        # Try apt first (Ubuntu/Debian)
        # xh might not be in default apt.
        if command -v apt &> /dev/null; then
            echo "Using apt..."
            sudo apt update
            # Try installing. If fails, cargo.
            if ! sudo apt install -y xh; then
                echo "xh not found in apt. Trying cargo..."
                if command -v cargo &> /dev/null; then
                    cargo install xh
                else 
                    echo "❌ xh not in apt and cargo not found."
                    exit 1
                fi
            fi

        # Try dnf (Fedora/RHEL)
        elif command -v dnf &> /dev/null; then
            echo "Using dnf..."
            sudo dnf install -y xh

        # Fallback to cargo
        elif command -v cargo &> /dev/null; then
            echo "Using cargo..."
            cargo install xh

        else
            echo "❌ No supported package manager found"
            echo "Install Rust toolchain: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
            exit 1
        fi
        ;;
esac

# Verify installation
if command -v xh &> /dev/null; then
    echo ""
    echo "✅ xh installed successfully!"
    echo ""
    xh --version
    echo ""
    echo "📚 Quick start:"
    echo "  xh httpbin.org/get   # GET request"
    echo "  xh post httpbin.org/post name=val  # POST JSON"
    echo ""
    echo "📖 Full documentation: references/xh.md"
else
    echo ""
    echo "❌ Installation failed. xh command not found."
    exit 1
fi
