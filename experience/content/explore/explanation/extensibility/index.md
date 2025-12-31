[&larr; explanation](../)

# extensibility

<p class="dimmed-intro">understanding how to extend claude code with custom functionality</p>

## what does extensible mean?

extensibility means you can add new capabilities to claude code without modifying its core. think of it like a smartphone:

- **base phone** - claude code CLI (camera, phone, messaging)
- **app store** - plugin marketplaces (install new apps)
- **custom apps** - your own plugins (build what you need)

claude code provides extension points where you can plug in custom behavior.

## extension mechanisms

| mechanism | what it extends | when to use |
|-----------|----------------|-------------|
| **skills** | claude's knowledge | teach claude domain expertise (rust patterns, cli tools) |
| **hooks** | claude's behavior | modify how claude responds (forced eval, output formatting) |
| **agents** | autonomous capabilities | specialized task execution (code review, research) |
| **commands** | CLI workflows | custom slash commands (/deploy, /test) |
| **MCP servers** | external integrations | connect to APIs, databases, services |

## how plugins work

a plugin is a package that bundles multiple extensions:

```
my-plugin/
├── skills/           # knowledge to inject
│   └── SKILL.md
├── hooks/            # behavior modifiers
│   └── SessionStart.js
├── agents/           # autonomous workers
│   └── my-agent/
├── commands/         # slash commands
│   └── deploy.md
└── mcp/              # external integrations
    └── server.js
```

when you install a plugin, claude code registers all these extensions and makes them available.

## extending with skills

skills inject domain knowledge. you write SKILL.md files containing:

- **description** - when claude should use this (critical for activation)
- **knowledge** - decision frameworks, patterns, tools
- **references** - additional docs (loaded on-demand)

example: terminal-1337 teaches claude about modern CLI tools (rg, fd, bat). when you ask "how do i search files", claude loads that skill and recommends ripgrep.

### skill activation pattern

```
User asks question
  ↓
Claude evaluates <available_skills>
  ↓
Matches skill description → activates and loads SKILL.md
  ↓
Uses knowledge to respond
```

see [activation research](../activation/) on skill activation rates and how to optimize descriptions.

## extending with hooks

hooks modify claude's behavior at specific lifecycle points:

| hook | when it runs | what it can do |
|------|-------------|----------------|
| SessionStart | when claude starts up | inject instructions, set mode, configure behavior |
| UserPromptSubmit | before claude sees your message | modify prompt, add context, enforce patterns |
| AssistantResponse | after claude responds | post-process output, log, format |

example: core-1337's SessionStart hook injects the forced evaluation pattern that increases skill activation from 20% to 84%.

## extending with custom agents

agents are autonomous workers built with the claude agent sdk. they:

- receive a goal (task description)
- have access to specific tools
- execute without asking for confirmation
- return structured results

example: sensei-1337's feynman agent explains concepts using the feynman technique autonomously.

### agent anatomy

```javascript
// agent definition
{
  name: "code-reviewer",
  description: "reviews code for issues",
  tools: [Read, Grep, Bash],
  systemPrompt: `
    you are a code reviewer.
    check for: security, performance, style.
    output: markdown report.
  `
}
```

when invoked via Task tool, the agent spawns, does its work, and returns findings.

## extending with commands

commands are custom slash commands that expand to prompts:

```markdown
// .claude/commands/deploy.md
---
name: deploy
description: deploy to production
---
run the deployment script, then verify health checks.
if anything fails, rollback.
```

when you type `/deploy`, claude sees the expanded prompt and executes it.

## extending with MCP servers

MCP (model context protocol) servers connect claude to external systems:

- **databases** - query postgres, mongodb, redis
- **APIs** - call rest endpoints, graphql, grpc
- **services** - interact with github, slack, jira
- **filesystems** - access remote files, s3 buckets

MCP servers expose tools that claude can call. example:

```javascript
// github MCP server provides:
- create_issue(title, body)
- list_prs(repo)
- merge_pr(pr_number)
```

claude can then "create a github issue" by calling the tool provided by the MCP server.

## combining extensions

powerful plugins combine multiple extension types:

```
terminal-1337:
├── skill: teaches modern CLI tools
├── hook: warns about deprecated commands
└── (future) agent: auto-optimizes shell scripts

core-1337:
└── hook: forces skill evaluation before responding

sensei-1337:
├── skill: teaches feynman + diataxis
└── agent: explains concepts using feynman
```

## extension discovery

claude code discovers extensions through:

1. **plugin.json** - declares what extensions the plugin contains
2. **marketplace.json** - lists available plugins
3. **.claude/** - user's local custom extensions

when you install a plugin, its extensions are registered and become available to claude.

## building your own extensions

### quick start

- **skill** - create SKILL.md with skill description (YAML frontmatter) + knowledge. see [1337-skill-creator](../../reference/1337-skill-creator/)
- **hook** - create javascript file exporting handler function
- **agent** - use claude agent sdk to define agent + tools
- **command** - create markdown file in .claude/commands/
- **MCP server** - implement MCP protocol to expose tools

### testing extensions

local development workflow:

```
1. create extension in .claude/
2. restart claude code (or reload)
3. test activation/behavior
4. iterate until working
5. package as plugin
6. publish to marketplace
```

## extension best practices

- **single responsibility** - one plugin, one purpose
- **clear descriptions** - skills must have good "use when:" clauses with explicit activation triggers
- **fail gracefully** - hooks shouldn't break claude if they error
- **minimal dependencies** - keep plugins lightweight
- **test activation** - use the eval framework to validate skills activate reliably

## limitations and constraints

what you can't extend (currently):

- **core tool implementations** - can't modify Read, Edit, Bash tools
- **model selection** - can't force claude to use specific models globally
- **token limits** - can't increase context window
- **skill budget** - can't exceed ~20-22k char in available_skills

these are platform constraints, not extensibility limitations.

## next steps

to build extensions:

1. read [architecture](../architecture/) to understand the system
2. study [1337-skill-creator](../../reference/1337-skill-creator/) for skill authoring
3. browse [plugin catalog](../../reference/catalog/) for examples
4. use the [eval framework](../activation/) to validate activation rates
