[&larr; reference](../)

standard skills teach. 1337 skills decide.

## install

```
/plugin install 1337-skill-creator@claude-1337
```

**composes with:** `example-skills:skill-creator` - load that first for skill anatomy, on-demand loading (progressive disclosure), and packaging. this skill adds the "1337 layer": opinionated content.

## the difference

| standard skill | 1337 skill |
|----------------|------------|
| "options include A, B, C" | "use A. B is deprecated, C doesn't scale." |
| explains how things work | decision frameworks for what to pick |
| comprehensive coverage | production gotchas only |
| tutorial-style | tables and trees |

## core principles

1. **best-in-class only** - THE answer, not catalogs
2. **evidence over opinion** - production usage > github stars
3. **concise** - decision frameworks + gotchas, not tutorials
4. **claude is smart** - only add what claude doesn't already know

## content triage

quick test for every piece of content:

```
Does Claude know this? → YES → Is there an elite twist? → NO → CUT
```

### include (green flags)

| signal | example |
|--------|---------|
| corrects assumptions | "async-std is deprecated" |
| production gotcha | mutex across await |
| decision framework | string ownership 95% rule |
| evidence-based | ripgrep uses lexopt not clap |
| non-obvious footgun | CString lifetime trap |

### cut (red flags)

| signal | example |
|--------|---------|
| basic syntax | `for x in items { }` |
| textbook examples | `fn longest<'a>(...)` |
| generic explanations | "rust uses ownership..." |
| complete tutorials | step-by-step guides |

## description is everything

skills activate through pure LLM reasoning - no algorithmic routing. the description is the **only signal** claude uses to decide whether to activate your skill.

### what works (from 200+ test study)

| pattern | why |
|---------|-----|
| "use when:" clause | explicit activation conditions |
| specific tools/terms | "axum, tonic, sqlx" not "backend" |
| action verbs | "building", "debugging", "configuring" |
| domain keywords | front-load what claude matches against |

### what fails

| anti-pattern | problem |
|--------------|---------|
| generic descriptions | claude can't distinguish from others |
| missing activation triggers | no "use when:" means guessing |
| abstract terms | "helps with development" - too vague |

**reality check:** skills only activate ~20% by default. good descriptions are critical.

## skill.md structure

```markdown
---
name: domain-1337
description: "What it does. Use when: activation trigger 1, activation trigger 2. Covers: keyword1, keyword2."
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

## size targets

| component | target | max |
|-----------|--------|-----|
| SKILL.md | 100-200 lines | 500 lines |
| reference file | 100-150 lines | no hard limit |

## executable workflow

**don't read process docs. run prompts.**

| step | do |
|------|-----|
| 1 | test claude's knowledge, find gaps |
| 2 | research 3 production codebases |
| 3 | verify with maintainer quotes |
| 4 | collect production gotchas |
| 5 | fill in SKILL.md template |
| 6 | run validation checks |

see `references/research-workflow.md` for copy-paste prompts for each step.

## validation checklist

after passing `example-skills:skill-creator` validation:

- no catalogs - clear winners picked
- each recommendation has evidence
- content is decisions, not tutorials
- would an expert find this useful? (not just beginners)

## structure

```
plugins/1337-skill-creator/
├── SKILL.md                    # methodology
└── references/
    ├── research-workflow.md    # executable prompts
    ├── content-triage.md       # what to include/cut
    └── skill-process.md        # process overview
```
