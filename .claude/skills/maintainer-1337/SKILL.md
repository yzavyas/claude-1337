---
name: maintainer-1337
description: "Maintain the claude-1337 marketplace. Use when: committing, creating PRs, reviewing skills, verifying triggers, checking tokenomics, validating SKILL.md, adding plugins. Covers conventional commits, squash/rebase, skill review checklist, size limits."
---

# claude-1337 Maintainer

Maintain and update the claude-1337 marketplace.

**Composes with**:
- `example-skills:skill-creator` - skill fundamentals, anatomy, packaging
- `1337-skill-creator` - opinionated content layer (picks winners, evidence-based)

## Repository Structure

```
claude-1337/
├── .claude-plugin/
│   └── marketplace.json     # Plugin registry
├── .claude/
│   ├── commands/            # Repo-local commands
│   │   ├── skill-check.md
│   │   └── skill-update.md
│   └── skills/              # Repo-local skills
│       └── maintainer-1337/ # This skill
├── plugins/                 # Public plugins
│   ├── terminal-1337/
│   ├── rust-1337/
│   └── 1337-skill-creator/
└── .github/workflows/
    └── update-skills.yml    # Weekly auto-update
```

## Skill Review Checklist

Before merging any skill changes:

### Frontmatter (Critical)

| Check | Why |
|-------|-----|
| `name` < 50 chars | Hard limit |
| `description` < 600 chars | Truncated otherwise |
| Quoted strings only | `>-`, `\|` parse as literal ">-" |
| "Use when:" in description | Explicit triggers help matching |

### Trigger Quality

- **Front-load keywords** Claude matches against
- **Be specific**: "axum, tonic, sqlx" not just "backend"
- **Include verbs**: "building", "debugging", "configuring"
- Test: Ask related question without naming skill - does it trigger?

### Size Limits

| File | Target | Max |
|------|--------|-----|
| SKILL.md | 100-200 lines | 500 |
| references/*.md | 100-150 lines | No hard limit |
| Description | ~400 chars | 600 |

### Tokenomics Check

- `<available_skills>` budget: ~20-22k chars total
- ~34-36 skills fit before truncation
- **Truncated skills don't trigger** - Claude can't see them
- Test: "How many skills in your `<available_skills>` block?"

### Content Quality (1337 Standards)

- [ ] Picks winners, not catalogs
- [ ] Evidence cited (production > stars)
- [ ] Decision frameworks, not tutorials
- [ ] No "you could use X or Y" - pick one
- [ ] Gotchas are non-obvious (Claude doesn't know)

### File Integrity

- [ ] All linked references exist
- [ ] No broken internal links
- [ ] Scripts executable (`chmod +x`)

## Git Workflow

### Conventional Commits

```
type(scope): description

feat:     New feature
fix:      Bug fix
docs:     Documentation only
refactor: No behavior change
chore:    Build, deps, config
```

Examples:
- `feat(rust-1337): add data-plane reference`
- `fix: correct install command in README`
- `refactor: restructure docs for maintainability`

### PR Process

```
1. Branch from main
   git checkout -b feat/my-feature

2. Commit with conventional format
   git commit -m "feat(skill): add X"

3. Before PR: squash related commits
   git rebase -i origin/main

4. Force push after rebase
   git push --force-with-lease

5. PR → Squash and merge
```

### Squash Strategy

| Commits | Strategy |
|---------|----------|
| WIP commits | Squash into logical units |
| Fixup commits | Squash into original |
| Unrelated changes | Split into separate PRs |

Rule: **One PR = one logical change = one squashed commit on main.**

## Skill Update Workflow

Run `/skill-update` or manually:

1. **Research**: Web search for deprecations, new releases, production usage
2. **Validate**: Is "best-in-class" still best? Any new contenders?
3. **Update**: Only with evidence (production usage > GitHub stars)
4. **Commit**: Use conventional format
   ```
   fix(rust-1337): update deprecated crate recommendation

   thiserror 2.0 released with breaking changes.
   Source: https://github.com/dtolnay/thiserror/releases

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

## Adding a New Plugin

1. **Load skills**: `example-skills:skill-creator` then `1337-skill-creator`
2. Create `plugins/new-plugin/SKILL.md` following skill-creator guidelines
3. Add to `marketplace.json`:
   ```json
   {
     "name": "new-plugin",
     "source": "./plugins/new-plugin",
     "description": "Brief description with triggers",
     "version": "0.1.0",
     "skills": ["./"]
   }
   ```
4. Run `/skill-check` to validate

## Skill Activation Research

**Problem**: Skills only activate ~20% of the time by default. Claude often ignores them and "wings it."

### How Triggering Actually Works

From [Lee Han Chung's deep dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/):
- **No algorithmic routing** - no regex, no embeddings, no classifiers
- **Pure LLM reasoning** - Claude reads skill descriptions and decides
- **Description is everything** - it's the only signal for matching

### What Makes Skills Activate

From [Scott Spence's 200+ test study](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably):

| Approach | Success Rate |
|----------|--------------|
| No intervention (baseline) | ~20% |
| Simple instruction | ~20% |
| LLM eval hook | 80% |
| Forced eval hook | **84%** |

**Key insight**: Forcing Claude to explicitly evaluate each skill before proceeding dramatically improves activation.

### Effective Description Patterns

| Pattern | Example |
|---------|---------|
| Action verbs | "building", "debugging", "configuring" |
| Specific tools | "axum, tonic, sqlx" not "backend" |
| "Use when:" clause | Explicit trigger conditions |
| Domain keywords | Terms Claude will match against |

### Testing Skills

1. **Trigger test**: Fresh session, ask related question (don't name skill) - does it activate?
2. **Content test**: Compare output with/without skill - is there a difference?
3. **Tokenomics test**: "How many skills in your `<available_skills>` block?"

### Sources

- [Anthropic: Equipping agents with skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) - eval-driven development
- [Scott Spence: Skills activation](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably) - 200+ test study
- [Lee Han Chung: Skills deep dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) - triggering mechanism

## Update Schedule

- **rust-1337**: Check quarterly (Rust moves fast)
- **terminal-1337**: Check semi-annually
- **GitHub Action**: Runs monthly (1st at 2am UTC)
