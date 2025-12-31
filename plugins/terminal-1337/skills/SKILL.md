---
name: terminal-1337
description: "Modern CLI tools replacing legacy Unix utilities. Use when: searching code (rg), finding files (fd), viewing files (bat), listing directories (eza), HTTP requests (xh), JSON processing (jq), command history (atuin), fuzzy selection (fzf). Detect before use, suggest installation if missing."
---

# Terminal 1337

Modern Rust-based CLI tools that outperform legacy Unix utilities.

## Tool Selection

| Task | Use | Not | Why |
|------|-----|-----|-----|
| Search code | `rg` (ripgrep) | `grep -r` | 10x faster, respects .gitignore |
| Find files | `fd` | `find` | Simpler syntax, faster |
| View files | `bat` | `cat` | Syntax highlighting, line numbers |
| List dirs | `eza` | `ls` | Git status, icons |
| HTTP requests | `xh` | `curl` | Cleaner syntax, auto-formatting |
| JSON | `jq` | manual | Query language, pretty-print |
| History | `atuin` | `history` | Searchable, synced |
| Selection | `fzf` | manual | Fuzzy find anything |

## Usage Pattern

```
1. Detect: command -v toolname >/dev/null 2>&1
2. Available → use it
3. Missing → suggest once → fallback if declined
```

## Command Quick Reference

| Legacy | Modern | Example |
|--------|--------|---------|
| `grep -r "TODO" .` | `rg "TODO"` | Parallel, ignores .git |
| `find . -name "*.ts"` | `fd -e ts` | Simpler glob syntax |
| `cat config.json` | `bat config.json` | Highlighted output |
| `ls -la` | `eza -la --git` | Shows git status |
| `curl -X POST -H "Content-Type: application/json" -d '{"name":"x"}'` | `xh POST url name=x` | Auto JSON |
| `history \| grep docker` | `atuin search docker` | Context-aware |

## Tool-Specific Patterns

### ripgrep (rg)

```bash
rg "pattern"              # Search all files
rg -t ts "import"         # TypeScript only
rg -C 3 "ERROR"           # 3 lines context
rg -l "TODO"              # Files only (no content)
rg --json "pattern"       # Machine-readable
```

### fd

```bash
fd -e ts                  # Find by extension
fd -t f "test"            # Files matching "test"
fd -t d                   # Directories only
fd -H .env                # Include hidden
fd -e ts -x bat {}        # Find + view each
```

### bat

```bash
bat file.rs               # Syntax highlighted
bat -l json < data        # Force language
bat -p file               # Plain (no line nums)
bat --diff file           # Show git diff
```

### eza

```bash
eza -la                   # Long + hidden
eza --tree -L 2           # Tree, 2 levels
eza -la --git             # With git status
eza --icons               # With file icons
```

### xh

```bash
xh GET url                # GET request
xh POST url name=value    # POST JSON
xh url Authorization:Bearer\ token  # Headers
xh --body url             # Response body only
```

### jq

```bash
jq '.'                    # Pretty print
jq '.users[].name'        # Extract field
jq -r '.id'               # Raw output (no quotes)
jq 'select(.active)'      # Filter
```

### fzf

```bash
fd -t f | fzf             # Fuzzy file picker
rg -l "" | fzf --preview "bat {}"  # With preview
history | fzf             # Search history
```

### atuin

```bash
atuin search docker       # Search commands
atuin stats               # Usage statistics
# Ctrl+R in shell         # Interactive search
```

## Installation

All Rust tools. One command, any platform:

```bash
bash scripts/install-all.sh
```

Or manually:
```bash
cargo install ripgrep fd-find bat eza xh atuin
```

Installs rustup automatically if needed. fzf/jq handled via system package manager.

## Rules

1. **Detect first** - Never assume installed
2. **Suggest once** - Don't repeat if declined
3. **Always fallback** - Legacy tools work fine
4. **Use features** - Leverage syntax highlighting, git integration, etc.

For detailed tool docs: `references/{tool}.md`
