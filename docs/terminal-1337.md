# terminal-1337

> Yo dawg, I heard you like terminals, so we made terminal-1337 and taught Claude 1337 terminal tools, so you can 1337 terminal while Claude 1337 terminals in your terminal

## Overview

Teaches Claude Code to use elite terminal tools instead of basic Unix utilities.

**Tools:**
- `ripgrep` (`rg`) - Fast code search
- `fd` - Fast file finding
- `bat` - File viewing with syntax highlighting
- `eza` - Directory listing with Git status
- `fzf` - Fuzzy finding
- `xh` - HTTP client
- `jq` - JSON processing
- `atuin` - Shell history

## How It Works

The skill enables Claude to:
1. Detect what's installed on your system
2. Use elite tools automatically when available
3. Educate you on tool benefits before suggesting installation
4. Ask permission before installing anything
5. Remember if you decline and use fallback tools
6. Work faster through modern Rust-based utilities

## Installation

### 1. Install the Skill

```bash
# Method 1: Copy to Claude Code skills directory
cp -r skills/terminal-1337 ~/.claude/skills/

# Method 2: Load the packaged .skill file in Claude Code
# (after packaging with package_skill.py)
```

### 2. Install Tools

Tools are installed individually via scripts:

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

**Note:** Scripts auto-detect your OS (macOS/Linux) and use appropriate package managers.

## Usage

Once installed, Claude Code automatically:
- Uses `rg` instead of `grep` for searching
- Uses `fd` instead of `find` for file finding
- Uses `bat` instead of `cat` for viewing files
- Uses `eza` instead of `ls` for directory listing
- And so on...

If a tool isn't installed, Claude will:
1. Explain why it's better (1-2 sentences)
2. Show quick usage examples
3. Ask if you want to install it
4. Run the install script if you approve
5. Use standard fallback tools if you decline

## Examples

### Code Search
```bash
# Before: grep -r "TODO" .
# After:  rg "TODO"          # 10x faster, respects .gitignore
```

### File Finding
```bash
# Before: find . -name "*.ts"
# After:  fd -e ts            # Simpler syntax, faster
```

### File Viewing
```bash
# Before: cat config.json
# After:  bat config.json     # Syntax highlighting, line numbers
```

### Directory Listing
```bash
# Before: ls -la
# After:  eza -la --git       # Icons, Git status, better colors
```

## Tool Details

For comprehensive documentation on each tool, see the `references/` directory in the skill:

- `references/ripgrep.md` - Complete ripgrep guide
- `references/fd.md` - Complete fd guide
- `references/bat.md` - Complete bat guide
- `references/eza.md` - Complete eza guide
- `references/fzf.md` - Complete fzf guide
- `references/xh.md` - Complete xh guide
- `references/jq.md` - Complete jq guide
- `references/atuin.md` - Complete atuin guide

Each reference doc includes:
- Overview and benefits
- Installation instructions
- Common usage patterns
- Command-line options reference
- Configuration examples
- Tips & tricks
- Gotchas and solutions

## Status

**Current**: Alpha - Being hardened for initial release

## License

MIT
