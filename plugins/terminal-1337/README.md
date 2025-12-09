# terminal-1337

Modern CLI tools that replace legacy Unix utilities.

## Tools

| Legacy | Elite | Why |
|--------|-------|-----|
| grep | ripgrep (rg) | 10x faster, respects .gitignore |
| find | fd | Simpler syntax, faster |
| cat | bat | Syntax highlighting, line numbers |
| ls | eza | Git status, icons |
| curl | xh | Cleaner output, sensible defaults |
| history | atuin | Searchable, synced across machines |
| - | fzf | Fuzzy finder for everything |
| - | jq | JSON processing |

## How It Works

1. Detects installed tools
2. Uses elite tools when available
3. Offers to install missing ones
4. Falls back to standard tools if declined

## Examples

```bash
# Search code
rg "TODO"                    # vs grep -r "TODO" .

# Find files
fd -e ts                     # vs find . -name "*.ts"

# View file
bat config.json              # vs cat config.json

# List directory
eza -la --git                # vs ls -la
```

## Contents

```
terminal-1337/
├── skills/
│   ├── SKILL.md
│   └── references/      # Per-tool docs (ripgrep.md, fd.md, etc.)
└── scripts/             # Install scripts (install-*.sh)
```
