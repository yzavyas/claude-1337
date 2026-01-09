# Evidence Templates

Copy-paste prompts for researching extensions. Use these exactly — don't interpret.

## Step 1: Define Gap

```
I want to build a skill for [DOMAIN].

Test what I already know:
1. What's the best tool for [COMMON USE CASE]?
2. What gotchas exist when doing [TYPICAL OPERATION]?
3. Is [POPULAR OPTION] still recommended?

Where did I give generic advice? Where am I outdated?
These gaps become the skill's content.
```

**Expected output**: 3-5 specific gaps (wrong defaults, missing gotchas, no decision framework).

---

## Step 2: Research Production Codebases

```
Find 3 production codebases in [DOMAIN]:
- Most-starred project in ecosystem
- Tool by domain experts (e.g., ripgrep for Rust CLI)
- Company production (Cloudflare, Discord, 1Password)

For each, find:
- What libraries/tools do they use?
- What patterns appear repeatedly?
- What did they avoid that's popular?
```

### Evidence Template

```markdown
## [Codebase Name]

**URL**: [GitHub link]
**What they use**: [specific tool/crate]
**Evidence**: [file path or quote]
**Notable absence**: [popular thing they don't use]
```

---

## Step 3: Verify with Maintainers

```
Find what core maintainers of [TOOL] recommend:
- Conference talks or blog posts
- GitHub issues with design decisions
- Downloads/usage stats (crates.io, npm, etc.)
- Recent activity (last commit, last release)
- Known deprecations or migrations
```

### Evidence Template

```markdown
## [Tool] Maintainer Position

**Maintainer**: [name]
**Source**: [URL]
**Quote**: "[exact quote]"
**Downloads**: [X/week]
**Last release**: [date]
```

---

## Step 4: Identify Production Gotchas

```
Search for production issues, postmortems:
- "[tool] production issue"
- "[tool] postmortem"
- "[tool] we replaced"
- "[tool] gotcha"
- "[tool] doesn't scale"

Look for:
- Things that work in dev but fail in prod
- Performance cliffs
- Migration regrets
```

### Evidence Template

```markdown
## [Gotcha Title]

**Source**: [URL]
**The trap**: [what seemed fine]
**The failure**: [what went wrong]
**The fix**: [what to do instead]
```

---

## Step 5: Draft the Skill

```markdown
---
name: [domain]-1337
description: "[What it does]. Use when: [trigger 1], [trigger 2]."
---

# [Domain] Production Patterns

## Decision Framework

| Situation | Choice | Why |
|-----------|--------|-----|
| [Use case] | **[winner]** | Evidence: [source] |

## Production Gotchas

| Trap | Fix |
|------|-----|
| [Gotcha] | [Solution] |
```

---

## Step 6: Validate (CoVe)

For each claim:

| claim | source | quality | contradictions? | confidence |
|-------|--------|---------|-----------------|------------|
| [claim 1] | | prod/maintainer/blog | | high/medium/low |

### Checklist

- [ ] Description < 600 chars with "Use when:"
- [ ] SKILL.md < 500 lines
- [ ] Decisions, not option lists
- [ ] Tested in real session

---

## Full Evidence Tracker

Use this to collect all evidence before writing:

```markdown
# [Skill Name] Evidence

## Gap Analysis
- Gap 1: [Claude said X, but production uses Y]
- Gap 2: [Claude missed gotcha Z]
- Gap 3: [No decision framework for W]

## Production Codebases

### [Codebase 1]
- URL:
- Uses:
- Evidence:
- Avoids:

### [Codebase 2]
- URL:
- Uses:
- Evidence:
- Avoids:

### [Codebase 3]
- URL:
- Uses:
- Evidence:
- Avoids:

## Maintainer Positions

### [Tool 1]
- Maintainer:
- Source:
- Quote:
- Stats:

## Production Gotchas

### [Gotcha 1]
- Source:
- Trap:
- Failure:
- Fix:

## Decisions Ready to Draft

| Question | Answer | Evidence |
|----------|--------|----------|
| Best X for Y? | | |
| When to use Z? | | |
```
