# atuin - Complete Reference

## Overview

`atuin` replaces your existing shell history (Ctrl-R) with a SQLite-backed, syncable, and encrypted history database. It records additional context (exit code, directory, execution time) and allows you to sync your shell history across all your machines securely.

## Why Use This Tool?

- **Memory**: Never lose a command again. Standard history files have limits; atuin is a database.
- **Sync**: Type a command on your laptop, press Up-Arrow on your server. It's magic.
- **Context**: Search by "commands I ran in this directory" or "commands that failed".
- **Privacy**: End-to-end encryption. The server (even if self-hosted) cannot read your history.

## Installation

See `scripts/install-atuin.sh` for automated installation.

**Manual install**:
```bash
# macOS
brew install atuin

# Linux (Cargo recommended)
cargo install atuin

# Official Script
curl --proto '=https' --tlsv1.2 -sSf https://setup.atuin.sh | sh
```

## Common Usage Patterns

### Basic Usage

**Search history (Interactive):**
Press `Ctrl+R` (or `Up` arrow if configured).

**Search via command line:**
```bash
atuin search "docker"
```

**Search commands run in current directory only:**
```bash
atuin search --cwd . "make"
```

### Advanced Usage

**View history stats:**
```bash
atuin stats
```

**Delete a command from history:**
In the UI, press `Ctrl+D` (or `Delete`).
Or CLI:
```bash
atuin history delete --pattern "secret_key"
```

**Sync manually:**
```bash
atuin sync
```

### Integration with Other Tools

**Disable atuin for a session (e.g. for screencasting):**
```bash
export ATUIN_NOBIND="true"
```

**Prevent a command from being logged:**
Start command with a space (standard shell feature, atuin respects it).

## Command-Line Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `search` | Interactive or non-interactive search | `atuin search foo` |
| `history` | Manage history manipulation | `atuin history list` |
| `stats` | Show usage statistics | `atuin stats` |
| `sync` | Force sync with server | `atuin sync` |
| `login` | Login to sync server | `atuin login` |
| `register` | Register account | `atuin register` |
| `import` | Import legacy history file | `atuin import auto` |

## Configuration

**Config file location**: `~/.config/atuin/config.toml`.

**Common settings**:
```toml
# Store failure commands?
show_preview = true

# Search mode: prefix, full-text, fuzzy
search_mode = "fuzzy"

# Keybinding style (vim/emacs)
keymap_mode = "vim"
```

## Tips & Tricks

1.  **Filter by exit code**: You can search for commands that failed.
    `atuin search --exit 1`
2.  **Time travel**: Search commands run yesterday.
    `atuin search --after "yesterday"`
3.  **Sync setup**:
    - Machine A: `atuin register -u <user> -e <email>` -> gives you a key.
    - Machine B: `atuin login -u <user>` -> asks for key.
    - Copy key from A (`atuin key`) to B.

## Gotchas & Common Issues

- **Issue**: `Ctrl+R` not working.
  **Solution**: You must add `eval "$(atuin init zsh)"` (or bash) to your shell config.

- **Issue**: History missing after install.
  **Solution**: You need to import your old history file once. Run `atuin import auto`.

- **Issue**: Database locked.
  **Solution**: Rare SQLite issue. Usually happens if multiple shells try to write exactly at once or NFS is involved. Usually resolves itself or kill the stuck process.

## See Also

- Official documentation: https://docs.atuin.sh/
- GitHub repository: https://github.com/atuinsh/atuin
