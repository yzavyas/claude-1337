---
name: terminal
description: "Modern CLI tools replacing legacy Unix utilities. Use when: grep/find too slow on large codebases, find syntax confusing, need syntax highlighting in terminal, directory listings need git status, curl commands too verbose, shell history search inadequate, want fuzzy file/command selection. Detect before use, suggest installation if missing."
---

# Terminal 1337

Modern Rust-based CLI tools that outperform legacy Unix utilities.

**Production evidence:** These tools are used by major codebases. ripgrep is the default search backend in VS Code. fd is recommended by the fish shell maintainers. bat, eza, and xh are built on the same Rust CLI patterns from the ripgrep author (BurntSushi).

## Performance Evidence

| Tool | Benchmark | Source |
|------|-----------|--------|
| ripgrep | 1.7s vs 9.5s grep (with `-n`) on 13GB file | BurntSushi benchmarks |
| ripgrep | SIMD + finite automata + literal optimizations | Rust regex engine design |
| fd | ~855ms vs ~20s find (regex search, 546 files) | sharkdp/fd benchmarks |
| fd | Parallelized directory traversal + ignore crate | Same engine as ripgrep |

**Why ripgrep is faster:** Built on Rust's regex engine with finite automata, SIMD, and aggressive literal optimizations. UTF-8 decoding baked into the DFA. For simple literals, ripgrep is strictly superior to GNU grep.

**Why fd is faster:** Parallelized traversal using the same `ignore` crate as ripgrep. Sensible defaults (respects .gitignore, skips hidden files) mean less work.

**Caveat:** Performance varies by workload. GNU grep can be faster when output is `/dev/null` (exits at first match). fd is slower than find for exhaustive directory listing (`find ~ -type f` is ~2x faster than `fd -HI -t f`). For git repos, `git ls-files` beats both (5x+ faster).

## Tool Selection

| Task | Use | Not | Why |
|------|-----|-----|-----|
| Search code | `rg` (ripgrep) | `grep -r` | Parallel search, respects .gitignore — VS Code search backend |
| Find files | `fd` | `find` | Simpler syntax, sensible defaults — fish shell recommended |
| View files | `bat` | `cat` | Syntax highlighting via syntect — uses Sublime Text syntax definitions |
| List dirs | `eza` | `ls` | Git integration built-in — successor to exa |
| HTTP requests | `xh` | `curl` | HTTPie-compatible with Rust performance |
| JSON | `jq` | manual | Industry standard — used by GitHub Actions, AWS CLI |
| History | `atuin` | `history` | SQLite-backed with sync — Ellie Huxtable (maintainer) |
| Selection | `fzf` | manual | Go-based fuzzy finder — powers many TUI tools |

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

1. **Detect first** - Run `command -v toolname >/dev/null 2>&1` before use. Never assume installed.
2. **Suggest once** - If missing, offer installation once. Track declined tools in conversation context to avoid re-asking.
3. **Always fallback** - Legacy tools work fine. If user declines or tool unavailable, use grep/find/cat/ls without apology.
4. **Use features** - When tool is available, use its strengths: syntax highlighting (bat), git integration (eza), parallel search (rg), simpler syntax (fd).

## Hook Behavior

This plugin includes hooks that **suggest** modern alternatives. Following the collaborative agency principle, hooks never block commands - they inform and let you proceed.

**SessionStart hook**: Displays available modern alternatives at session start.

**PreToolUse hook**: When legacy commands like `rm` are used, suggests the modern alternative (e.g., `rip` for recoverable deletion) but allows the original command to proceed.

### Disabling Suggestions

To disable all hook suggestions, set the environment variable:

```bash
export TERMINAL_1337_SKIP_SUGGESTIONS=1
```

This silences both the session start message and per-command suggestions. The modern tools remain available for manual use.

For detailed tool docs: `references/{tool}.md`
