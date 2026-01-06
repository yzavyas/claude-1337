# Commands

Commands are slash-invoked actions for explicit user workflows.

## Why Use Commands

Commands give users explicit control. Unlike skills (auto-activated) or hooks (event-driven), commands are intentionally invoked.

**Example**: `/skill-check` explicitly runs validation. The user wants this action now.

## When to Use Commands

| Use | When |
|-----|------|
| **Skill** | Knowledge should be available implicitly when relevant |
| **Hook** | Action should happen automatically at an event |
| **Command** | User should explicitly choose to run this |

Commands are for workflows users want to trigger deliberately.

## Structure

```
plugin-name/
└── commands/
    └── command-name.md
```

Or project-local:

```
.claude/
└── commands/
    └── command-name.md
```

### Command Definition

```markdown
---
name: my-command
description: "What this command does"
---

# Command Name

[Instructions for what Claude should do when this command is invoked]

## Arguments

If the command accepts arguments, document them:
- `$1` - First argument description
- `$2` - Second argument description

## Process

Step-by-step what happens when invoked.
```

## Design Principles

### Clear Purpose

Each command should do one thing well. If a command has many modes, consider splitting it.

**Too broad:**
```
/skill - create, update, check, or delete skills
```

**Focused:**
```
/skill-check - validate skill structure and triggers
/skill-update - refresh skill content
```

### Useful Defaults

Commands should work without arguments when possible. Arguments refine, not enable.

```
/skill-check              # Check all skills
/skill-check rust-1337    # Check specific skill
```

### Feedback

Commands should confirm what they did. Users invoked explicitly - they want to know it worked.

```markdown
## Output

After running, provide:
- What was checked/done
- Any issues found
- Suggested next steps if applicable
```

## Example: skill-check

```markdown
---
name: skill-check
description: "Validate skill structure, triggers, and tokenomics"
---

# Skill Check

Validate skills against the maintainer-1337 checklist.

## Process

1. Load maintainer-1337 for the review checklist
2. For each skill (or specified skill):
   - Check frontmatter format
   - Verify description length and triggers
   - Confirm referenced files exist
   - Estimate token impact
3. Report findings

## Arguments

- `$1` (optional) - Specific skill to check. Default: all skills.

## Output

Summary table of checks passed/failed per skill.
```

## Project Commands

This project has commands in `.claude/commands/`:

| Command | Purpose |
|---------|---------|
| `/skill-check` | Validate skill structure |
| `/skill-update` | Refresh skill content |
