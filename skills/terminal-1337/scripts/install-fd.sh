#!/bin/bash
# claude-1337: Install fd
# Part of terminal-1337 skill

set -e

echo "📦 Installing fd..."
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
        brew install fd
        ;;
    linux)
        echo "🐧 Installing on Linux..."

        # Try apt first (Ubuntu/Debian)
        if command -v apt &> /dev/null; then
            echo "Using apt..."
            sudo apt update
            sudo apt install -y fd-find
            
            # Handle fdfind -> fd naming
            if ! command -v fd &> /dev/null && command -v fdfind &> /dev/null; then
                 echo "⚠️  Installed as 'fdfind'. Creating user-local symlink 'fd'..."
                 mkdir -p "$HOME/.local/bin"
                 ln -sf "$(which fdfind)" "$HOME/.local/bin/fd"
                 echo "Ensure $HOME/.local/bin is in your PATH."
            fi

        # Try dnf (Fedora/RHEL)
        elif command -v dnf &> /dev/null; then
            echo "Using dnf..."
            sudo dnf install -y fd-find

        # Fallback to cargo if package not in repos
        elif command -v cargo &> /dev/null; then
            echo "Using cargo..."
            cargo install fd-find

        else
            echo "❌ No supported package manager found"
            echo "Install Rust toolchain: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
            exit 1
        fi
        ;;
esac

# Verify installation
if command -v fd &> /dev/null; then
    echo ""
    echo "✅ fd installed successfully!"
    echo ""
    fd --version
    echo ""
    echo "📚 Quick start:"
    echo "  fd pattern           # Find files matching pattern"
    echo "  fd -e md             # Find markdown files"
    echo ""
    echo "📖 Full documentation: references/fd.md"
else
    echo ""
    echo "❌ Installation failed. fd command not found."
    if [[ "$OS" == "linux" ]]; then
        echo "Check if 'fdfind' is installed and consider aliasing it to 'fd'."
    fi
    exit 1
fi
