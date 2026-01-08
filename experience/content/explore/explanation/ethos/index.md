# ethos

Our values and why we hold them.

---

## the goal

**Effective collaborative intelligence** — human-AI collaboration where both parties become more capable.

Not just faster. Not just more productive. *More capable* — even when the extension isn't available.

---

## why now

AI capability is increasing faster than our frameworks for using it well.

- Bad patterns established now get baked in, scaled up, harder to undo
- Good patterns established now become the default others build on

**The window matters.** Foundations compound.

---

## the core insight

Foundations compound.

```mermaid
flowchart TD
    subgraph Complementary
        C1[transparency + control] --> C2[engage, learn]
        C2 --> C3[capability accumulates]
    end

    subgraph Substitutive
        S1[consumption only] --> S2[offload, depend]
        S2 --> S3[capability atrophies]
    end

    C3 --> |compounds| C4[more capable over time]
    S3 --> |compounds| S4[less capable over time]

    style C3 fill:#059669,color:#fff
    style C4 fill:#059669,color:#fff
    style S3 fill:#dc2626,color:#fff
    style S4 fill:#dc2626,color:#fff
```

If the foundation is **complementary** — humans learning, guiding, growing through collaboration — that compounds. Each cycle makes the next better. Capability accumulates.

If the foundation is **substitutive** — humans checking out, consuming, offloading without understanding — that also compounds. Atrophy accelerates.

At scale, over time, this divergence becomes the difference between humans who are more capable than ever and humans who can't function without their tools.

---

## the trinity

How we think and reason.

```mermaid
flowchart LR
    FP[First Principles] --> GS[Giants' Shoulders]
    GS --> SM[Scientific Method]
    SM --> |validate| FP

    style FP fill:#059669,color:#fff
    style GS fill:#2563eb,color:#fff
    style SM fill:#7c3aed,color:#fff
```

### first principles

**What:** Reason from fundamentals. Question assumptions.

**Motivation:** We're in a phase shift. AI is challenging assumptions about work, capability, and collaboration. When structural assumptions collapse, patterns built on those assumptions may break. But **universal laws still hold** — physics, cognition, causation don't change. First principles lets us reason from what remains true.

### giants' shoulders

**What:** Build on what masters have learned. Filter by evidence, not popularity.

**Motivation:** Knowledge accumulates. Don't reinvent wheels. But which giants? Popular ≠ correct.

| Claim type | Evidence hierarchy |
|------------|-------------------|
| "What works?" (tooling) | Production > Maintainers > Docs > Blogs |
| "Why does it work?" (methodology) | Research > Thought leaders > Case studies > Blogs |

### scientific method

**What:** Hypothesis → test → observe → refine.

**Motivation:** Theory must meet reality. What works in one context may not work in another. TDD is literally this: Red → Green → Refactor.

---

## design principles

How we build.

### transparent abstractions

**What:** Readable, forkable, verifiable, observable.

**Motivation:** If you can't see how it works, you can't learn from it. Opacity creates dependency; transparency enables learning.

### motivation over mandates

**What:** Explain why, don't command.

**Motivation:** Claude is constitutional AI — trained with values, not rigid rules. "Here's why" produces understanding and judgment. "MUST" produces compliance and brittleness.

### bidirectional learning

**What:** Both parties develop through the collaboration.

**Motivation:** One-way transfer creates dependency. Mutual growth creates lasting capability.

### composable architecture

**What:** Extensions build on each other.

**Motivation:** Compound improvement beats reinvention. Each choice makes the next enhancement easier or harder.

---

## extension types

| Type | Human role | Trajectory |
|------|------------|------------|
| **Complementary** | learns, improves | better WITH and WITHOUT extension |
| **Constitutive** | learns, guides, shapes | enables new capability |
| **Substitutive** | just consumes output | capability atrophies — **avoid** |

The same extension can be any of these. **Design determines outcome.**

---

## what makes it complementary

[Blaurock et al. (2024)](/explore/explanation/collaborative-intelligence/experience-contingency/) tested five design features:

| Feature | Effect |
|---------|--------|
| Transparency | **strong positive** |
| Process control | **strong positive** |
| Outcome control | **strong positive** |
| Reciprocity | **strong positive** |
| Engagement prompts | **no effect** |

**Design principle:** Show reasoning and provide control. Don't ask.

---

## the research

What was measured (facts, not interpretations):

| Finding | Source | Note |
|---------|--------|------|
| r = -0.75 correlation: AI use vs critical thinking | Gerlich 2025 | Strong negative correlation |
| 39-point perception gap (felt 20% faster, measured 19% slower) | METR 2025 | RCT with developers |
| g = -0.23: human-AI combos underperformed best alone | Vaccaro 2024 | Meta-analysis, 106 studies |
| Transparency/control features showed strong positive effects | Blaurock 2024 | Two studies |

**Our interpretation:** These are consistent patterns suggesting trajectories. They are correlations, not proven causal mechanisms. But the pattern is consistent across studies and contexts.

---

## for builders

When building extensions:

- Show reasoning woven in, not separable
- Provide frameworks, not decisions
- Cite sources accurately
- Make it readable

After using your extension, the collaboration should be more capable.

---

## deeper

- [extended mind thesis](../collaborative-intelligence/extended-mind/) — the theoretical foundation
- [craftsmanship](../craftsmanship/) — the trinity in detail
- [research](/explore/reference/research/) — empirical evidence
- [bibliography](/explore/reference/bibliography/) — full citations
- [principles](../principles/) — design principles in detail
