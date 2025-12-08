#!/bin/bash
# claude-1337: Install atuin
# Part of terminal-1337 skill

set -e

echo "📦 Installing atuin..."
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
        brew install atuin
        ;;
    linux)
        echo "🐧 Installing on Linux..."

        # Try cargo first for atuin as it's often the best way if not using their script
        if command -v cargo &> /dev/null; then
            echo "Using cargo..."
            cargo install atuin

        # Try apt (Ubuntu/Debian) - might be missing or old
        elif command -v apt &> /dev/null; then
            echo "Using apt..."
            sudo apt update
            if ! sudo apt install -y atuin; then
                echo "❌ atuin not found in apt. Install Cargo or use official script."
                exit 1
            fi

        # Try dnf (Fedora/RHEL)
        elif command -v dnf &> /dev/null; then
            echo "Using dnf..."
            sudo dnf install -y atuin

        else
            echo "❌ No supported package manager found"
            echo "Install Rust toolchain: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
            exit 1
        fi
        ;;
esac

# Verify installation
if command -v atuin &> /dev/null; then
    echo ""
    echo "✅ atuin installed successfully!"
    echo ""
    atuin --version
    echo ""
    echo "⚡️ CRITICAL SETUP:"
    echo "  1. Add this to your ~/.zshrc (or bashrc):"
    echo "     eval \"$(atuin init zsh)\""
    echo "     # OR use the asset provided:"
    echo "     # source assets/configs/atuin-init.sh"
    echo ""
    echo "  2. Import your existing history:"
    echo "     atuin import auto"
    echo ""
    echo "  3. Register/Login (optional but recommended):"
    echo "     atuin register -u <username> -e <email>"
    echo ""
    echo "📖 Full documentation: references/atuin.md"
else
    echo ""
    echo "❌ Installation failed. atuin command not found."
    exit 1
fi
