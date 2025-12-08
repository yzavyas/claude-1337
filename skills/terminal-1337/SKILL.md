---
name: terminal-1337
description: Master elite terminal tools for 10x productivity. Use when helping developers search code (ripgrep), find files (fd), view files (bat), list directories (eza), test APIs (xh), process JSON (jq), search command history (atuin), or select items interactively (fzf). Always prefer these modern Rust-based tools over standard Unix utilities when available. Educate users on benefits and ask permission before installing.
---

# Terminal 1337: Elite Terminal Superpowers

Give Claude superpowers through modern, fast terminal tools + educate developers on elite workflows.

## Overview

This skill enables Claude to:
1. **Use elite tools** when available (10x faster, better defaults)
2. **Detect what's installed** and adapt accordingly
3. **Educate developers** on tool benefits before suggesting installation
4. **Ask permission** before installing anything
5. **Remember declined installations** and use fallbacks for that project
6. **Work faster** through Rust-based modern utilities

## Core Workflow

```
User requests task (search code, find files, test API, etc.)
    ↓
Detect if elite tool available (command -v toolname)
    ↓
├─ Tool available → Use it
│
└─ Tool missing → Follow suggestion workflow:
    1. Check if tool would significantly help
    2. If yes → Educate user (why it's better + example)
    3. Ask permission to install
    4. If yes → Run install script
    5. If no → Mark tool as "declined for this project"
    6. Use fallback tool (grep, find, cat, curl, etc.)
```

## Tool Detection

Always check before using elite tools:

```bash
# Pattern for checking availability
command -v rg >/dev/null 2>&1 && echo "available" || echo "use fallback"
```

## Tool Suggestion Workflow

When a tool is missing but would help, follow this pattern:

1. **Explain the benefit** (1-2 sentences max)
2. **Show quick example** (1-2 commands)
3. **Ask permission to install**
4. **Wait for user response**

**Example:**
> "I notice you don't have `ripgrep` installed. It's 10x faster than grep, runs searches in parallel, and automatically respects .gitignore.
>
> Quick example:
> ```bash
> rg "TODO"       # Search all files
> rg -C 3 "ERROR" # Show 3 lines of context
> ```
>
> Would you like me to install it? (I'll run: `bash scripts/install-ripgrep.sh`)"

**CRITICAL**: If user declines, remember this choice for the current project/session and always use fallback tools without asking again.

## Elite Tools Quick Reference

| Tool | Replaces | Use For | Install Script |
|------|----------|---------|----------------|
| `rg` (ripgrep) | `grep` | Searching code, finding patterns | `scripts/install-ripgrep.sh` |
| `fd` | `find` | Finding files by name/extension | `scripts/install-fd.sh` |
| `bat` | `cat` | Viewing source code/configs | `scripts/install-bat.sh` |
| `eza` | `ls` | Listing directory contents | `scripts/install-eza.sh` |
| `fzf` | manual selection | Interactive fuzzy finding | `scripts/install-fzf.sh` |
| `xh` | `curl` | Testing REST APIs | `scripts/install-xh.sh` |
| `jq` | manual parsing | Processing JSON data | `scripts/install-jq.sh` |
| `atuin` | `history` | Searching command history | `scripts/install-atuin.sh` |

For detailed documentation on any tool, see `references/{tool-name}.md`

## Task-Based Usage

### Searching Code

**User asks:** "Find all TODO comments"

**Workflow:**
1. Check: `command -v rg`
2. If available: `rg -i "TODO"`
3. If not: Suggest ripgrep OR use `grep -r -i "TODO" .`

**Why ripgrep:** 10x faster, parallel search, respects .gitignore

### Finding Files

**User asks:** "Find all TypeScript files"

**Workflow:**
1. Check: `command -v fd`
2. If available: `fd -e ts`
3. If not: Suggest fd OR use `find . -name "*.ts"`

**Why fd:** Simpler syntax, faster, respects .gitignore

### Viewing Files

**User asks:** "Show me the config file"

**Workflow:**
1. Check: `command -v bat`
2. If available: `bat config.json`
3. If not: Suggest bat OR use `cat config.json`

**Why bat:** Syntax highlighting, Git integration, line numbers

### Listing Directories

**User asks:** "What's in this directory?"

**Workflow:**
1. Check: `command -v eza`
2. If available: `eza --icons -la --git`
3. If not: Suggest eza OR use `ls -la`

**Why eza:** Icons, Git status, better colors

### Testing APIs

**User asks:** "Test this API endpoint"

**Workflow:**
1. Check: `command -v xh`
2. If available: `xh POST api.com/users name=john`
3. If not: Suggest xh OR use `curl -X POST -d ...`

**Why xh:** Human-friendly syntax, auto JSON formatting

### Processing JSON

**User asks:** "Extract the user IDs from this JSON"

**Workflow:**
1. Check: `command -v jq`
2. If available: `cat data.json | jq '.users[].id'`
3. If not: Suggest jq OR use Python one-liner

**Why jq:** Powerful query language, pretty-printing

### Searching History

**User asks:** "What docker commands did I run?"

**Workflow:**
1. Check: `command -v atuin`
2. If available: `atuin search docker`
3. If not: Suggest atuin OR use `history | grep docker`

**Why atuin:** Context-aware, unlimited history, sync across machines

### Interactive Selection

**User asks:** "Let me pick a file to edit"

**Workflow:**
1. Check: `command -v fzf`
2. If available: `fd -t f | fzf | xargs bat`
3. If not: Suggest fzf OR manually list files

**Why fzf:** Real-time fuzzy search, preview pane, keyboard-driven

## Command Translation Table

Use this for quick reference when translating standard commands:

| Standard Command | Elite Alternative | Key Benefit |
|------------------|-------------------|-------------|
| `grep -r "pattern" .` | `rg "pattern"` | 10x faster, parallel |
| `find . -name "*.js"` | `fd -e js` | Simpler, faster |
| `cat file.py` | `bat file.py` | Syntax highlighting |
| `ls -la` | `eza -la --git` | Icons + Git status |
| `curl -X POST` | `xh POST` | Human-friendly |
| `history \| grep cmd` | `atuin search cmd` | Context-aware |

## Rules

1. **Always detect first** - Never assume tools are installed
2. **Educate before suggesting** - Explain why tool is better
3. **Always ask permission** - Never install without approval
4. **Remember declined choices** - Don't keep asking
5. **Always provide fallbacks** - Standard tools work too
6. **Use tool-specific features** - Leverage syntax highlighting, Git integration, etc.
7. **Keep suggestions brief** - 1-2 sentences + quick example
8. **Reference detailed docs** - Point to `references/` for deep dives

## Handling Declined Installations

If a user declines installing a tool:

1. **Acknowledge** their choice
2. **Remember** for this project/session (don't ask again)
3. **Use fallback** tool without mentioning elite alternative again
4. **Work effectively** with standard tools

**Example:**
> "No problem! I'll use `grep` instead. Here's the search..."

## Real-World Examples

### Example 1: Bug Hunt
```
User: "Find all imports of the broken module"
Claude: [Detects rg installed] rg "import.*brokenModule" --type ts
```

### Example 2: API Development
```
User: "Test the user creation endpoint"
Claude: [Detects xh installed] xh POST localhost:3000/api/users name=john email=john@test.com
Claude: [Detects jq installed] And extract the ID: xh GET localhost:3000/api/users | jq '.[0].id'
```

### Example 3: Code Exploration
```
User: "Show me the structure of the components directory"
Claude: [Detects eza installed] eza --tree src/components
Claude: [Detects bat installed] Want to see a specific file? bat src/components/Button.tsx
```

## Installation Notes

- All install scripts are in `scripts/` directory
- Scripts detect OS (macOS/Linux) and use appropriate package manager
- Some tools require Rust toolchain (scripts handle this)
- atuin requires shell config update (script provides instructions)

## Golden Rules

1. **Elite tools when available** - Use them automatically
2. **Standard tools as fallback** - Always work, even without elite tools
3. **Educate, don't pushy** - Respect user choices
4. **Fast and user-friendly** - That's why these tools exist

---

**This skill makes Claude 10x more effective** by using modern tools that are faster, more intuitive, and provide better output than traditional Unix utilities.
