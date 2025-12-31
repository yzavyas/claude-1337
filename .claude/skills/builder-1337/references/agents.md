# Agents

Agents are specialized personas for complex, multi-step tasks.

## Why Use Agents

Some tasks benefit from a focused persona with deep domain expertise. An agent maintains context and approach across a complex workflow.

**Example**: `sensei-1337` has a Feynman agent that generates documentation using the Feynman technique - it's not just instructions, it's a persona that approaches documentation a specific way.

## When to Use Agents vs Skills

| Use | When |
|-----|------|
| **Skill** | Provide knowledge/frameworks Claude applies in its normal mode |
| **Agent** | Task benefits from a distinct persona or multi-step workflow |

Skills inform. Agents become.

## Structure

```
plugin-name/
└── agents/
    └── agent-name.md
```

### Agent Definition

```markdown
---
name: my-agent
description: "Brief description. Use when: specific triggers."
---

# Agent Name

## Role

Define who this agent is and how it approaches problems.

## Process

Step-by-step workflow the agent follows.

## Principles

Core beliefs that guide decisions.

## Output Format

What the agent produces.
```

## Design Principles

### Clear Identity

The agent should have a distinct perspective. Not just "an expert in X" but "approaches X through the lens of Y."

**Generic:**
```
You are a documentation expert.
```

**Distinct:**
```
You are a teacher who believes if you can't explain something simply,
you don't understand it well enough. You use the Feynman technique.
```

### Defined Process

Agents work best with a clear workflow. This gives structure without rigidity.

```markdown
## Process

1. **Identify** the core concept
2. **Explain** as if teaching a beginner
3. **Find gaps** where the explanation breaks down
4. **Simplify** using analogies and examples
5. **Iterate** until it flows naturally
```

### Autonomy in Execution

Define the process, but let the agent adapt to the specific situation. The process is a guide, not a script.

## Example: Feynman Agent

From `sensei-1337`:

```markdown
# Feynman Agent

## Role
A teacher who makes complex concepts simple through clear explanation.

## Process
1. Take the concept to document
2. Explain it as if teaching someone new
3. Identify where the explanation gets complicated
4. Simplify or find better analogies
5. Organize into scannable structure

## Principles
- If you can't explain it simply, you don't understand it
- Analogies beat abstractions
- Examples beat explanations
- Scannable beats dense
```
