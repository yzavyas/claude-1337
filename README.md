# claude-1337

A marketplace of cognitive extensions for Claude Code.

📚 **[Documentation](https://yzavyas.github.io/claude-1337/)** · 🔍 **[Catalog](https://yzavyas.github.io/claude-1337/catalog/)** · 💡 **[Ethos](https://yzavyas.github.io/claude-1337/ethos/)**

## Install

Three options depending on your setup:

### Option 1: Marketplace (recommended)

```
/plugin marketplace add yzavyas/claude-1337
/plugin install core-1337@claude-1337
```

### Option 2: Direct copy

Clone and copy plugins directly to `~/.claude/plugins/`:

```bash
git clone https://github.com/yzavyas/claude-1337.git
cd claude-1337
./install-plugins.sh --all        # Install all plugins
./install-plugins.sh core-1337    # Or specific ones
./install-plugins.sh --list       # See available plugins
```

### Option 3: Workaround hook

If marketplace plugins don't auto-load ([#14815](https://github.com/anthropics/claude-code/issues/14815), [#14061](https://github.com/anthropics/claude-code/issues/14061), [#15369](https://github.com/anthropics/claude-code/issues/15369)):

```bash
# After Option 1
~/.claude/plugins/marketplaces/claude-1337/install-workaround.sh
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) or the [contributor guide](https://yzavyas.github.io/claude-1337/explore/how-to/contribute/).

## License

MIT
