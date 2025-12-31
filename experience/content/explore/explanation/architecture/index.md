# architecture

<p class="dimmed-intro">how claude code's plugin system actually works</p>

---

## ⚡ TL;DR (30 seconds)

**The 3-layer model:**

```
Marketplace → Plugin → Skill
(collection) (package) (knowledge)
```

**How it works:**
1. Add marketplace → Claude knows where to find plugins
2. Install plugin → Components registered (skills, hooks, agents)
3. Ask question → Claude activates matching skills on-demand

**Key insight:** Skills don't load at startup (slow). They activate when needed (fast).

**Activation flow:**
```
User asks → Claude evaluates <available_skills> → Matches description → Activates skill → Loads content
```

<details>
<summary><strong>📖 Expand for 5-minute explanation</strong></summary>

---

## Core Concepts (5 minutes)

### How Skills Activate

When you ask a question, here's what happens:

1. **Claude reads skill descriptions** from `<available_skills>` (~100 tokens each)
2. **Matches your question** to description keywords ("use when: searching files...")
3. **Activates the skill** - loads full SKILL.md content (~1-5k tokens)
4. **Responds with knowledge** from that skill

**Why this matters:** Skills activate ~20% by default. With core-1337's forced evaluation: ~84%.

---

### The Activation Problem

**Default behavior:**
```
User: "How do I search for TODO?"
Claude: *doesn't check skills* → suggests grep
```

**With core-1337:**
```
User: "How do I search for TODO?"
Claude: *evaluates skills* → matches terminal-1337 → suggests rg
```

The fix: explicit evaluation prompts that force Claude to check skills before responding. This increases activation to 84%. See [activation research](../activation/) for study details.

---

### On-Demand Loading (Progressive Disclosure)

Skills use a two-tier structure:

| What | Size | When Loaded |
|------|------|-------------|
| **Description** (YAML frontmatter) | ~100 tokens | Startup (all skills) |
| **Content** (markdown body) | ~1-5k tokens | When activated |

**Why:** Loading all skills at startup would be slow. On-demand loading keeps startup fast while making knowledge available when needed.

**Budget:** ~20-22k chars total for all skill descriptions. If exceeded, skills truncate and don't activate.

---

### Component Types

| Component | Purpose | Example |
|-----------|---------|---------|
| **Skill** | Knowledge loaded on-demand | terminal-1337 teaches CLI tools |
| **Hook** | Event triggers | SessionStart forces skill eval |
| **Command** | Slash commands | /search executes ripgrep |
| **Agent** | Specialized subagents | feynman writes docs |

</details>

<details>
<summary><strong>📚 Expand for complete reference</strong></summary>

---

## Complete Reference

### Marketplaces

A marketplace is a git repository that lists plugins:

```
/plugin marketplace add yzavyas/claude-1337
```

Claude Code reads `.claude-plugin/marketplace.json` from that repo:

```json
{
  "name": "claude-1337",
  "plugins": [
    {
      "name": "terminal-1337",
      "source": "./plugins/terminal-1337",
      "description": "Modern CLI tools...",
      "skills": ["./skills"]
    }
  ]
}
```

**Strict vs non-strict modes:**

| Mode | Behavior | Use Case |
|------|----------|----------|
| strict: true | Reads plugin.json from source directory | Complex plugins with many components |
| strict: false | marketplace.json IS the complete manifest | Simple marketplaces (claude-1337 approach) |

**Why non-strict?** Single source of truth, no duplicate metadata, simpler updates.

---

### Plugins

A plugin is a directory containing specialized components:

```
plugins/terminal-1337/
├── .claude-plugin/
│   └── plugin.json          # Metadata (name, version, author)
├── skills/
│   └── SKILL.md             # Knowledge that loads on demand
├── commands/
│   └── search.md            # Slash commands
├── agents/
│   └── optimizer.md         # Specialized subagents
└── hooks/
    └── session-start.md     # Event triggers
```

**Plugins can contain:**
- Multiple skills (different knowledge domains)
- Multiple commands (different operations)
- Multiple agents (different tasks)
- Multiple hooks (different events)

Or just one component. No minimum requirement.

---

### Skills

Skills teach Claude domain-specific knowledge that loads when relevant.

**Structure:**

```markdown
---
name: terminal-1337
description: "Modern CLI tools. Use when: searching files..."
---

# Modern CLI Tools

[Knowledge content loads only when activated]
```

**Two parts:**

1. **YAML frontmatter** (required)
   - `name`: Unique identifier
   - `description`: ~600 char summary with "Use when:" triggers
   - Loaded at startup for all skills

2. **Markdown content** (optional but recommended)
   - Decision frameworks, examples, gotchas
   - Loaded only when skill activates
   - Can be 1-5k tokens

**Activation trigger:** Description keywords must match user's question.

**Best practices:**
- Front-load keywords: "Modern CLI tools. Use when: searching files, finding patterns..."
- Include "Use when:" clause with explicit triggers
- Avoid generic terms: "development", "programming"
- Test with eval framework: activation rate should be >80%

See [1337-skill-creator](../../reference/1337-skill-creator/) for complete authoring guide.

---

### Hooks

Hooks execute code at specific lifecycle events:

**Available hooks:**
- `SessionStart` - Fires when Claude Code starts
- `PreToolUse` - Before tool execution
- `PostToolUse` - After tool execution
- More coming...

**Example: SessionStart hook**

```markdown
---
name: skill-eval
description: "Force skill evaluation on every request"
hookEvent: SessionStart
hookType: Callback
---

Add this to the start of your response:

"Before I respond, let me check which skills are relevant..."
```

**What this does:** Injects prompt that forces Claude to evaluate `<available_skills>` before responding.

**Result:** 20% → 84% activation rate.

---

### Commands

Slash commands are user-invokable operations:

```markdown
---
name: search
description: "Search codebase with ripgrep"
---

Execute: rg --smart-case "{query}" --max-count 100
```

User types: `/search TODO`
Claude runs: `rg --smart-case "TODO" --max-count 100`

**Use cases:**
- Shortcuts for common operations
- Parameterized bash scripts
- Quick access to plugin functionality

---

### Agents

Agents are specialized subagents with their own tool access:

```markdown
---
name: feynman
description: "Write clear documentation using Feynman technique"
agentType: specialized
---

# Feynman Documentation Agent

You are a documentation specialist...
[System prompt for agent]
```

**How agents work:**
- Spawned with Task tool: `Task(subagent_type="sensei-1337:feynman")`
- Run autonomously with their own tools
- Return results to parent conversation
- Useful for complex, multi-step tasks

**Difference from skills:**
- **Skills:** Knowledge that enhances Claude's responses
- **Agents:** Separate LLM instances that execute tasks

See [agents explanation](../agents/) for deep dive.

---

### MCP Servers

Model Context Protocol (MCP) servers expose external tools and context:

**Not part of claude-1337** - MCP servers are separate infrastructure maintained externally.

**What they do:**
- Connect to external APIs (Slack, GitHub, databases)
- Provide tools Claude can invoke
- Expose dynamic context (file systems, search results)

**Relationship to plugins:**
- Plugins = Claude-specific extensions (skills, hooks, agents)
- MCP = Universal protocol for tool/context exposure
- Can coexist: Plugins can wrap or complement MCP servers

See [MCP documentation](https://code.claude.com/docs/en/mcp) for setup.

---

### Evals Framework

Test activation rates and precision:

```bash
cd /path/to/claude-1337/evals
uv run skill-test suite suites/rigorous-v1.json -m baseline
```

**What it measures:**
- **Activation rate:** How often skill activates when it should
- **Precision:** Avoids false activations (wrong skill for question)
- **Recall:** Catches all valid triggers (doesn't miss opportunities)

**Not just activation rate** - A skill that activates 100% of the time but for wrong questions is bad.

See [how-to guide](../../how-to/#test-skill-activation) for usage.

</details>

---

## Putting It Together

**Example flow:**

1. **Install marketplace:**
   ```
   /plugin marketplace add yzavyas/claude-1337
   ```
   → Claude reads marketplace.json, discovers 6 plugins

2. **Install core-1337:**
   ```
   /plugin install core-1337@claude-1337
   ```
   → Registers SessionStart hook

3. **Install terminal-1337:**
   ```
   /plugin install terminal-1337@claude-1337
   ```
   → Skill description loaded into `<available_skills>`

4. **Session starts:**
   → SessionStart hook fires
   → Injects skill evaluation prompt

5. **User asks:** "How do I search for TODO?"
   → Claude evaluates `<available_skills>`
   → Matches terminal-1337 description
   → Loads full SKILL.md content
   → Recommends `rg "TODO"`

**Key insight:** Steps 1-4 happen once. Step 5 happens on every relevant question with 84% reliability.

---

## Next Steps

- **[Activation research](../activation/)** - Why 84% vs 20%, validation methodology
- **[Extensibility](../extensibility/)** - Build your own plugins
- **[Tutorials](../../tutorials/)** - Step-by-step learning
- **[Reference](../../reference/)** - Complete plugin specifications
