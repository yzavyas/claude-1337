# Research Workflow

Executable prompts for building elite skills. Copy-paste these, don't interpret them.

## Step 1: Define the Gap

**Run this prompt to start:**

```
I want to build a skill for [DOMAIN].

First, test what I already know. Ask me these questions and I'll answer based on my training:
1. What's the best tool/crate/approach for [COMMON USE CASE]?
2. What gotchas exist when doing [TYPICAL OPERATION]?
3. Is [POPULAR OPTION] still the recommended choice?

Then identify: where did I give generic advice? Where am I outdated? Where did I lack evidence?

These gaps become the skill's content.
```

**Expected output:**
- 3-5 specific gaps (wrong defaults, missing gotchas, no decision framework)
- Clear scope for the skill

## Step 2: Research Production Codebases

**Run these searches in order:**

```
Search for [3 production codebases] in [DOMAIN] to see what they actually use.

Targets (pick 3):
- Most-starred project in the ecosystem
- Tool written by domain experts (e.g., ripgrep for Rust CLI)
- Company production codebase (e.g., Cloudflare, Discord, 1Password)

For each, find:
- What [LIBRARIES/TOOLS] do they use?
- What patterns appear repeatedly?
- What did they avoid that's popular?
```

**Evidence template:**
```markdown
## [Codebase Name]

**URL**: [GitHub link]
**What they use**: [specific tool/crate]
**Evidence**: [file path or quote]
**Notable absence**: [popular thing they don't use]
```

## Step 3: Verify with Maintainers

**Run this search:**

```
Find what the core maintainer(s) of [TOOL/CRATE] recommend:
- Conference talks or blog posts
- GitHub issues where they explain design decisions
- Quotes about best practices

Also check:
- Downloads/usage stats (crates.io, npm, etc.)
- Recent activity (last commit, last release)
- Known deprecations or migrations
```

**Evidence template:**
```markdown
## [Tool/Crate] Maintainer Position

**Maintainer**: [name]
**Source**: [URL]
**Quote**: "[exact quote]"
**Downloads**: [X/week]
**Last release**: [date]
```

## Step 4: Identify Production Gotchas

**Run this prompt:**

```
Search for production issues, postmortems, and "lessons learned" for [DOMAIN]:

Keywords to search:
- "[tool] production issue"
- "[tool] postmortem"
- "[tool] lessons learned"
- "[tool] we replaced"
- "[tool] doesn't scale"
- "[tool] gotcha"

Look for:
- Things that work in dev but fail in prod
- Performance cliffs
- Migration regrets
- What looked good but wasn't
```

**Evidence template:**
```markdown
## [Gotcha Title]

**Source**: [URL]
**The trap**: [what seemed fine]
**The failure**: [what went wrong]
**The fix**: [what to do instead]
```

## Step 5: Draft the Skill

**Fill in this template:**

```markdown
---
name: [domain]-1337
description: "[What it does]. Use when: [trigger 1], [trigger 2]. Covers: [keyword1], [keyword2]."
---

# [Domain] Elite Patterns

[One sentence: what problem this solves]

## Decision Framework

| Situation | Choice | Why |
|-----------|--------|-----|
| [Use case 1] | **[winner]** | Evidence: [source] |
| [Use case 2] | **[winner]** | Evidence: [source] |

## Production Gotchas

| Trap | Fix |
|------|-----|
| [Gotcha 1] | [Solution] |
| [Gotcha 2] | [Solution] |

## Domain Routing

| Detected | Load |
|----------|------|
| [keyword] | [reference.md](references/reference.md) |
```

## Step 6: Validate

**Run these checks:**

```
Review the skill I just drafted:

1. Description check:
   - Is it < 600 characters?
   - Does it have "Use when:" triggers?
   - Are keywords front-loaded?

2. Content check:
   - Every recommendation has evidence?
   - No catalogs ("options include A, B, C")?
   - Tables over prose?
   - Would an expert push back?

3. Size check:
   - SKILL.md < 200 lines (hard max: 500)?
   - References < 150 lines each?

4. Trigger test:
   - What question would activate this skill?
   - Does the description match that question?
```

## Evidence Tracker Template

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
