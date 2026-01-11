# Contributing

Build cognitive extensions for Claude Code. Production patterns, decision frameworks.

## Before You Start

1. Read **CLAUDE.md** — architecture, philosophy, conventions
2. Install the extension builder: `/plugin install 1337-extension-builder@claude-1337`
3. Browse [existing plugins](https://yzavyas.github.io/claude-1337/catalog/) to understand patterns

## Plugin Structure

```
plugins/your-plugin/
├── .claude-plugin/
│   └── plugin.json      # Required: manifest
├── SKILL.md             # Required: decisions + gotchas (< 500 lines)
├── references/          # Optional: deep dives loaded on demand
├── agents/              # Optional: specialized subagents
├── hooks/               # Optional: event handlers
└── commands/            # Optional: slash commands
```

## Plugin Manifest (plugin.json)

```json
{
  "name": "your-plugin",
  "description": "What it does. Use when: specific triggers.",
  "version": "0.1.0",
  "author": {
    "name": "yourname",
    "email": "you@example.com"
  }
}
```

**Gotcha:** Component paths (agents, hooks) must be strings, not arrays. Or omit them entirely — auto-discovery works.

```json
// ❌ WRONG
{ "agents": ["./agents/"] }

// ✅ RIGHT
{ "agents": "./agents/" }

// ✅ BEST — let auto-discovery handle it
{ "name": "...", "description": "...", "version": "..." }
```

## Register in Marketplace

Add to `.claude-plugin/marketplace.json`:

```json
{
  "name": "your-plugin",
  "source": "./plugins/your-plugin",
  "description": "Brief description. Use when: triggers."
}
```

Add display metadata to `.claude-plugin/metadata.json`:

```json
{
  "your-plugin": {
    "displayName": "Your Plugin",
    "category": "language|tooling|documentation|testing|foundation|meta"
  }
}
```

## Quality Standards

| Do | Don't |
|----|-------|
| Fill gaps (what Claude doesn't know) | Teach basics |
| Decision frameworks + gotchas | Complete tutorials |
| Cite evidence (production usage) | State opinions |
| Tables and trees | Verbose prose |
| < 500 lines SKILL.md | Monolithic files |

## Validation

Always validate before submitting:

```bash
# Validate plugin manifest
claude plugin validate ./plugins/your-plugin

# Run all plugin tests
cd evals && uv run pytest tests/test_plugins.py -v
```

PRs automatically run:
- Plugin manifest validation
- Docs build check
- TypeScript type check

## Checklist

- [ ] `plugin.json` valid (run `claude plugin validate`)
- [ ] Description < 600 chars with "Use when:" triggers
- [ ] SKILL.md is decisions, not tutorial (< 500 lines)
- [ ] Each recommendation has evidence
- [ ] Claims traceable to source
- [ ] References in separate files, linked not embedded
- [ ] Added to `marketplace.json` and `metadata.json`

## Commit Format

```
feat(plugin-name): brief description

Evidence or reasoning for the change.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## Local Development

```bash
# Add local marketplace for testing
/plugin marketplace add ./

# Install your plugin
/plugin install your-plugin@claude-1337

# After changes, update
/plugin update your-plugin
```

## Getting Help

- Read the [extension builder skill](plugins/1337-extension-builder/SKILL.md)
- Check [plugin-schema.md](plugins/1337-extension-builder/references/plugin-schema.md) for manifest format
- Review existing plugins for patterns

## License

MIT. By contributing, you agree your contributions will be licensed under MIT.
