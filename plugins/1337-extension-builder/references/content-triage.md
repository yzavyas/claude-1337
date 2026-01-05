# Content Triage

Filter research content into skills. Apply to every piece of content.

## Pre-Filter: Evidence Quality

Before triaging content, verify research quality:

| gate | principle |
|------|-----------|
| sources | Multiple independent sources — if limited, acknowledge explicitly |
| evidence | Use highest quality available — production > maintainer > blog |
| claims | Each claim traceable to source (author, year, context) |

**If research lacks quality → STOP.** Return to [research-workflow.md](research-workflow.md) Step 2.

Triaging bad research just produces well-organized bad content.

## The Filter

```
1. Does Claude know this from training?
   ├── YES → Is there a non-obvious insight?
   │         ├── YES → Include twist only
   │         └── NO  → CUT
   └── NO  → Continue

2. Is this a decision or fact?
   ├── DECISION → Format as table/tree
   └── FACT → Is it time-sensitive?
             ├── YES → Note version, consider reference
             └── NO  → Include if passed step 1

3. Is this >20 lines of code?
   ├── YES → Script or reference file
   └── NO  → Include inline

4. Is this domain-specific?
   ├── YES → Route to reference file
   └── NO  → Include in SKILL.md core
```

## Quick Categorization

### Cut (Red Flags)

| Signal | Example |
|--------|---------|
| Basic syntax | `for x in items { }` |
| Textbook examples | `fn longest<'a>(...)` |
| Standard structure | `src/main.rs` |
| Official docs | How to use `Result<T,E>` |
| Generic explanations | "Rust uses ownership..." |

### Include (Green Flags)

| Signal | Example |
|--------|---------|
| Corrects assumptions | "async-std is deprecated" |
| Production gotcha | Mutex across await |
| Decision framework | String ownership 95% rule |
| Evidence-based | ripgrep uses lexopt not clap |
| Non-obvious footgun | CString lifetime trap |
| Quantified | "10-100μs between await points" |

## Content Routing
//TODO: Scripts? Command references, etc. ? This needs review. 
| Type | Destination |
|------|-------------|
| Decision frameworks | SKILL.md |
| Production gotchas | SKILL.md |
| Deprecation tables | SKILL.md |
| Anti-patterns | SKILL.md |
| Domain-specific | references/ |
| Deep examples | references/ |
| Config files | references/ or scripts/ |

## Format Selection

| Content | Format |
|---------|--------|
| X vs Y decision | Table |
| Multiple conditions | Decision tree |
| Quick lookup | Table |
| Pattern + anti-pattern | Side-by-side code |
| Procedure | Numbered steps |

## Line Budgets

| Section | Lines | Rationale |
|---------|-------|-----------|
| Philosophy | 15-25 | context-setting only |
| Decision framework | 15-30 | scannable tables |
| Gotchas catalog | 40-60 | the core value |
| Pattern with code | 15-30 | code is dense |
| Anti-patterns | 15-25 | quick reference |
| Domain routing | 15-25 | links to references |
| **SKILL.md total** | **< 500** | loads on activation |
| Reference file | no hard limit | loads on-demand |
