---
name: maintainer-1337
description: "Review and maintain the claude-1337 marketplace. Use when: reviewing PRs, validating skills, checking quality gates, stewardship tasks. Evaluation and polish."
---

# claude-1337 Maintainer

Stewardship of the claude-1337 marketplace. Review, validate, polish.

For building, see `builder-1337`. This skill focuses on evaluation.

## Skill Review Checklist

### Frontmatter

| Check | Why |
|-------|-----|
| `name` < 50 chars | Hard limit in Claude Code |
| `description` < 600 chars | Truncated beyond this |
| Quoted strings only | YAML `>-`, `\|` parse incorrectly |
| "Use when:" clause | Explicit triggers improve activation |

### Trigger Quality

Skills activate based on description matching. Test: ask a related question without naming the skill.

| Pattern | Why it helps |
|---------|--------------|
| Front-load keywords | Claude matches against description start |
| Specific terms | "axum, tonic" > "backend" |
| Action verbs | "building", "debugging" signal intent |

### Size Limits

| File | Target | Why |
|------|--------|-----|
| SKILL.md | < 500 lines | Anthropic best practices |
| Description | ~400 chars | Leave room in budget |

### Tokenomics

`<available_skills>` has ~20-22k char budget. ~34-36 skills fit before truncation.

**Truncated skills don't activate.** Test: "How many skills in your `<available_skills>` block?"

### Quality Gates (Primary)

| gate | target | principle |
|------|--------|-----------|
| sources | 3+ codebases | Independent? Limitations noted if <3? |
| evidence | production-tier | Highest quality used? |
| CoVe | 100% claims | Each traceable? |
| activation | F1 ≥0.8, FPR ≤20% | Run `uv run skill-test` |

**Targets are specific. Principles allow judgment.**

### Content Quality (1337 Standards)

| Check | Why |
|-------|-----|
| Battle-tested, best-in-class picks | Stand on giants' shoulders |
| Evidence cited | Production usage > GitHub stars |
| Decision frameworks | Actionable > educational |
| Gotchas are non-obvious | Value-add over common knowledge |

### File Integrity

- [ ] All referenced files exist
- [ ] No broken internal links
- [ ] Scripts executable (`chmod +x`)

## PR Review Process

### Before Approving

1. Run checklist above for any skill changes
2. Verify no TODO/placeholder content
3. Check commit message format
4. Confirm tests pass (if applicable)

### Commit Message Format

```
type(scope): description

feat:     New feature
fix:      Bug fix
docs:     Documentation
refactor: No behavior change
chore:    Build, deps, config
```

Why: Scannable history, potential automated changelogs.

### Merge Strategy

One PR = one logical change = one squashed commit on main.

Why: Clean history, easy reverts, clear blame.

## Plugin Validation

Before a plugin ships:

1. **Structure**: Has required files (plugin.json, SKILL.md if skill)
2. **Triggers**: Description activates on relevant queries
3. **Content**: Follows 1337 standards (battle-tested, best-in-class)
4. **Integration**: Registered in marketplace.json

## Update Checks

For skill updates:

| Signal | Action |
|--------|--------|
| Deprecated tool/crate | Find replacement with evidence |
| New best-in-class option | Validate production status first |
| Major version release | Review for breaking changes |
| Security advisory | Update with mitigation |

## Activation Testing

```bash
cd evals
uv sync
uv run skill-test test "query" -s skill-name -n 3
```

| Result | Meaning |
|--------|---------|
| 80%+ | Description working well |
| 50-79% | Needs improvement |
| <50% | Missing triggers or too vague |
