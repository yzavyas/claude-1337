# Content Triage

Filter research content into skills. Apply to every piece of content.

## The Filter

```
1. Does Claude know this from training?
   ├── YES → Is there an elite twist?
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

| Section | Lines |
|---------|-------|
| Philosophy | 15-25 |
| Decision framework | 15-30 |
| Gotchas catalog | 40-60 |
| Pattern with code | 15-30 |
| Anti-patterns | 15-25 |
| Domain routing | 15-25 |
| **SKILL.md total** | **100-350** |
| Reference file | 100-200 |
