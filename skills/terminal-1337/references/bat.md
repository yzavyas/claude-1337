# bat - Complete Reference

## Overview

`bat` is a `cat` clone with wings. It serves the same purpose as `cat` (concatenating and printing files) but adds syntax highlighting, Git integration, and automatic paging. It is an essential tool for reading code or configuration files directly in the terminal without opening a text editor.

## Why Use This Tool?

- **Visuals**: Syntax highlighting for a huge number of programming languages and file formats.
- **Git Integration**: Shows added/modified/removed lines in the gutter relative to the git index.
- **Developer Experience**: Automatic paging (uses `less` by default) so long files don't scroll off screen. Shows non-printable characters option.
- **Drop-in Replacement**: Mostly compatible with `cat` flags, making it easy to adopt.

## Installation

See `scripts/install-bat.sh` for automated installation.

**Manual install**:
```bash
# macOS
brew install bat

# Linux (Ubuntu/Debian)
sudo apt install bat
# Note: Binary is often named `batcat` on Debian/Ubuntu.
# You may want to alias it: alias bat=batcat

# Cargo
cargo install bat
```

## Common Usage Patterns

### Basic Usage

**Display a file with syntax highlighting:**
```bash
bat src/main.rs
```

**Concatenate files (like cat):**
```bash
bat header.md content.md > combined.md
# Note: When redirecting output, bat behaves like cat (no decorations, no color by default)
```

**Read from stdin (detects language if possible, or specify it):**
```bash
curl -s https://example.com | bat -l html
```

### Advanced Usage

**Show non-printable characters:**
```bash
bat -A file.txt
```

**Display specific lines:**
```bash
bat -r 10:20 file.txt
# Lines 10 to 20
```

**Plain mode (no decorations, pure text, but with colors if terminal supports):**
```bash
bat -p file.txt
# or -pp for absolutely raw output (like cat)
```

### Integration with Other Tools

**Use as a pager for `man`:**
```bash
export MANPAGER="sh -c 'col -bx | bat -l man -p'"
man grep
```

**Preview files in `fzf`:**
```bash
fzf --preview 'bat --style=numbers --color=always --line-range :500 {}'
```

**View `git diff` with syntax highlighting (using `delta` is better, but `bat` works):**
```bash
git show HEAD:src/main.rs | bat -l rs
```

## Command-Line Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `-l`, `--language <lang>` | Force syntax highlighting language | `bat -l json data.txt` |
| `-p`, `--plain` | Show plain style (no line numbers/grid) | `bat -p file` |
| `-n`, `--number` | Show only line numbers (alias for `--style=numbers`) | `bat -n file` |
| `-r`, `--line-range` | Show specific lines | `bat -r 1:10 file` |
| `-A`, `--show-all` | Show non-printable characters | `bat -A file` |
| `--theme <theme>` | specific syntax theme | `bat --theme GitHub file` |
| `--list-languages` | List supported languages | `bat --list-languages` |
| `--list-themes` | List supported themes | `bat --list-themes` |
| `--paging <when>` | Control paging (auto, never, always) | `bat --paging=never` |

## Configuration

**Config file location**: `~/.config/bat/config`.

**Common settings**:
```
# Set the theme
--theme="TwoDark"

# Show line numbers, git changes and file header
--style="numbers,changes,header"

# Use italic text
--italic-text=always
```

**Adding themes/syntaxes**:
You can add new themes and syntaxes to `~/.config/bat/themes` and `~/.config/bat/syntaxes`, then run `bat cache --build`.

## Tips & Tricks

1.  **Tail with highlighting**: `bat` is not `tail`, but you can pipe tail to it.
    `tail -f access.log | bat --paging=never -l log`
2.  **Integration with `find -exec`**:
    `find . -name "*.py" -exec bat {} +`
3.  **Git Diff filter**: While `delta` is the specialized tool for this, `bat` can be used to view older versions of files nicely.
    `git show v1.0:README.md | bat -l md`

## Gotchas & Common Issues

- **Issue**: Outputting control characters when piped.
  **Solution**: `bat` detects pipes and disables decorations, but if you force color/style with flags, it might break downstream tools.

- **Issue**: `bat` command not found on Ubuntu.
  **Solution**: Check for `batcat`. Alias it: `alias bat=batcat`.

- **Issue**: Colors look wrong.
  **Solution**: Check your terminal's color support (truecolor) or try a different theme `bat --list-themes`.

## See Also

- Official documentation: https://github.com/sharkdp/bat
- Related tools: `delta` (git pager by same author), `cat` (original).
