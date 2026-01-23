# Skills

Reference for building skill extensions. Follows the Agent Skills open standard.

Sources:
- [Claude Code - Skills](https://code.claude.com/docs/en/skills)
- [Claude Code - Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [AgentSkills.io - Open Standard](https://agentskills.io/specification)

---

## Quick Reference

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | No (uses directory name) | Slash command name. Lowercase, hyphens, max 64 chars. |
| `description` | Recommended | When to use. Claude uses this for auto-activation. |
| `disable-model-invocation` | No | Set `true` to prevent Claude from auto-triggering. |
| `user-invocable` | No | Set `false` to hide from `/` menu. |
| `allowed-tools` | No | Tools Claude can use without asking. |
| `context` | No | Set `fork` to run in subagent. |
| `agent` | No | Subagent type when `context: fork`. |

---

## Two Types of Content

### Reference Content

Knowledge Claude applies to current work. Conventions, patterns, style guides.

```yaml
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

Runs inline. Claude uses it alongside conversation context.

### Task Content

Step-by-step instructions for specific actions. Deployments, commits, generation.

```yaml
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

Often invoke-only (`disable-model-invocation: true`).

---

## Invocation Control

| Setting | You invoke | Claude invokes | Use for |
|---------|------------|----------------|---------|
| (default) | Yes | Yes | Most skills |
| `disable-model-invocation: true` | Yes | No | Workflows with side effects (deploy, commit) |
| `user-invocable: false` | No | Yes | Background knowledge (legacy-system-context) |

---

## Frontmatter Reference

```yaml
---
name: my-skill
description: What this skill does and when to use it
argument-hint: [issue-number]
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Grep, Glob
model: sonnet
context: fork
agent: Explore
---
```

| Field | Description |
|-------|-------------|
| `name` | Display name. If omitted, uses directory name. |
| `description` | What and when. Claude uses for auto-activation. |
| `argument-hint` | Shown in autocomplete. Example: `[filename]`. |
| `disable-model-invocation` | Prevent Claude from auto-triggering. |
| `user-invocable` | Hide from `/` menu if `false`. |
| `allowed-tools` | Pre-approved tools list. |
| `model` | Model to use when active. |
| `context` | `fork` runs in isolated subagent. |
| `agent` | Subagent type (`Explore`, `Plan`, `general-purpose`, or custom). |

---

## String Substitutions

| Variable | Replaced with |
|----------|---------------|
| `$ARGUMENTS` | Arguments passed when invoking |
| `${CLAUDE_SESSION_ID}` | Current session ID |

If `$ARGUMENTS` not in content, arguments appended as `ARGUMENTS: <value>`.

---

## Dynamic Context Injection

Shell commands in `` !`command` `` run before content is sent to Claude:

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

Commands execute immediately. Claude sees the output, not the command.

---

## Subagent Execution

`context: fork` runs skill in isolated subagent. Skill content becomes the prompt.

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

**Note:** Only makes sense for skills with explicit instructions. Guidelines without a task return without meaningful output.

---

## Directory Structure

```
skill-name/
├── SKILL.md           # Required - pragmatic, < 500 lines
├── references/        # Detailed docs, load as needed
├── scripts/           # Executable code
└── assets/            # Templates, files used in output
```

---

## What Goes Where

| SKILL.md | references/ |
|----------|-------------|
| High-level workflow | Detailed patterns |
| Decision frameworks | Full examples |
| Practical motivation | Academic citations |
| "Load X when Y" navigation | Deep technical content |
| Gotchas and traps | API documentation |
| < 500 lines | No limit |

**Key insight:** SKILL.md motivates and navigates. References provide depth.

---

## Progressive Disclosure

| Level | Size | When loaded |
|-------|------|-------------|
| Metadata (name + description) | ~100 words | Always — triggers activation |
| SKILL.md body | < 500 lines | When skill activates |
| References | Unlimited | When Claude needs them |

Reference pattern:
```markdown
## References

| need | load |
|------|------|
| Python patterns | [python.md](references/python.md) |
| Error handling | [errors.md](references/errors.md) |
```

---

## Activation

Skills activate through LLM reasoning. **Description is the only signal.**

| Good | Bad |
|------|-----|
| "Use when: debugging TypeScript, need tsconfig help" | "Helps with TypeScript" |
| "Use when: creating diagrams, need Mermaid syntax" | "Diagram skill" |
| Action verbs + specific triggers | Abstract nouns |

Character budget: 15,000 chars for all descriptions combined (~4000 tokens).

---

## Checklist

### Content
- [ ] Fills gaps (what Claude doesn't know)
- [ ] Decisions, not tutorials
- [ ] SKILL.md < 500 lines
- [ ] Practical motivation, not academic

### Activation
- [ ] "Use when:" in description
- [ ] Description < 600 chars
- [ ] Triggers on right prompts
- [ ] Negative test cases (shouldn't trigger on X)

### Structure
- [ ] Skill in `skills/<name>/SKILL.md`
- [ ] References clearly navigated
- [ ] Academic sources in references, not SKILL.md
- [ ] Scripts for deterministic operations
- [ ] Tested in real session

### Invocation
- [ ] `disable-model-invocation: true` if has side effects
- [ ] `user-invocable: false` if background knowledge
- [ ] `context: fork` if needs isolation
- [ ] Correct subagent type if forked

---

## Sources

- [Claude Code - Skills](https://code.claude.com/docs/en/skills)
- [Claude Code - Plugins Reference](https://code.claude.com/docs/en/plugins-reference)
- [AgentSkills.io - Specification](https://agentskills.io/specification)
