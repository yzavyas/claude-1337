# Skill Creation Process

**Use [research-workflow.md](research-workflow.md) for executable prompts.**

This file documents the overall process. For copy-paste prompts, see the research workflow.

## Quick Reference

| Phase | What | Where |
|-------|------|-------|
| 1. Gap | Test Claude, find wrong/missing knowledge | [research-workflow.md#step-1](research-workflow.md#step-1-define-the-gap) |
| 2. Research | 3 production codebases | [research-workflow.md#step-2](research-workflow.md#step-2-research-production-codebases) |
| 3. Verify | Maintainer quotes, stats | [research-workflow.md#step-3](research-workflow.md#step-3-verify-with-maintainers) |
| 4. Gotchas | Production issues, postmortems | [research-workflow.md#step-4](research-workflow.md#step-4-identify-production-gotchas) |
| 5. Draft | Fill SKILL.md template | [research-workflow.md#step-5](research-workflow.md#step-5-draft-the-skill) |
| 6. Validate | Run checklist | [research-workflow.md#step-6](research-workflow.md#step-6-validate) |

## Structure

**Goal**: Organize for progressive disclosure.

### SKILL.md Core (~100-200 lines)

```markdown
---
name: domain-1337
description: "What + Use when: triggers"
---

# Title

One sentence purpose.

## Decision Framework
[Tables for common choices]

## Production Gotchas
[Non-obvious traps]

## Domain Routing
[Link to references/]
```

### Reference Files (~100-150 lines each)

| File Type | Contains |
|-----------|----------|
| Subdomain | Deep patterns for specific use case |
| Ecosystem | Crate/tool comparisons with evidence |
| Recipes | Multi-step patterns, config snippets |

### File Naming

```
skill-name/
├── SKILL.md              # Always loaded when triggered
└── references/
    ├── subdomain-a.md    # Loaded on: "X detection"
    ├── subdomain-b.md    # Loaded on: "Y detection"
    └── ecosystem.md      # Loaded on: "crate/tool questions"
```

## Writing Rules

**Goal**: Apply content triage to every line.

See [content-triage.md](content-triage.md) for the full filter.

### Writing Rules

1. **Tables over prose** - Scannable decisions
2. **Code shows, prose tells** - Minimal explanation
3. **Bold the winner** - Clear recommendations
4. **Cite evidence** - Production usage > stars
5. **Version things** - What might change

### Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| "There are many options..." | Pick THE answer |
| "You could use X or Y" | "Use X. Y is deprecated." |
| Teaching basics | Assume Claude knows syntax |
| Complete tutorials | Decision points only |
| Marketing language | Evidence-based claims |

## Validation

**Goal**: Ensure skill triggers and loads correctly.

### Pre-Commit Checklist

```
[ ] Description < 600 chars, has "Use when:" triggers
[ ] No YAML multiline (>-, |) - use quoted strings
[ ] SKILL.md < 500 lines (target 100-200)
[ ] References < 250 lines each (target 100-150)
[ ] All linked files exist
[ ] Evidence cited for recommendations
[ ] No catalogs - winners picked
```

### Trigger Testing

1. Start fresh Claude session
2. Ask related question (don't mention skill name)
3. Check: Does skill appear in response?
4. Check: Is full content loading, or truncated?

### Size Verification

```bash
# Check line counts
wc -l SKILL.md references/*.md

# Check char count for description
grep "description:" SKILL.md | wc -c
```

## Maintenance

**Goal**: Keep skill current.

### Update Triggers

| Signal | Action |
|--------|--------|
| Major version release | Review breaking changes |
| Deprecation notice | Find replacement |
| New crate gains traction | Validate production use, consider |
| Bug reports on advice | Fix with evidence |

### Update Process

1. Research the change
2. Verify evidence (production > hype)
3. Update affected files only
4. Test trigger still works
5. Commit with evidence in message
