# eza - Complete Reference

## Overview

`eza` is a modern, maintained replacement for `ls`. It lists directory contents with color, icons, and extra metadata. It uses colors to distinguish file types and permissions, and knows about Symlinks, Git, and Extended Attributes.
*Note: `eza` is the active community fork of the unmaintained `exa`.*

## Why Use This Tool?

- **Visuals**: Beautiful default coloring and optional icons (`--icons`) make parsing file lists instant.
- **Git Integration**: Shows git status (dirty, ignored, new) directly in the file list (`--git`).
- **Features**: Built-in tree view (`--tree`), distinct display for symlinks, and extended attributes support.
- **Speed**: Faster than `ls` for large directories in some cases, and significantly more feature-rich.

## Installation

See `scripts/install-eza.sh` for automated installation.

**Manual install**:
```bash
# macOS
brew install eza

# Linux
# Cargo is recommended as distro packages vary
cargo install eza

# Ubuntu/Debian (if package available)
sudo apt install eza
```

## Common Usage Patterns

### Basic Usage

**List files (grid view, like ls):**
```bash
eza
```

**Long listing (permissions, size, date):**
```bash
eza -l
```

**Show icons (requires Nerd Font):**
```bash
eza --icons
```

### Advanced Usage

**Tree view (like `tree` command):**
```bash
eza --tree
# Limit depth
eza --tree --level=2
```

**Git integration (show git status in long view):**
```bash
eza -l --git
# Shows 'N' (New), 'M' (Modified), 'I' (Ignored) in output
```

**Sort by modified date (newest first):**
```bash
eza -s modified
```
*Note: standard `ls` uses `-t`. `eza` uses `-s`.*

**Filter by file type:**
```bash
eza -D  # Only directories
eza -f  # Only files
```

### Integration with Other Tools

**Use as a preview for fzf:**
```bash
fzf --preview 'eza --tree --color=always {}'
```

**Alias `ls`:**
Many users alias `ls` to `eza`.
```bash
alias ls='eza'
alias ll='eza -l --icons --git'
alias la='eza -la --icons --git'
alias lt='eza --tree --level=2 --icons'
```

## Command-Line Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `-l`, `--long` | Display extended file metadata | `eza -l` |
| `-a`, `--all` | Show hidden files | `eza -a` |
| `-T`, `--tree` | Recurse into directories as a tree | `eza -T` |
| `--icons` | Display icons (needs Nerd Font) | `eza --icons` |
| `--git` | List git status for files | `eza -l --git` |
| `-s`, `--sort <field>` | Sort by field (name, size, ext, modified, etc) | `eza -s size` |
| `-r`, `--reverse` | Reverse sort order | `eza -s size -r` |
| `-D`, `--only-dirs` | List only directories | `eza -D` |
| `-f`, `--only-files` | List only files | `eza -f` |
| `--group-directories-first` | List directories before files | `eza --group-directories-first` |
| `--color-scale` | Color file sizes/dates by magnitude | `eza -l --color-scale` |

## Configuration

`eza` uses environment variables for some configuration, specifically colors (`EXA_COLORS` or `EZA_COLORS` and `LS_COLORS`).
There is no dedicated config file, usage relies on aliases.

## Tips & Tricks

1.  **Header**: Use `-h` or `--header` in long view to see column names.
    `eza -lh`
2.  **Time styles**: `eza` can show relative dates.
    `eza -l --time-style=relative` -> "2 days ago"
3.  **Git ignore**: `eza` can respect `.gitignore` with `--git-ignore`.
    `eza --git-ignore` (Hides gitignored files)

## Gotchas & Common Issues

- **Issue**: Icons looking like boxes.
  **Solution**: You must use a "Nerd Font" (patched font) in your terminal emulator.

- **Issue**: `ls` flags don't work.
  **Solution**: `eza` is not 100% flag compatible with `ls` (e.g., sorting). Check `eza --help`.

- **Issue**: Slow on massive network drives.
  **Solution**: `eza` reads more metadata than `ls`. Avoid `--git` on slow mounts.

## See Also

- Official documentation: https://github.com/eza-community/eza
- Related tools: `ls`, `tree`.
