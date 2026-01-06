---
name: builder-1337
description: "Build in the claude-1337 project. Use when: creating plugins, updating docs, building experiences. Composes with marketplace plugins or reads from plugins/ directory."
---

# claude-1337 Builder

Build and extend the claude-1337 marketplace.

## Composition

When building, compose with the relevant skill:

| Building... | Compose with | Fallback (if not installed) |
|-------------|--------------|------------------------------|
| Skills | `1337-extension-builder` | Read `plugins/1337-extension-builder/SKILL.md` |
| Documentation | `sensei-1337` | Read `plugins/sensei-1337/SKILL.md` |
| Diagrams | `diagrams-1337` | Read `plugins/diagrams-1337/SKILL.md` |

If the plugin is installed, use `Skill(name)` to activate it. If not, read the SKILL.md directly from this repo.

## Repository Structure

```
claude-1337/
├── .claude-plugin/
│   └── marketplace.json      # Plugin registry
├── .claude/skills/           # Project-local skills
│   ├── builder-1337/         # This skill
│   └── maintainer-1337/      # Evaluation/stewardship
├── plugins/                  # THE MARKETPLACE
│   └── [plugin-name]/
│       ├── .claude-plugin/plugin.json
│       ├── SKILL.md
│       ├── skills/
│       ├── hooks/
│       ├── agents/
│       └── commands/
├── experience/               # HUMAN-FACING LAYER
│   ├── content/              # Markdown source (Diataxis structure)
│   ├── app/                  # SvelteKit app that renders content
│   └── lab/                  # Experiments (gitignored)
└── evals/                    # Skill activation testing
```

## Plugin Types

### Skills
Knowledge and decision frameworks activated by description matching.
→ Compose with `1337-extension-builder` for methodology

### Hooks
Respond to Claude Code events. Structure:
```
hooks/
├── hooks.json
└── hook-script.sh
```
See [references/hooks.md](references/hooks.md)

### Agents
Specialized personas for complex tasks. Structure:
```
agents/
└── agent-name.md
```
See [references/agents.md](references/agents.md)

### Commands
Slash-invoked actions. Structure:
```
commands/
└── command-name.md
```
See [references/commands.md](references/commands.md)

## Workflows

### Creating a Plugin
1. Create `plugins/[name]/`
2. Add `.claude-plugin/plugin.json`
3. Add components (skills/, hooks/, agents/, commands/)
4. Update `marketplace.json`
5. Run maintainer-1337 review

### Updating explore/ (Documentation)
1. Compose with `sensei-1337`
2. Edit in `experience/content/explore/`
3. Build/preview in `experience/app/`

### Building ethos/ (Experience)
1. Develop in `experience/content/ethos/`
2. Experiment in `experience/lab/` (gitignored)
3. Graduate to `experience/app/`

## Experience Layer

The human-facing documentation layer. Markdown content rendered by SvelteKit.

### Structure

```
experience/
├── content/                  # Markdown source files
│   ├── start/               # Getting started
│   ├── ethos/               # Project motivation/philosophy
│   └── explore/             # Main docs (Diataxis)
│       ├── tutorials/       # Learning-oriented
│       ├── how-to/          # Task-oriented
│       ├── explanation/     # Understanding-oriented
│       │   ├── collaborative-intelligence/
│       │   │   └── extended-mind/
│       │   ├── ecosystem/
│       │   ├── craftsmanship/
│       │   └── ethos/
│       └── reference/       # Information-oriented
│           ├── research/    # Empirical foundations
│           └── bibliography/# Canonical citations
├── app/                     # SvelteKit app
│   ├── src/routes/          # File-based routing
│   └── build/               # Static output
└── lab/                     # Experiments (gitignored)
```

### Content → Routes Mapping

Most content paths map directly to URL routes:
- `content/ethos/index.md` → `/ethos/`
- `content/explore/reference/research/index.md` → `/explore/reference/research/`

### Dynamic Routes

Some routes are dynamically generated in the app, not from markdown:

| Route | Source | Why |
|-------|--------|-----|
| `/explore/reference/catalog/` | `marketplace.json` | Plugins self-describe; single source of truth |

The catalog reads from `.claude-plugin/marketplace.json` and renders a searchable, filterable plugin list. No static markdown - adding a plugin to the marketplace automatically adds it to the catalog.

### Diataxis Framework

| Type | Purpose | Example |
|------|---------|---------|
| **tutorials** | Learning by doing | first-skill, custom-plugin |
| **how-to** | Accomplish specific goals | (planned) |
| **explanation** | Understanding concepts | collaborative-intelligence, extended-mind |
| **reference** | Technical information | research, bibliography, catalog (dynamic) |

### Development

```bash
cd experience/app
bun install
bun run dev      # localhost:5173
bun run build    # static output to build/
```

## Tooling

Use `bun` not `npm`:
```bash
bun install
bun run dev
bun run build
```

## Contributor Setup

```bash
/plugin marketplace add ./
/plugin install core-1337@claude-1337
# Install others as needed
```
