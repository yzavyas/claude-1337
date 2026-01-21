# How to Contribute

Build cognitive extensions for Claude Code.

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/yzavyas/claude-1337.git
cd claude-1337

# 2. Add local marketplace
/plugin marketplace add ./

# 3. Install the extension builder
/plugin install 1337-extension-builder@claude-1337
```

---

## Create a Plugin

### 1. Structure

```
plugins/your-plugin/
├── .claude-plugin/
│   └── plugin.json      # Manifest (required)
├── SKILL.md             # Main content (required)
├── references/          # Deep dives (optional)
├── agents/              # Subagents (optional)
├── hooks/               # Event handlers (optional)
└── commands/            # Slash commands (optional)
```

### 2. Manifest

Create `.claude-plugin/plugin.json`:

```json
{
  "name": "your-plugin",
  "description": "What it does. Use when: specific triggers.",
  "version": "0.1.0"
}
```

### 3. Content

Write `SKILL.md` with:
- Decision frameworks (when to use X vs Y)
- Gotchas (what goes wrong)
- Evidence (production sources)

**Not:** tutorials, basics, verbose explanations.

### 4. Register

Add to `.claude-plugin/marketplace.json`:

```json
{
  "name": "your-plugin",
  "source": "./plugins/your-plugin",
  "description": "Brief. Use when: triggers."
}
```

Add to `.claude-plugin/metadata.json`:

```json
{
  "your-plugin": {
    "displayName": "Your Plugin",
    "category": "language"
  }
}
```

---

## Validation

```bash
# Validate manifest
claude plugin validate ./plugins/your-plugin

# Run tests
cd evals && uv run pytest tests/test_plugins.py -v
```

PRs run these automatically.

---

## Quality Checklist

| Requirement | Check |
|-------------|-------|
| `plugin.json` validates | `claude plugin validate` passes |
| Description has "Use when:" | Triggers are clear |
| SKILL.md < 500 lines | Not a monolith |
| Evidence for claims | Sources cited |
| No basics | Claude already knows |

---

## Common Gotchas

### Arrays in plugin.json

```json
// ❌ WRONG — fails validation
{ "agents": ["./agents/"] }

// ✅ RIGHT
{ "agents": "./agents/" }

// ✅ BEST — auto-discovery
{ "name": "...", "description": "...", "version": "..." }
```

### Missing "Use when:"

Bad: "Rust programming patterns"
Good: "Rust ecosystem decisions. Use when: choosing crates, async patterns, error handling."

### Too much content

If SKILL.md > 500 lines, split into references:
- Keep navigation in SKILL.md
- Move depth to `references/topic.md`

---

## Updating Plugins

```bash
# Test locally
/plugin update your-plugin

# Validate
claude plugin validate ./plugins/your-plugin

# Submit PR
git checkout -b feat/your-plugin
git add plugins/your-plugin
git commit -m "feat(your-plugin): description"
git push
```

---

## Getting Help

- [Extension Builder Skill](/explore/reference/catalog/) — methodology
- [Plugin Schema](/explore/reference/catalog/) — manifest format
- [Existing Plugins](https://github.com/yzavyas/claude-1337/tree/main/plugins) — examples

---

## License

MIT. Contributions licensed under MIT.
