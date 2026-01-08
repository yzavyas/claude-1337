# Marketplace Schema

Valid schema for `marketplace.json` in Claude Code plugins.

## Root Object

| field | type | required | description |
|-------|------|----------|-------------|
| `name` | string | yes | Marketplace identifier (kebab-case) |
| `owner` | object | yes | Maintainer info |
| `plugins` | array | yes | List of plugins |
| `metadata` | object | no | Description, version |

### Owner Object

| field | type | required |
|-------|------|----------|
| `name` | string | yes |
| `email` | string | no |

### Metadata Object

| field | type | description |
|-------|------|-------------|
| `description` | string | Brief marketplace description |
| `version` | string | Marketplace version |
| `pluginRoot` | string | Base directory for relative source paths |

## Plugin Entry Object

### Required Fields

| field | type | description |
|-------|------|-------------|
| `name` | string | Plugin identifier (kebab-case) |
| `source` | string/object | Where to fetch plugin |

### Optional Metadata

| field | type | description |
|-------|------|-------------|
| `description` | string | What plugin does |
| `version` | string | Plugin version |
| `author` | object | `{ name, email }` |
| `homepage` | string | URL |
| `repository` | string | URL |
| `license` | string | SPDX identifier |
| `keywords` | array | Search terms |
| `category` | string | Plugin category |
| `tags` | array | Additional tags |
| `strict` | boolean | Requires own `plugin.json` |

### Component Configuration

Explicit fields for each component type:

| field | type | description |
|-------|------|-------------|
| `commands` | string/array | Path(s) to commands |
| `agents` | string/array | Path(s) to agents |
| `hooks` | string/object | Path to hooks.json or inline |
| `mcpServers` | string/object | MCP server config |
| `lspServers` | string/object | LSP server config |

## Gotcha: No Generic "components" Field

Claude Code does NOT accept:

```json
{
  "components": ["skills", "agents"]  // INVALID - rejected
}
```

Use explicit fields instead:

```json
{
  "agents": "./agents"  // VALID
}
```

## Minimal Example

```json
{
  "name": "my-marketplace",
  "owner": { "name": "you" },
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./plugins/my-plugin",
      "description": "What it does. Use when: specific trigger.",
      "agents": "./agents",
      "hooks": "./hooks.json"
    }
  ]
}
```

## Full Example

```json
{
  "name": "claude-1337",
  "owner": {
    "name": "yzavyas",
    "email": "yza.vyas@gmail.com"
  },
  "metadata": {
    "description": "Curated cognitive extensions",
    "version": "0.1.0"
  },
  "plugins": [
    {
      "name": "sensei-1337",
      "source": "./plugins/sensei-1337",
      "description": "Documentation methodology. Use when: writing docs.",
      "version": "0.1.0",
      "author": { "name": "yzavyas" },
      "license": "MIT",
      "keywords": ["documentation", "teaching"],
      "category": "development",
      "agents": "./agents"
    }
  ]
}
```

## Source

Claude Code docs: https://code.claude.com/docs/en/plugin-marketplaces.md#marketplace-schema
