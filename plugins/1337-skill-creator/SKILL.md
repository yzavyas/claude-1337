---
name: 1337-skill-creator
description: "Create elite Claude skills with opinionated, best-in-class content. Use when: building skills that pick winners not catalogs, need evidence-based recommendations, or want decision frameworks over tutorials. Composes with example-skills:skill-creator."
---

# 1337 Skill Creator

**Composes with**: `example-skills:skill-creator` - load that first for skill anatomy, progressive disclosure, and packaging. This skill adds the "1337 layer": opinionated content that picks winners.

## The 1337 Difference

Standard skills teach. 1337 skills decide.

| Standard Skill | 1337 Skill |
|----------------|------------|
| "Options include A, B, C" | "Use A. B is deprecated, C doesn't scale." |
| Explains how things work | Decision frameworks for what to pick |
| Comprehensive coverage | Production gotchas only |
| Tutorial-style | Tables and trees |

## Core Principles

1. **Best-in-class only** - THE answer, not catalogs
2. **Evidence over opinion** - Production usage > GitHub stars
3. **Concise** - Decision frameworks + gotchas, not tutorials
4. **Claude is smart** - Only add what Claude doesn't already know

## Content Triage

See [content-triage.md](references/content-triage.md) for the full filter.

**Quick test for every piece of content:**

```
Does Claude know this? → YES → Is there an elite twist? → NO → CUT
```

### Include (Green Flags)

| Signal | Example |
|--------|---------|
| Corrects assumptions | "async-std is deprecated" |
| Production gotcha | Mutex across await |
| Decision framework | String ownership 95% rule |
| Evidence-based | ripgrep uses lexopt not clap |
| Non-obvious footgun | CString lifetime trap |

### Cut (Red Flags)

| Signal | Example |
|--------|---------|
| Basic syntax | `for x in items { }` |
| Textbook examples | `fn longest<'a>(...)` |
| Generic explanations | "Rust uses ownership..." |
| Complete tutorials | Step-by-step guides |

## Description is Everything

Skills activate through pure LLM reasoning - no algorithmic routing. The description is the **only signal** Claude uses to decide whether to load your skill.

### What Works (from 200+ test study)

| Pattern | Why |
|---------|-----|
| "Use when:" clause | Explicit trigger conditions |
| Specific tools/terms | "axum, tonic, sqlx" not "backend" |
| Action verbs | "building", "debugging", "configuring" |
| Domain keywords | Front-load what Claude matches against |

### What Fails

| Anti-pattern | Problem |
|--------------|---------|
| Generic descriptions | Claude can't distinguish from others |
| Missing triggers | No "Use when:" means guessing |
| Abstract terms | "helps with development" - too vague |

**Reality check**: Skills only activate ~20% by default. Good descriptions are critical.

## 1337 SKILL.md Structure

```markdown
---
name: domain-1337
description: "What it does. Use when: specific trigger 1, trigger 2. Covers: keyword1, keyword2."
---

# Title

One sentence purpose.

## Decision Framework

| Situation | Choice | Why |
|-----------|--------|-----|
| Building X | **winner** | Evidence: used by Y |

## Production Gotchas

| Trap | Fix |
|------|-----|
| Non-obvious issue | Solution |

## Domain Routing

| Detected | Load |
|----------|------|
| keyword | [ref.md](references/ref.md) |
```

## Size Targets

| Component | Target | Max |
|-----------|--------|-----|
| SKILL.md | 100-200 lines | 500 lines |
| Reference | 100-150 lines | No hard limit |

## 1337 Validation

After passing `example-skills:skill-creator` validation, also check:

- [ ] No catalogs - clear winners picked
- [ ] Each recommendation has evidence
- [ ] Content is decisions, not tutorials
- [ ] Would an expert find this useful? (not just beginners)

## Creation Process

See [skill-process.md](references/skill-process.md) for the full workflow.

1. Load `example-skills:skill-creator` for fundamentals
2. Identify gap - what does Claude get wrong or give generic advice on?
3. Research - find evidence (production codebases > blog posts)
4. Triage - apply content filter ruthlessly
5. Structure - decisions in SKILL.md, deep dives in references/
6. Validate - both standard and 1337 checklists
