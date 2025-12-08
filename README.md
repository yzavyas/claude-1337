# claude-1337

> **⚠️ Alpha**: Currently being hardened. First stable release coming soon.

Skills for Claude Code that teach it to use modern terminal tools.

## Quick Start

In Claude Code, run:

```
/plugin marketplace add https://github.com/yzavyas/claude-1337
```

That's it! Claude will automatically detect and use elite tools (or offer to install them).

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

## How It Works

When you add this marketplace to Claude Code:

1. Claude gains access to the `terminal-1337` skill
2. The skill automatically detects which elite tools are installed
3. Claude uses elite tools when available, or offers to install them
4. Install scripts handle OS detection and package manager selection

**No manual installation required** - just add the marketplace URL to Claude Code.

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
├── .claude-plugin/
│   └── marketplace.json          # Marketplace definition
├── plugins/
│   └── terminal-1337/            # Plugin container
│       ├── commands/             # Slash commands (future)
│       ├── agents/               # Specialized agents (future)
│       ├── hooks/                # Event hooks (future)
│       └── skills/
│           └── terminal-1337/    # The skill
│               ├── SKILL.md      # Skill instructions
│               ├── references/   # Tool documentation
│               ├── scripts/      # Install scripts
│               └── assets/       # Config snippets
├── docs/
│   └── terminal-1337.md          # Full skill documentation
└── README.md
```

## Status

**terminal-1337**: Complete and ready to use. All 8 tools documented with install scripts.

## License

MIT

## Documentation

- **[LAYOUT.md](LAYOUT.md)** - Visual reference of project structure
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guidelines for contributors
- **[CLAUDE.md](CLAUDE.md)** - Project steward for Claude instances
