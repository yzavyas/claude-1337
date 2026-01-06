# fzf - Complete Reference

## Overview

`fzf` is a general-purpose command-line fuzzy finder. It allows you to interactively filter any list of items (files, command history, processes, git commits, etc.) using fuzzy matching. It is famously composable and serves as the engine for thousands of terminal workflows.

## Why Use This Tool?

- **Speed**: extremely fast, written in Go. Can handle lists of millions of items.
- **Interactivity**: Turns any static list into an interactive selection menu.
- **Developer Experience**: dramatically speeds up navigation and recall. "I know it's called 'user'... something" -> `fzf` finds it.
- **Integration**: Can be dropped into almost any script or command chain.

## Installation

See `scripts/install-fzf.sh` for automated installation.

**Manual install**:
```bash
# macOS
brew install fzf
$(brew --prefix)/opt/fzf/install

# Linux
sudo apt install fzf
# or
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

## Common Usage Patterns

### Basic Usage

**Select a file from the current directory tree:**
```bash
fzf
```

**Filter a list from stdin:**
```bash
find . -type f | fzf
```

**Select a command from history:**
```bash
# Usually bound to Ctrl+R
history | fzf
```

### Advanced Usage

**Multi-select (use TAB to select multiple items):**
```bash
fzf -m
```

**Preview file content while selecting:**
```bash
fzf --preview 'bat --style=numbers --color=always {}'
```

**Using fzf to kill processes:**
```bash
# Type 'chrome' then select processes to kill
ps -ef | fzf -m | awk '{print $2}' | xargs kill -9
```

### Integration with Other Tools

**Opening file in editor:**
```bash
vim $(fzf)
```

**Git branch selection:**
```bash
git checkout $(git branch | fzf)
```

**Environment variables:**
```bash
export env_var=$(env | fzf | cut -d= -f1)
```

## Command-Line Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `-m`, `--multi` | Enable multi-select (TAB/Shift-TAB) | `fzf -m` |
| `--preview <cmd>` | Execute command for current line | `fzf --preview 'cat {}'` |
| `--preview-window` | Configure preview window layout | `fzf --preview-window=up:30%` |
| `-q`, `--query <str>` | Start with query string | `fzf -q "initial"` |
| `-f`, `--filter <str>` | Filter mode (non-interactive) | `fzf -f "match"` |
| `--bind` | Custom keybindings | `fzf --bind 'ctrl-d:preview-page-down'` |
| `--reverse` | Layout from top down | `fzf --reverse` |
| `--height` | limit height of window | `fzf --height 40%` |
| `--header` | Show header text | `fzf --header "Select file"` |

## Configuration

`fzf` is configured via environment variables, primarily `FZF_DEFAULT_OPTS` and `FZF_DEFAULT_COMMAND`.

**Common settings (in `.zshrc`/`.bashrc`):**

**1. Set default command to use `fd` (faster, respects gitignore):**
```bash
export FZF_DEFAULT_COMMAND='fd --type f --strip-cwd-prefix --hidden --follow --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
```

**2. UI customization:**
```bash
export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border'
```

**Keybindings (Shell Integration):**
- **CTRL-T**: Paste the selected file path(s) into the command line.
- **CTRL-R**: Paste the selected command from history.
- **ALT-C**: cd into the selected directory.

## Tips & Tricks

1.  **Fuzzy Matching Syntax**:
    - `sbtrkt`: fuzzy match
    - `'wild`: exact match (quote)
    - `^music`: prefix match
    - `.mp3$`: suffix match
    - `!fire`: inverse match
2.  **Preview Scrolling**: You can scroll the preview window! Default bindings are usually Shift-Up/Down or mouse wheel.
3.  **Trigger Sequence**: In zsh/bash with integration, you can type `vim **<TAB>` to trigger fzf for file completion anywhere.

## Gotchas & Common Issues

- **Issue**: Keybindings (Ctrl+R, etc.) not working.
  **Solution**: You likely skipped the shell integration step. Check if `[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh` (or similar) is in your shell config.

- **Issue**: Not showing hidden files.
  **Solution**: `fzf` relies on the input command. If `find` or `fd` doesn't send hidden files, `fzf` won't see them. Update `FZF_DEFAULT_COMMAND`.

## See Also

- Official documentation: https://github.com/junegunn/fzf
- Wiki (Examples): https://github.com/junegunn/fzf/wiki/examples
- Related tools: `fd`, `ripgrep`.
