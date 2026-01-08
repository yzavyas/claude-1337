# Ethos Reorganization Context

Session: 2026-01-08
Status: First pass complete - ethos page rewritten

---

## What Was Done

Rewrote `experience/content/explore/explanation/ethos/index.md` with:

1. **Clear structure** - Goal → Why Now → Core Insight → Trinity → Design Principles → Extension Types → Research
2. **The Trinity** - First Principles, Giants' Shoulders, Scientific Method (with motivations)
3. **Design Principles** - Transparent abstractions, Motivation over mandates, Bidirectional learning, Composable architecture (with motivations)
4. **Accurate research section** - Facts labeled as facts, interpretation labeled as interpretation
5. **Mermaid diagrams** - Visualizing the compounding trajectories and trinity

---

## The Complete Framework

### Ethos (Values - the "why")

**Goal:** Effective collaborative intelligence — both parties more capable.

**Core Insight:** Foundations compound.
- Complementary → capability accumulates
- Substitutive → capability atrophies

**Why Now:** AI capability increasing faster than our frameworks. Window matters.

### The Trinity (How we think)

| Principle | What | Motivation |
|-----------|------|------------|
| **First Principles** | Reason from fundamentals | In phase shift, assumptions collapse but universal laws hold |
| **Giants' Shoulders** | Build on masters, filtered by evidence | Knowledge accumulates; filter by evidence, not popularity |
| **Scientific Method** | Hypothesis → test → observe → refine | Theory must meet reality |

### Design Principles (How we build)

| Principle | What | Motivation |
|-----------|------|------------|
| **Transparent abstractions** | Readable, forkable, verifiable | Can't learn from what you can't see |
| **Motivation over mandates** | Explain why, don't command | Constitutional AI; "why" produces judgment |
| **Bidirectional learning** | Both parties develop | One-way transfer creates dependency |
| **Composable architecture** | Extensions build on each other | Compound improvement beats reinvention |

### Extension Types

| Type | Human Role | Trajectory |
|------|------------|------------|
| **Complementary** | learns, improves | better WITH and WITHOUT |
| **Constitutive** | learns, guides, shapes | enables new capability |
| **Substitutive** | just consumes | atrophies — AVOID |

### What Makes It Complementary (Blaurock 2024)

**Strong effects:** Transparency, Process control, Outcome control, Reciprocity

**NO effect:** Engagement prompts

**Design principle:** Show reasoning and provide control. Don't ask.

---

## Research (Facts Only)

| Finding | Source | Note |
|---------|--------|------|
| r = -0.75 correlation: AI use vs critical thinking | Gerlich 2025 | Correlation |
| 39-point perception gap | METR 2025 | RCT |
| g = -0.23 underperformance | Vaccaro 2024 | Meta-analysis |
| Transparency/control strong effects | Blaurock 2024 | Two studies |

**Interpretation:** Consistent patterns suggesting trajectories, not proven causation.

---

## Files Changed This Session

- `experience/content/explore/explanation/ethos/index.md` - **REWRITTEN** with full framework
- `experience/content/start/index.md` - Fixed inaccurate claims
- `plugins/sensei-1337/SKILL.md` - Added accuracy section
- `plugins/sensei-1337/references/accuracy-integrity.md` - New reference
- `experience/app/src/lib/components/CodeBlock.svelte` - Svelte 4 compat fix

---

## Key Quote

> "Precision isn't pedantry. It's the difference between a foundation that compounds toward enhancement vs one that compounds toward dependency."

---

## For Next Session

- Review ethos page for further refinement
- Ensure principles page aligns with ethos
- Check for remaining redundancies
- Consider creating PR
