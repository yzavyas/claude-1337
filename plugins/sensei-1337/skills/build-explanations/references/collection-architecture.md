# Collection Architecture

Principles for organizing multiple documents. Document-level writing is necessary but not sufficient — collections need their own architecture.

## Why This Matters

Sensei principles (cognitive load, Diataxis, Feynman) apply to individual documents. But when each author applies document-level principles independently, collections become redundant and incoherent:

- The same research gets explained fully in every document that references it
- Readers encounter the same information multiple times
- Key findings lose impact through repetition
- No clear path through the material

**The root cause**: Document-scoped thinking applied to collection-scoped problems.

## Single Source of Truth

### The Principle

Each piece of information lives in exactly one place. Everywhere else links to it.

| Instead of | Do this |
|------------|---------|
| Explain research in every doc that needs it | Explain once in reference, link from everywhere |
| Define concept wherever it's used | Define once, link to definition |
| Repeat the same table | Put table in one place, reference it |

### Why It Matters

| Redundancy causes | Single source fixes |
|-------------------|---------------------|
| Cognitive load from repetition | Reader sees info once |
| Inconsistency when one copy updates | One place to update |
| Diluted impact | Key findings hit once, memorably |
| Maintenance burden | Change one place, done |

### Implementation

```
reference/
  └── research/
      └── collaboration.md    ← Full explanation of collaboration research

explanation/
  └── principles.md           ← Links to research, doesn't repeat it
      "Collaboration often underperforms. [See the research →]"
```

## Progressive Disclosure at Architecture Level

Within a document, progressive disclosure means simple first, details later. At the collection level, it means structuring the entire doc set as layers of depth.

### The Layer Model

```
Layer 1: Entry Point (30 seconds)
         ├── The bottom line
         ├── Why it matters
         └── Where to go next
              │
              ▼
Layer 2: Explanation (5 minutes)
         ├── Concepts without deep evidence
         ├── Mental models
         └── Links to evidence
              │
              ▼
Layer 3: Reference (verify)
         ├── Full research details
         ├── Methodology
         └── Links to sources
              │
              ▼
Layer 4: Bibliography (deep dive)
         └── Primary sources
```

### Each Layer Is Complete

A reader who stops at any layer got what they needed. They don't feel they missed something — they just didn't need more depth.

| Reader | Stops at | Gets |
|--------|----------|------|
| Decision-maker | Layer 1 | The number, the risk, the action |
| Practitioner | Layer 2 | The concepts, how to apply |
| Evaluator | Layer 3 | The evidence, methodology |
| Researcher | Layer 4 | Primary sources to verify |

## Linking Patterns

### When to Inline vs. Link

| Situation | Inline | Link |
|-----------|--------|------|
| Core to understanding this doc | ✓ | |
| Supporting evidence | | ✓ |
| Tangential but interesting | | ✓ |
| Reader needs it to continue | ✓ | |
| Reader might want to verify | | ✓ |
| Appears in multiple docs | | ✓ (to single source) |

### Link Phrasing

| Purpose | Pattern |
|---------|---------|
| Dive deeper | "See: [topic] for details" |
| Evidence | "See: [research] for the evidence" |
| Related | "Related: [topic]" |
| Definition | "[term →]" (linked inline) |

### Avoiding Orphan Readers

Every link should help the reader, not strand them:
- Link text should indicate what they'll find
- Don't link mid-thought if it breaks flow
- Consider "back" flow — can they return easily?

## Collection-Level Diataxis

Diataxis maps cleanly to collection structure:

```
start/              ← Entry point (pre-Diataxis: the hook)
  └── index.md

explore/
  ├── tutorials/    ← Learning-oriented (teach me)
  ├── how-to/       ← Task-oriented (help me do)
  ├── explanation/  ← Understanding-oriented (help me understand)
  └── reference/    ← Information-oriented (give me facts)
      └── bibliography/  ← Sources (let me verify)
```

### Where Things Live

| Content type | Lives in | Not in |
|--------------|----------|--------|
| Research findings | reference/research/ | explanation/ (just link) |
| Concepts explained | explanation/ | reference/ (too dry) |
| Step-by-step tasks | how-to/ | explanation/ (wrong mode) |
| Learning journeys | tutorials/ | how-to/ (different need) |
| Citations | bibliography/ | everywhere (single source) |

## The Linking Flow

Information flows downward; links point downward and sideways, rarely upward.

```
start (BLUF)
    │
    ├──→ explanation (concepts)
    │         │
    │         └──→ reference (evidence)
    │                   │
    │                   └──→ bibliography (sources)
    │
    ├──→ tutorials (if learning)
    │
    └──→ how-to (if doing)
```

A reader starts at the top and follows links to the depth they need.

## Diagnosing Collection Problems

### Symptoms of Document-Scoped Thinking

| Symptom | Root cause | Fix |
|---------|------------|-----|
| Same research in multiple docs | Each author included what they needed | Consolidate to reference, link |
| Inconsistent terminology | No shared definitions | Define once, link everywhere |
| Readers say "I read this already" | Redundancy | Single source of truth |
| Hard to find things | Unclear organization | Enforce layer model |
| Updates missed in some places | Multiple copies | Single source |

### The Audit Process

1. **List all claims/citations** across documents
2. **Find duplicates** — same info in multiple places
3. **Designate single source** for each
4. **Replace duplicates with links**
5. **Verify linking flow** — can readers navigate?

## Application Example

**Before** (document-scoped):
- `explanation/principles.md` — explains Blaurock 2024 research in full
- `explanation/ethos.md` — explains Blaurock 2024 research in full
- `reference/research/cognition.md` — explains Blaurock 2024 research in full

**After** (collection-scoped):
- `reference/research/collaboration.md` — full Blaurock 2024 explanation (single source)
- `explanation/principles.md` — "Transparency and control matter more than engagement. [See the research →]"
- `explanation/ethos.md` — "Design choices compound. [Evidence →]"

Same information reaches the reader. No redundancy. Key findings land once, memorably.

## Sources

- Information architecture best practices
- Technical documentation standards (Google, Microsoft, Stripe)
- Content strategy methodology (Halvorson, Kissane)
- Our own experience with document redundancy in claude-1337
