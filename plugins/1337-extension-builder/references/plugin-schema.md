# Plugin Manifest Schema

Valid schema for `.claude-plugin/plugin.json` in Claude Code plugins.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Plugin identifier (kebab-case) |
| `description` | string | What it does, include "Use when:" triggers |
| `version` | string | Semver (e.g., "0.1.0") |

## Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `author` | object | `{ name: string, email?: string }` |
| `homepage` | string | URL |
| `repository` | string | URL |
| `license` | string | SPDX identifier |
| `keywords` | string[] | Search terms |

## Component Paths

These are **auto-discovered** by default. Only specify if using non-standard locations.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `commands` | string | `"./commands"` | Path to commands directory |
| `agents` | string | `"./agents"` | Path to agents directory |
| `hooks` | string | `"./hooks"` | Path to hooks directory |
| `skills` | string | `"./"` | Path to skills (SKILL.md) |

---

## Gotchas

### Arrays Are Invalid

```json
// ❌ WRONG - will fail validation
{
  "agents": ["./agents/"]
}

// ✅ CORRECT - string path
{
  "agents": "./agents/"
}
```

### Auto-Discovery Preferred

If your structure is standard, **omit component paths entirely**:

```
plugin/
├── .claude-plugin/
│   └── plugin.json
├── SKILL.md           ← auto-discovered
├── agents/            ← auto-discovered
│   └── my-agent.md
├── hooks/             ← auto-discovered
│   └── hooks.json
└── commands/          ← auto-discovered
    └── my-command.md
```

```json
// ✅ BEST - rely on auto-discovery
{
  "name": "my-plugin",
  "description": "What it does. Use when: specific trigger.",
  "version": "0.1.0"
}
```

---

## Minimal Example

```json
{
  "name": "my-plugin",
  "description": "Brief description. Use when: trigger conditions.",
  "version": "0.1.0"
}
```

## Full Example

```json
{
  "name": "my-plugin",
  "description": "Full description. Use when: building X, debugging Y.",
  "version": "0.1.0",
  "author": {
    "name": "yourname",
    "email": "you@example.com"
  },
  "license": "MIT",
  "keywords": ["category", "feature"]
}
```

---

## Validation

Always validate before publishing:

```bash
claude plugin validate ./path/to/plugin
```

This catches schema errors before users hit them.

---

## Source

Claude Code plugin system. Schema inferred from validation errors and working examples.
