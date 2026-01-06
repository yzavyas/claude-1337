# concepts

understanding how cognitive extensions become part of thinking

*for the theoretical foundations (extended mind thesis, Ba, methodology), see [ethos](ethos/)*

---

## why this architecture?

Extensions need to feel like part of cognition, not tools you pick up. This requires:

- **Low friction** - descriptions load at startup, content loads on-demand
- **Contextual activation** - Claude evaluates relevance, not regex matching
- **Composability** - five modalities that extend different capabilities

The architecture below implements these principles.

---

## marketplace

a marketplace is a git repository that lists plugins. when you run:

```
/plugin marketplace add yzavyas/claude-1337
```

claude code reads `.claude-plugin/marketplace.json` from that repo. this file contains an array of plugins with their locations.

each marketplace entry points to a plugin directory using the `source` field:

```json
{
  "name": "terminal-1337",
  "source": "./plugins/terminal-1337",
  "description": "Modern CLI tools...",
  "skills": ["./skills"]
}
```

the marketplace itself doesn't contain the plugins - it's a pointer. plugins live in subdirectories and can be from any repo.

### strict vs non-strict

two loading modes exist:

| mode | behavior | when to use |
|------|----------|-------------|
| strict: true | reads plugin.json from source directory | complex plugins with many components |
| strict: false | marketplace.json IS the complete manifest | simple marketplaces (our approach) |

## plugins

a plugin is a directory containing specialized components for claude. think of it as a package of **cognitive extensions**.

### the five modalities

plugins and the broader ecosystem support five types of cognitive extension:

| modality | what it extends |
|----------|-----------------|
| **skills** | knowledge — decision frameworks, expertise |
| **commands** | efficiency — workflow shortcuts |
| **agents** | reasoning — specialized problem-solving |
| **hooks** | context — session behavior, environment |
| **mcp** | reach — access to external data, agency on external systems |

together they extend knowledge, efficiency, reasoning, context, and reach.

### structure

```
plugins/terminal-1337/
├── .claude-plugin/
│   └── plugin.json          # metadata (name, version, author)
├── skills/
│   └── SKILL.md             # knowledge that loads on demand
├── commands/
│   └── search.md            # slash commands
├── agents/
│   └── optimizer.md         # specialized subagents
└── hooks/
    └── session-start.md     # event triggers
```

plugins can contain any combination of these. terminal-1337 has skills, rust-1337 has skills, sensei-1337 has skills AND an agent.

### progressive disclosure

claude doesn't load everything at once. here's what loads when:

| stage | what loads | size impact |
|-------|------------|-------------|
| startup | skill descriptions only (~100 tokens each) | 20-22k char budget |
| activation | SKILL.md content | < 500 lines |
| on-demand | references/, scripts/, assets/ | no hard limit |

this means your skill description must trigger activation. if claude doesn't load the skill, the SKILL.md never gets read.

## skills

skills add specialized knowledge to claude. example: you install rust-1337, ask about async rust, and claude loads production patterns from actual codebases.

### how activation works

skills appear in claude's context as an `<available_skills>` block:

```xml
<available_skills>
<skill>
  <name>terminal-1337</name>
  <description>Modern CLI tools. Use when: searching files,
  grepping patterns, viewing code. Covers: rg, fd, bat</description>
</skill>
<skill>
  <name>rust-1337</name>
  <description>Rust production patterns. Use when: building
  async systems, choosing crates, debugging ownership</description>
</skill>
</available_skills>
```

when you ask a question, claude reads these descriptions and decides whether to activate a skill. there's no algorithmic routing - no regex, no embeddings. pure LLM reasoning.

### the activation problem

extensions don't activate reliably by default. you install an extension, ask a relevant question, claude ignores it.

why? claude sees the extensions but doesn't automatically evaluate them against your request. it responds without checking if an extension would help.

the fix: explicit evaluation prompts that force claude to check extensions before responding. see [activation research](./activation/) for the methodology.

### the available_skills budget

the `<available_skills>` block has a ~20-22k character limit. with typical descriptions, that fits 34-36 skills.

what happens at 37 skills? truncation. skills beyond the limit don't appear in the block at all.

truncated skills cannot activate. claude can't see them, so they never trigger.

### what makes descriptions work

from testing 200+ skills, these patterns activate reliably:

| pattern | example | why it works |
|---------|---------|--------------|
| "Use when:" clause | "Use when: building APIs, debugging async" | explicit trigger conditions |
| specific tools/terms | "Covers: tokio, axum, sqlx" | keyword matching |
| action verbs | "building, debugging, configuring" | matches user intent |
| front-loaded keywords | put critical terms early | claude scans top to bottom |

descriptions that say "helps with development" or "useful for coding" activate poorly. too vague.

## hooks

hooks run code when specific events occur. example: show a tip when claude starts, or validate input when a user submits a prompt.

### event types

| event | when it fires | use case |
|-------|---------------|----------|
| SessionStart | claude code session begins | welcome messages, mode setting |
| UserPromptSubmit | user sends a message | input validation, context injection |

### what hooks can do

hooks output text that gets added to the conversation. they CANNOT invoke tools or make API calls.

example SessionStart hook:

```markdown
---
event: SessionStart
---

Teaching mode active. I'll use the Feynman technique:
- Example before theory
- One concept per section
- No unexplained jargon
```

this text appears in the conversation when the session starts, setting context for claude's behavior.

## commands

slash commands are shortcuts that expand to prompts. when you type `/skill-check`, claude sees the contents of `commands/skill-check.md`.

example command file:

```markdown
Diagnose skill health and triggering issues.

## Check Available Skills

1. How many skills are in your <available_skills> block?
2. List each skill's name and first 50 chars of description
3. Are any descriptions truncated?
```

commands are prompts, not scripts. they tell claude what to do, claude executes using its normal tools.

### when to use commands

| use case | example |
|----------|---------|
| repetitive tasks | `/skill-check` to validate all skills |
| complex workflows | `/skill-update` with multi-step process |
| domain shortcuts | `/rg pattern` as ripgrep helper |

## agents

agents are specialized versions of claude with custom system prompts. they run as subagents - separate conversations with focused capabilities.

example: the feynman agent in sensei-1337:

```markdown
---
name: feynman
description: "Documentation agent using Feynman technique"
model: sonnet
---

You are an elite documentation agent.

## Your Workflow

### Phase 1: UNDERSTAND
1. Read the domain
2. Identify the audience
3. List concepts

### Phase 2: TEACH
- Example before theory
- No unexplained jargon
- Max 5 lines per paragraph
```

### agents vs skills

| aspect | skill | agent |
|--------|-------|-------|
| what it is | knowledge that loads into context | separate claude instance with custom prompt |
| when it runs | main conversation, activated on demand | separate thread, invoked explicitly |
| use for | reference data, decision frameworks | specialized workflows, different behavior |

agents are for when you need claude to behave fundamentally differently, not just know different things.

## mcp

Model Context Protocol (MCP) servers provide tools to claude. think of them as plugin backends that expose new capabilities.

example: an MCP server for a database might provide:

- `query_db(sql)` - run SQL queries
- `get_schema()` - fetch table definitions
- `explain_plan(sql)` - analyze query performance

claude sees these as tools it can invoke, similar to its built-in tools like Read or Bash.

### mcp vs skills

| aspect | skill | mcp server |
|--------|-------|------------|
| provides | knowledge, context, patterns | executable tools, APIs, data access |
| runs as | markdown loaded into context | separate process claude calls |
| use for | decisions, references, gotchas | actions, queries, integrations |

skills teach claude what to do. MCP servers give claude new abilities.

note: claude-1337 focuses on skills. MCP servers are separate infrastructure.

## evals

evals (evaluations) test skill quality using **precision** and **recall**, not just activation rate.

### why raw activation rate is meaningless

a skill that activates on every prompt has 100% "activation rate" but is useless. real evaluation requires:

- **precision**: when skill activates, is it actually relevant?
- **recall**: when skill should activate, does it?

### the confusion matrix

```
                    ACTUAL ACTIVATION
                    Yes         No
                +-----------+-----------+
SHOULD    Yes   |    TP     |    FN     |
ACTIVATE        | (correct) | (missed)  |
                +-----------+-----------+
          No    |    FP     |    TN     |
                | (noise)   | (correct) |
                +-----------+-----------+
```

### how testing works

test cases have labeled expectations:

```python
TestCase(prompt="what crate for cli args?", expectation="must_activate")
TestCase(prompt="help me write python", expectation="should_not_activate")
```

this observes actual tool invocation and compares to ground truth. not asking claude's opinion.

### interpreting results

| metric | good | problem |
|--------|------|---------|
| precision | 90%+ (few false activations) | <50% (mostly noise) |
| recall | 80%+ (catches triggers) | <50% (misses too many) |
| F1 | 85%+ (balanced) | <60% (needs work) |

### why evals matter

evals are TDD for agent behavior - the scientific method applied to plugin development. without rigorous testing, you don't know if your skill works.

see `/evals` in the repo and [explanation](../explanation/) for full methodology.

## putting it together

here's how these concepts compose in practice:

1. you add a **marketplace** that lists plugins
2. you install a **plugin** containing skills, commands, agents, hooks
3. plugin **skills** appear in `<available_skills>` with their descriptions
4. when you ask a question, claude reads descriptions and activates relevant skills
5. **hooks** inject context at session start or prompt submit
6. **commands** give you shortcuts for repetitive workflows
7. **agents** run specialized tasks in separate threads
8. **MCP servers** provide tools claude can invoke
9. **evals** measure whether your skills actually activate

the key insight: descriptions are critical. if claude doesn't load your skill, everything inside it is wasted. test activation, optimize descriptions, measure results.

## next steps

- [how-to](../how-to/) - install and use the marketplace
- [explanation](../explanation/) - why skills don't activate and how we fixed it
- [reference](../reference/) - detailed plugin documentation
