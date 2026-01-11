# Contributing

Build cognitive extensions for Claude Code.

**Full guide:** [yzavyas.github.io/claude-1337/explore/how-to/contribute/](https://yzavyas.github.io/claude-1337/explore/how-to/contribute/)

## Quick Start

```bash
# Add local marketplace
/plugin marketplace add ./

# Install extension builder
/plugin install 1337-extension-builder@claude-1337

# Validate your plugin
claude plugin validate ./plugins/your-plugin
```

## Structure

```
plugins/your-plugin/
├── .claude-plugin/plugin.json   # Manifest
├── SKILL.md                     # Main content (< 500 lines)
└── references/                  # Deep dives
```

## Checklist

- [ ] `claude plugin validate` passes
- [ ] Description has "Use when:" triggers
- [ ] SKILL.md is decisions, not tutorials
- [ ] Claims have evidence

## License

MIT
