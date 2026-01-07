# ethos

What we're building toward.

---

## the goal

Extensions that make the collaboration **more capable**.

After using a tool, nothing changes. After using a cognitive extension, both parties understand something they didn't before.

---

## the divergence

Small design choices multiply their effects over time. Same technology, different trajectories.

```mermaid
stateDiagram-v2
    direction LR
    [*] --> extension: use

    extension --> complementary: transparency + control
    extension --> substitutive: consumption only

    complementary --> accumulates: engage, learn
    substitutive --> atrophies: offload, depend

    accumulates --> [*]: better with and without
    atrophies --> [*]: can't function alone
```

The evidence:
- r = -0.75 correlation between AI use and critical thinking ([Gerlich 2025](/explore/reference/bibliography/#gerlich-2025))
- 20% skill degradation in 3 months ([Lancet 2025](/explore/reference/bibliography/#lancet-2025))
- 39-point perception gap — developers thought they were 20% faster, were 19% slower ([METR 2025](/explore/reference/bibliography/#metr-2025))

These aren't one-time drops that level out — they indicate ongoing decline.

---

## what determines outcome

Blaurock et al. (2024) tested five design features:

**Strong effect**: transparency, process control, outcome control, reciprocity.

**No effect**: engagement prompts (asking questions, prompting reflection).

Show reasoning and provide control. Don't ask.

---

## three types

**Complementary** — human learns through collaboration. Better with and without.

**Constitutive** — enables what was impossible. New capability emerges.

**Substitutive** — human consumes output. Capability atrophies.

The same extension can be any of these, depending on design.

---

## principles

**Collaborative agency** — both parties retain judgment.

**Bidirectional learning** — both parties develop.

**Transparent abstractions** — readable, forkable, verifiable.

**Composable architecture** — extensions build on each other.

---

## for builders

- Show reasoning woven in, not separable
- Provide frameworks, not decisions
- Cite sources
- Make it readable

After using your extension, the collaboration should be more capable.

---

## deeper

- [extended mind thesis](../collaborative-intelligence/extended-mind/)
- [research](/explore/reference/research/)
- [bibliography](/explore/reference/bibliography/)
- [principles](../principles/)
