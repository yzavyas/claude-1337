# plugin catalog

all plugins in the claude-1337 marketplace. filter by component type (skills, hooks, agents) or search by keywords.

## install core-1337 first

```
/plugin marketplace add yzavyas/claude-1337
/plugin install core-1337@claude-1337
```

## plugins by component

### skills

skills inject domain knowledge into claude's context.

| plugin | description |
|--------|-------------|
| **terminal-1337** | modern cli tools (rg, fd, bat, eza, xh, jq, atuin, fzf) |
| **rust-1337** | production rust patterns, decision frameworks, 12 domain references |
| **1337-skill-creator** | skill authoring methodology, content triage |
| **sensei-1337** | feynman technique, diataxis framework, anti-patterns |
| **diagrams-1337** | diagram type selection, mermaid vs d2, platform gotchas |

### hooks

hooks modify claude's behavior at lifecycle points.

| plugin | hook | description |
|--------|------|-------------|
| **core-1337** | SessionStart | forced skill evaluation pattern (20% → 84%) |
| **terminal-1337** | SessionStart | skill activation fix |
| **sensei-1337** | SessionStart | skill activation fix |

### agents

agents execute tasks autonomously.

| plugin | agent | description |
|--------|-------|-------------|
| **sensei-1337** | feynman | autonomous documentation workflow (understand → simplify → teach → refine) |
| **diagrams-1337** | davinci | deep architecture diagramming (context, container, sequence, state, data) |

## installation

install individual plugins:

```
/plugin install terminal-1337@claude-1337
/plugin install rust-1337@claude-1337
```

list installed plugins:

```
/plugin list
```

## component types explained

| type | what it does | example |
|------|-------------|---------|
| **skill** | injects knowledge | rust patterns, cli tools |
| **hook** | modifies behavior | force skill evaluation |
| **agent** | autonomous execution | documentation workflow |
| **command** | slash commands | /deploy, /test |
| **mcp** | external integrations | databases, APIs |

see [concepts](../../tutorials/concepts/) for full architecture explanation.
