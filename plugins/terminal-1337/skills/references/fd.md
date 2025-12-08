# fd - Complete Reference

## Overview

`fd` is a simple, fast, and user-friendly alternative to the standard `find` command. While `find` is powerful, its syntax can be esoteric (`find . -name '*pattern*'`). `fd` simplifies this to `fd pattern`. It is written in Rust and features parallel execution, colorized output, and smart defaults (respects `.gitignore`).

## Why Use This Tool?

- **Speed**: Parallel command traversal makes it significantly faster than `find` for large directory trees.
- **Features**: Regular expression support by default (or glob), smart case sensitivity, and automatic ignoring of hidden/gitignored files.
- **Developer Experience**: Concise syntax. No more remembering if it's `-name` or `-iname`. Colors by default.
- **Integration**: Specifically designed to pipe results into other tools like `rg`, `fzf`, or execute commands on results.

## Installation

See `scripts/install-fd.sh` for automated installation.

**Manual install**:
```bash
# macOS
brew install fd

# Linux (Ubuntu/Debian)
sudo apt install fd-find
# Note: Binary is often named `fdfind` on Debian/Ubuntu to avoid name collision.
# You may want to alias it: alias fd=fdfind

# Cargo
cargo install fd-find
```

## Common Usage Patterns

### Basic Usage

**Find files matching a pattern (regex by default):**
```bash
fd "pat.*tern"
```

**Find files by extension:**
```bash
fd -e md
# Find all markdown files
```

**Find files including hidden and gitignored:**
```bash
fd -H -I "config"
```

### Advanced Usage

**Execute a command for each result:**
```bash
# Convert all jpg to png
fd -e jpg -x convert {} {.}.png
```
*Syntax: `{}` is full path, `{.}` is path without extension, `{/}` is basename.*

**Delete all files matching a pattern:**
```bash
fd -H "\.DS_Store" -X rm
```
*Difference between `-x` (exec) and `-X` (exec-batch): `-x` runs once per file, `-X` runs once with all files as arguments.*

**Find files modified in the last 7 days:**
```bash
fd --changed-within 7d
```

### Integration with Other Tools

**Pipe to fzf for interactive selection:**
```bash
fd --type f | fzf
```

**Count lines of code in all Rust files:**
```bash
fd -e rs -X tokei
```

**Pass files to ripgrep (though rg searches recursively, this allows filtering files first):**
```bash
fd -e js -x rg "TODO"
```

## Command-Line Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `-H`, `--hidden` | Search hidden files/directories | `fd -H config` |
| `-I`, `--no-ignore` | Do not respect .gitignore | `fd -I build` |
| `-e`, `--extension` | Filter by file extension | `fd -e json` |
| `-p`, `--full-path` | Match against full path, not just filename | `fd -p "src/.*test"` |
| `-t`, `--type` | Filter by type (f=file, d=directory, l=symlink) | `fd -t d "src"` |
| `-x`, `--exec` | Execute command for each search result | `fd -e zip -x unzip` |
| `-X`, `--exec-batch` | Execute command once with all results | `fd -e txt -X vim` |
| `-s`, `--case-sensitive` | Case sensitive search | `fd -s "Main"` |
| `-i`, `--ignore-case` | Case insensitive search | `fd -i "img"` |
| `-g`, `--glob` | Glob-based search instead of regex | `fd -g "*.ts"` |
| `--max-depth <d>` | Limit directory traversal depth | `fd --max-depth 2` |
| `--size <size>` | Filter by file size | `fd --size +10mb` |

## Configuration

`fd` does not use a config file by default, but you can create an alias or wrapper function to set defaults.
Recent versions support a global ignore file `~/.config/fd/ignore`.

## Tips & Tricks

1.  **Shortcuts**: `fd` is smart. `fd pattern` finds pattern in current dir. `fd pattern path` finds pattern in `path`.
2.  **Excluding directories**: Use `-E` or `--exclude`.
    `fd pattern -E node_modules -E .git`
3.  **Placeholders in execution**:
    - `{}`: path (`a/b/c.txt`)
    - `{.}`: path without extension (`a/b/c`)
    - `{/}`: basename (`c.txt`)
    - `{//}`: parent directory (`a/b`)
    - `{/.}`: basename without extension (`c`)
4.  **Color control**: If you pipe `fd` to a file, it auto-disables color. To force color (e.g. for `less`), use `--color=always`.

## Gotchas & Common Issues

- **Issue**: `fd` command not found on Ubuntu.
  **Solution**: It is often installed as `fdfind`. Check `fdfind --version`. Add alias `alias fd=fdfind` to your shell config.

- **Issue**: Not finding files you see in `ls`.
  **Solution**: Check if they are in `.gitignore` or hidden. Use `fd -I` (no ignore) or `fd -H` (hidden).

- **Issue**: Regex failing on simple dots.
  **Solution**: `fd` uses regex by default. `.` matches any character. To match a literal dot, escape it `\.` or use glob mode `-g`.

## See Also

- Official documentation: https://github.com/sharkdp/fd
- GitHub repository: https://github.com/sharkdp/fd
- Related tools: `find` (classic), `ripgrep` (complementary).
