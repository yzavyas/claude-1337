#!/bin/bash
# claude-1337: Install bat
# Part of terminal-1337 skill

set -e

echo "📦 Installing bat..."
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
        brew install bat
        ;;
    linux)
        echo "🐧 Installing on Linux..."

        # Try apt first (Ubuntu/Debian)
        if command -v apt &> /dev/null; then
            echo "Using apt..."
            sudo apt update
            sudo apt install -y bat
            
            # Handle batcat -> bat naming
            if ! command -v bat &> /dev/null && command -v batcat &> /dev/null; then
                 echo "⚠️  Installed as 'batcat'. Creating user-local symlink 'bat'..."
                 mkdir -p "$HOME/.local/bin"
                 ln -sf "$(which batcat)" "$HOME/.local/bin/bat"
                 echo "Ensure $HOME/.local/bin is in your PATH."
            fi

        # Try dnf (Fedora/RHEL)
        elif command -v dnf &> /dev/null; then
            echo "Using dnf..."
            sudo dnf install -y bat

        # Fallback to cargo if package not in repos
        elif command -v cargo &> /dev/null; then
            echo "Using cargo..."
            cargo install bat

        else
            echo "❌ No supported package manager found"
            echo "Install Rust toolchain: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
            exit 1
        fi
        ;;
esac

# Verify installation
if command -v bat &> /dev/null; then
    echo ""
    echo "✅ bat installed successfully!"
    echo ""
    bat --version
    echo ""
    echo "📚 Quick start:"
    echo "  bat file.txt         # View file with syntax highlighting"
    echo "  bat -p file.txt      # Plain view (no decorations)"
    echo ""
    echo "📖 Full documentation: references/bat.md"
else
    echo ""
    echo "❌ Installation failed. bat command not found."
    if [[ "$OS" == "linux" ]]; then
        echo "Check if 'batcat' is installed and consider aliasing it to 'bat'."
    fi
    exit 1
fi
