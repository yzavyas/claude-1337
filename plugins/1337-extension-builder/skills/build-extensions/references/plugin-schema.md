# Plugin Manifest Schema

Valid schema for `.claude-plugin/plugin.json` in Claude Code plugins.

Source: [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)

---

## Plugin Directory Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # REQUIRED - only this goes in .claude-plugin/
├── skills/                   # Skills directory (at plugin root)
│   └── skill-name/          # Subdirectory per skill
│       └── SKILL.md         # Skill file with frontmatter
├── commands/                 # Slash commands (at plugin root)
│   └── my-command.md
├── agents/                   # Agent definitions (at plugin root)
│   └── my-agent.md
├── hooks/                    # Event handlers (at plugin root)
│   └── hooks.json
├── .mcp.json                # MCP server definitions (optional)
└── .lsp.json                # LSP server configurations (optional)
```

**Critical**: Only `plugin.json` goes inside `.claude-plugin/`. Everything else at plugin root.

---

## Required Fields

Only `name` is strictly required:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Plugin identifier (kebab-case, unique) |

---

## Recommended Fields

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | What it does + "Use when:" triggers |
| `version` | string | Semver (e.g., "0.1.0") |
| `author` | object | `{ name: string, email?: string, url?: string }` |

---

## Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `homepage` | string | URL to documentation |
| `repository` | string | URL to source code |
| `license` | string | SPDX identifier |
| `keywords` | string[] | Search terms |
| `strict` | boolean | Path traversal control (default: false) |

### strict

Controls whether plugin can access files outside its directory:

| Value | Behavior |
|-------|----------|
| `false` (default) | Plugin can access sibling directories, parent paths |
| `true` | Plugin strictly contained, no external refs allowed |

Use `strict: true` for self-contained plugins. Use `strict: false` when plugin needs shared resources.

---

## Component Path Overrides

These are **auto-discovered** from standard locations. Only specify if using non-standard paths.

| Field | Type | Default Location | Description |
|-------|------|------------------|-------------|
| `commands` | string | `./commands/` | Path to commands directory |
| `agents` | string | `./agents/` | Path to agents directory |
| `skills` | string | `./skills/` | Path to skills directory |
| `hooks` | string | `./hooks/hooks.json` | Path to hooks config |
| `mcpServers` | string | `./.mcp.json` | Path to MCP config |
| `lspServers` | string | `./.lsp.json` | Path to LSP config |

---

## Gotchas

### Arrays Are Invalid for Paths

```json
// WRONG - will fail validation
{
  "agents": ["./agents/"]
}

// CORRECT - string path
{
  "agents": "./agents/"
}
```

### Skills Location

Skills must be in subdirectories under `skills/`:

```
my-plugin/
└── skills/
    └── my-skill/
        └── SKILL.md
```

### Auto-Discovery Preferred

If your structure is standard, **omit component paths entirely**:

```json
{
  "name": "my-plugin",
  "description": "What it does. Use when: specific trigger.",
  "version": "0.1.0"
}
```

---

## Examples

### Minimal (Required Only)

```json
{
  "name": "my-plugin"
}
```

### Recommended

```json
{
  "name": "my-plugin",
  "description": "Brief description. Use when: trigger conditions.",
  "version": "0.1.0"
}
```

### Full

```json
{
  "name": "my-plugin",
  "description": "Full description. Use when: building X, debugging Y.",
  "version": "0.1.0",
  "author": {
    "name": "yourname",
    "email": "you@example.com",
    "url": "https://github.com/yourname"
  },
  "homepage": "https://docs.example.com",
  "repository": "https://github.com/yourname/my-plugin",
  "license": "MIT",
  "keywords": ["category", "feature"]
}
```

---

## Testing

### During Development

```bash
claude --plugin-dir ./my-plugin
```

### Verify Components Load

- Commands: Check `/help` or run `/my-plugin:command-name`
- Agents: Check `/agents`
- Skills: Trigger with matching prompt
- Hooks: Run relevant tool/event

---

## File Locations Reference

| Component | Location | Format |
|-----------|----------|--------|
| Manifest | `.claude-plugin/plugin.json` | JSON |
| Commands | `commands/*.md` | Markdown with frontmatter |
| Agents | `agents/*.md` | Markdown with frontmatter |
| Skills | `skills/<name>/SKILL.md` | Markdown with frontmatter |
| Hooks | `hooks/hooks.json` | JSON |
| MCP | `.mcp.json` | JSON |
| LSP | `.lsp.json` | JSON |

---

## Sources

- [Claude Code - Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)
- [Claude Code - Create Plugins](https://code.claude.com/docs/en/plugins.md)
