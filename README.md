# claude-1337

A marketplace of cognitive extensions for Claude Code. Engineering excellence through effective collaborative intelligence.

📚 **[Documentation](https://yzavyas.github.io/claude-1337/)** · 🔍 **[Plugin Catalog](https://yzavyas.github.io/claude-1337/catalog/)**

## What Is This?

Curated skills, hooks, and agents that extend Claude Code with production-tested patterns, decision frameworks, and domain expertise. Not tutorials — decision frameworks and gotchas that fill gaps in what Claude already knows.

## Quick Start

```bash
# Add the marketplace
/plugin marketplace add yzavyas/claude-1337

# Install core methodology (recommended first)
/plugin install core-1337@claude-1337

# Browse and install others
/plugin install rust-1337@claude-1337
/plugin install eval-1337@claude-1337
```

## Available Plugins

| Plugin | Type | Description |
|--------|------|-------------|
| **core-1337** | skill | Engineering excellence methodology |
| **eval-1337** | skill | LLM evaluation frameworks |
| **rust-1337** | skill | Rust ecosystem decisions |
| **kotlin-1337** | skill | Kotlin/JVM patterns |
| **terminal-1337** | hooks | Terminal best practices |
| **sensei-1337** | skill | Documentation methodology |
| **experience-1337** | skill + hooks | Docs site patterns |
| **1337-extension-builder** | skill + agents | Build your own extensions |

See the full [catalog](https://yzavyas.github.io/claude-1337/catalog/) for all plugins.

## Philosophy

**Collaborative intelligence, not replacement.** Extensions should make you more capable, not more dependent.

- **Transparency** — See reasoning, learn patterns
- **Control** — You shape direction, Claude amplifies
- **Evidence** — Claims traced to sources
- **Compound value** — Each enhancement makes the next easier

Read the [ethos](https://yzavyas.github.io/claude-1337/ethos/) for the full framework.

## Development

```bash
# Run plugin validation
cd evals && uv run pytest tests/test_plugins.py -v

# Run docs site locally
cd experience/app && bun install && bun run dev
```

PRs run validation automatically (plugin tests, docs build, type check).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding or updating plugins.

## License

MIT
