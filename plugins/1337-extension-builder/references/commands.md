# Commands

Slash commands for user-invoked workflows. Location: `commands/name.md`

---

## Template

```markdown
---
description: "Short description for /slash menu"
allowed-tools: Bash(git *:*), Read(*), Edit(*)
---

## Context

- Current status: !`git status`
- Current branch: !`git branch --show-current`

## Your task

Based on the above context:

1. Do step one
2. Do step two
3. Complete the task
```

---

## Frontmatter Fields

| field | required | description |
|-------|----------|-------------|
| `description` | yes | Shows in /slash menu |
| `allowed-tools` | no | Restrict which tools command can use |
| `context` | no | `fork` to run in sub-agent |
| `agent` | no | Model: `haiku`, `sonnet`, `opus` |

### allowed-tools Patterns

```yaml
# Specific command
allowed-tools: Bash(git commit:*)

# Multiple commands
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)

# Wildcards
allowed-tools: Bash(git *:*), Read(*), Edit(*)

# All tools (default if omitted)
# allowed-tools: *
```

---

## Dynamic Context: !`backticks`

Commands can inject live data using `!`backticks``:

```markdown
## Context

- Git status: !`git status`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`
- Package version: !`jq -r .version package.json`
```

**How it works:**
- Bash command runs when command is invoked
- Output is injected into the prompt
- Claude sees the result, not the command

**Not available in skills** - only commands support this.

---

## Complete Examples

### Simple: /commit

```markdown
---
description: Create a git commit
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---

## Context

- Current git status: !`git status`
- Current git diff: !`git diff HEAD`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.
Stage files and commit in a single message.
```

### Complex: /commit-push-pr

```markdown
---
description: Commit, push, and open a PR
allowed-tools: Bash(git checkout --branch:*), Bash(git add:*), Bash(git status:*), Bash(git push:*), Bash(git commit:*), Bash(gh pr create:*)
---

## Context

- Current git status: !`git status`
- Current git diff: !`git diff HEAD`
- Current branch: !`git branch --show-current`

## Your task

Based on the above changes:

1. Create a new branch if on main
2. Create a single commit with an appropriate message
3. Push the branch to origin
4. Create a pull request using `gh pr create`

Do all steps in a single message.
```

### With Arguments: /review-pr

```markdown
---
description: Review a pull request
allowed-tools: Bash(gh pr *:*), Read(*), Grep(*)
---

## Context

- PR details: !`gh pr view $1 --json title,body,files`
- PR diff: !`gh pr diff $1`

## Your task

Review PR #$1:

1. Summarize the changes
2. Check for issues
3. Provide feedback
```

Arguments: `$1`, `$2`, etc. from user input after command name.

---

## Skills vs Commands

| Aspect | Skill | Command |
|--------|-------|---------|
| **Location** | `skills/name/SKILL.md` or `SKILL.md` | `commands/name.md` |
| **Trigger** | Auto by context matching | User via `/name` |
| **Dynamic context** | No | Yes (`!`backticks``) |
| **Arguments** | No | Yes (`$1`, `$2`) |
| **Use case** | Knowledge, patterns, guidance | Workflows, automation |

**Since v2.1.3**: Skills in `skills/` are also visible in slash menu by default.
Opt-out with `user-invocable: false` in skill frontmatter.

---

## Best Practices

| practice | why |
|----------|-----|
| Minimal allowed-tools | Principle of least privilege |
| Dynamic context | Fresh data each invocation |
| Single responsibility | One command, one workflow |
| Clear task instructions | Predictable behavior |
| Chain with `&&` mindset | Steps depend on previous |

### Dos and Don'ts

```markdown
# DO: Be specific about the task
## Your task
Create a commit with a conventional commit message.
Stage only modified files, not untracked.

# DON'T: Be vague
## Your task
Make a commit.
```

---

## Forked Context

Run command in isolated sub-agent:

```yaml
---
description: Long-running analysis
context: fork
agent: haiku
---
```

- `context: fork` - Runs in background, doesn't pollute main context
- `agent: haiku` - Use faster/cheaper model for simple tasks

---

## Quality Checklist

- [ ] Description is concise (<60 chars)
- [ ] allowed-tools is minimal
- [ ] Dynamic context uses !`backticks`
- [ ] Task instructions are specific
- [ ] Works when run multiple times (idempotent)
- [ ] Handles edge cases (no changes, errors)
