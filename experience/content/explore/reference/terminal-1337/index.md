[&larr; reference](../)

modern rust-based cli tools that outperform legacy unix utilities

## install

```
/plugin install terminal-1337@claude-1337
```

## tools

| task | use | not | why |
|------|-----|-----|-----|
| search code | rg (ripgrep) | grep -r | 10x faster, respects .gitignore |
| find files | fd | find | simpler syntax, faster |
| view files | bat | cat | syntax highlighting, line numbers |
| list dirs | eza | ls | git status, icons |
| http requests | xh | curl | cleaner syntax, auto-formatting |
| json | jq | manual | query language, pretty-print |
| history | atuin | history | searchable, synced |
| selection | fzf | manual | fuzzy find anything |

## usage pattern

```
1. Detect: command -v toolname >/dev/null 2>&1
2. Available → use it
3. Missing → suggest once → fallback if declined
```

## quick reference

| legacy | modern |
|--------|--------|
| `grep -r "TODO" .` | `rg "TODO"` |
| `find . -name "*.ts"` | `fd -e ts` |
| `cat config.json` | `bat config.json` |
| `ls -la` | `eza -la --git` |
| `curl -X POST -H "..." -d '...'` | `xh POST url name=x` |
| `history | grep docker` | `atuin search docker` |

## ripgrep (rg)

```
rg "pattern"              # search all files
rg -t ts "import"         # typescript only
rg -C 3 "ERROR"           # 3 lines context
rg -l "TODO"              # files only (no content)
rg --json "pattern"       # machine-readable
```

## fd

```
fd -e ts                  # find by extension
fd -t f "test"            # files matching "test"
fd -t d                   # directories only
fd -H .env                # include hidden
fd -e ts -x bat {}        # find + view each
```

## bat

```
bat file.rs               # syntax highlighted
bat -l json < data        # force language
bat -p file               # plain (no line nums)
bat --diff file           # show git diff
```

## eza

```
eza -la                   # long + hidden
eza --tree -L 2           # tree, 2 levels
eza -la --git             # with git status
eza --icons               # with file icons
```

## xh

```
xh GET url                # GET request
xh POST url name=value    # POST JSON
xh url Authorization:Bearer\ token  # headers
xh --body url             # response body only
```

## jq

```
jq '.'                    # pretty print
jq '.users[].name'        # extract field
jq -r '.id'               # raw output (no quotes)
jq 'select(.active)'      # filter
```

## fzf

```
fd -t f | fzf             # fuzzy file picker
rg -l "" | fzf --preview "bat {}"  # with preview
history | fzf             # search history
```

## atuin

```
atuin search docker       # search commands
atuin stats               # usage statistics
# Ctrl+R in shell         # interactive search
```

## rules

1. **detect first** - never assume installed
2. **suggest once** - don't repeat if declined
3. **always fallback** - legacy tools work fine
4. **use features** - leverage syntax highlighting, git integration

## structure

```
plugins/terminal-1337/
├── skills/
│   ├── SKILL.md           # core decision logic
│   ├── references/        # per-tool docs (8 files)
│   ├── scripts/           # install scripts (8 + install-all)
│   └── assets/configs/    # shell configs (atuin-init.sh)
└── hooks/
    └── skill-eval.sh      # activation fix
```
