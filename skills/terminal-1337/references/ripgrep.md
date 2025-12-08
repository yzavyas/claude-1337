# ripgrep - Complete Reference

## Overview

ripgrep (`rg`) is a line-oriented search tool that recursively searches your current directory for a regex pattern. By default, ripgrep will respect your `.gitignore` and automatically skip hidden files/directories and binary files. It is widely considered the fastest search tool available, significantly outperforming `grep`, `ack`, and `ag` (The Silver Searcher).

## Why Use This Tool?

- **Speed**: Built on Rust's regex engine, it utilizes SIMD optimizations and multi-threading to search massive codebases in milliseconds.
- **Features**: First-class support for `.gitignore`, automatic filtering of binary files, and smart case sensitivity.
- **Developer Experience**: Defaults are sane for developers (ignores `.git`, `node_modules`, etc.), colorful output, and intuitive flags.
- **Integration**: Works perfectly with `fzf` for interactive searching and integrates seamlessly into VIM/NeoVim/VSCode.

## Installation

See `scripts/install-ripgrep.sh` for automated installation.

**Manual install**:
```bash
# macOS
brew install ripgrep

# Linux (Ubuntu/Debian)
sudo apt install ripgrep
# or
cargo install ripgrep
```

## Common Usage Patterns

### Basic Usage

**Search for a string in the current directory (recursive):**
```bash
rg "function_name"
```

**Search with case insensitivity (smart case is default, strict needs flag):**
```bash
rg -i "error"
```

**Search only in specific file types:**
```bash
rg "TODO" -t py
# Equivalent to: rg "TODO" -g "*.py"
```

**List all supported file types:**
```bash
rg --type-list
```

### Advanced Usage

**Search for a pattern, showing 3 lines of context around the match:**
```bash
rg "critical_failure" -C 3
```

**Search for a pattern only in files that match a glob, excluding others:**
```bash
rg "import" -g "src/**/*.ts" -g "!**/*.test.ts"
```

**Search for files that DO NOT contain a pattern (inverse match):**
```bash
# Find all files without a license header
rg -L "Copyright"
```

**Replace occurrences (printing to stdout, not modifying files):**
```bash
rg "foo" -r "bar"
```
*Note: To actually modify files, you often combine this with `sed` or use `sd`.*

**Search using full Perl-compatible Regex (PCRE2):**
```bash
rg -P "(?<=foo)bar"
```

### Integration with Other Tools

**Interactive search with fzf:**
```bash
rg --line-number --no-heading --color=always --smart-case "pattern" | fzf --ansi
```

**Pass matching files to `sed` for replacement:**
```bash
rg -l "old_api" | xargs sed -i 's/old_api/new_api/g'
```

**Open matching files in editor (e.g., VS Code):**
```bash
rg -l "Component" | xargs code
```

## Command-Line Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `-i`, `--ignore-case` | Case insensitive search | `rg -i "foo"` |
| `-S`, `--smart-case` | Case insensitive if pattern is all lowercase | `rg -S "foo"` |
| `-w`, `--word-regexp` | Only match whole words | `rg -w "log"` |
| `-l`, `--files-with-matches` | Print only filenames of matching files | `rg -l "TODO"` |
| `-v`, `--invert-match` | Invert match (show lines NOT matching) | `rg -v "DEBUG"` |
| `-C <n>`, `--context <n>` | Show n lines of context | `rg "error" -C 3` |
| `-g`, `--glob` | Include/exclude files matching glob | `rg -g "*.js" foo` |
| `-t`, `--type` | Only search files of specific type | `rg -t rust foo` |
| `-T`, `--type-not` | Do not search files of specific type | `rg -T js foo` |
| `-F`, `--fixed-strings` | Treat pattern as literal string, not regex | `rg -F ".*"` |
| `--hidden` | Search hidden files/directories | `rg --hidden .env` |
| `--no-ignore` | Do not respect .gitignore | `rg --no-ignore secret` |
| `--stats` | Print statistics about the search | `rg foo --stats` |
| `-u`, `-uu`, `-uuu` | Unrestricted search (ignore .gitignore, hidden, binary) | `rg -uuu "key"` |

## Configuration

**Config file location**: `ripgrep` reads a config file defined by the `RIPGREP_CONFIG_PATH` environment variable.

**Common settings**:
Create a file `~/.ripgreprc`:
```
--smart-case
--hidden
--glob=!.git/*
--colors=line:style:bold
```

Then add to your shell profile (`~/.zshrc` or `~/.bashrc`):
```bash
export RIPGREP_CONFIG_PATH="$HOME/.ripgreprc"
```

## Tips & Tricks

1.  **Use `rg -uuu` for "grep everything"**: When you can't find something you know is there, `rg -uuu` disables all smart filtering (gitignore, hidden files, binary files) and acts like a raw grep.
2.  **Define custom types**: You can define custom file types on the fly.
    `rg --type-add 'web:*.{html,css,js,ts}' -t web "class"`
3.  **Multimodal search**: `rg` handles UTF-16 and other encodings automatically, making it great for searching logs or legacy files.
4.  **Structure search**: Combine with `bat` for a preview.
    `rg "foo" --json | delta` (if you have delta installed) or simpler: `rg "foo" | bat`
5.  **Sort by path**: `rg` output is non-deterministic in order due to parallelism. Use `--sort path` if you need consistent output order (slightly slower).

## Gotchas & Common Issues

- **Issue**: Not finding a file that exists.
  **Solution**: Check if it's gitignored or hidden. Use `--no-ignore` or `--hidden`. Also check `.ignore` or `.rgignore` files.

- **Issue**: Searching for a string starting with `-`.
  **Solution**: Use `--` to separate flags from the pattern. `rg -- -my-flag`.

- **Issue**: Regex not behaving as expected.
  **Solution**: Remember `rg` uses Rust regexes by default, which are similar to PCRE but lack lookarounds/backreferences. Use `-P` to enable PCRE2 if you need advanced features.

- **Issue**: Massive memory usage on huge single-line files (like minified JS).
  **Solution**: `rg` usually handles this well by not loading the whole file, but you can use `-M`/`--max-columns` to limit line length displayed. `rg -M 100` truncates long lines.

## See Also

- Official documentation: https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md
- GitHub repository: https://github.com/BurntSushi/ripgrep
- Related tools: `fd` (often used with rg), `fzf` (often used with rg).
