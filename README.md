# claude-1337

> **⚠️ Alpha**: Currently being hardened. First stable release coming soon.

Skills for Claude Code that teach it to use modern terminal tools.

## Quick Start

```bash
# Clone the repo
git clone https://github.com/yzavyas/claude-1337.git
cd claude-1337

# Install the skill (copy to Claude Code skills directory)
# Then install the tools via individual scripts as needed
```

## What's Included

### terminal-1337

Teaches Claude Code to use elite terminal tools instead of basic Unix utilities.

**[Full Documentation →](docs/terminal-1337.md)**

**Tools:**
- `ripgrep` - Fast code search
- `fd` - Fast file finding
- `bat` - File viewing with syntax highlighting
- `eza` - Directory listing with Git status
- `fzf` - Fuzzy finding
- `xh` - HTTP client
- `jq` - JSON processing
- `atuin` - Shell history

**How it works:**
- Detects what's installed
- Uses elite tools when available
- Asks permission before installing
- Falls back to standard tools if declined

## Installation

### 1. Install the Skill

Copy the skill to Claude Code:
```bash
# Method 1: Manual
cp -r skills/terminal-1337 ~/.claude/skills/

# Method 2: Use the packaged .skill file
# Load terminal-1337.skill in Claude Code (when available)
```

### 2. Install Tools

Tools are installed individually via scripts in `skills/terminal-1337/scripts/`:

```bash
# Install specific tools
bash skills/terminal-1337/scripts/install-ripgrep.sh
bash skills/terminal-1337/scripts/install-fd.sh
# ... etc

# Or install all at once
for script in skills/terminal-1337/scripts/install-*.sh; do
  bash "$script"
done
```

**Note:** Scripts detect your OS (macOS/Linux) and use appropriate package managers.

## Usage

Once installed, Claude Code automatically:
- Uses `rg` instead of `grep` for searching
- Uses `fd` instead of `find` for file finding
- Uses `bat` instead of `cat` for viewing files
- Uses `eza` instead of `ls` for directory listing
- And so on...

If a tool isn't installed, Claude will explain why it's better and ask if you want to install it.

## Project Structure

```
claude-1337/
├── skills/
│   └── terminal-1337/
│       ├── SKILL.md              # Skill instructions for Claude
│       ├── references/           # Tool documentation
│       ├── scripts/              # Install scripts
│       └── assets/               # Config snippets
├── docs/
│   └── TERMINAL_SETUP.md         # Comprehensive terminal guide
└── README.md
```

## Status

**terminal-1337**: Complete and ready to use. All 8 tools documented with install scripts.

## License

MIT

## Contributing

Currently in development. Contributions will open in the new year.
