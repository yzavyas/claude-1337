# The Anti-Hollowing Framework

Why transparency and control protect capability, and how to design for it.

---

## The Hollowing Risk

Convergent research shows a consistent pattern: passive AI use correlates with capability decline.

| Study | Finding | Effect | Timeframe |
|-------|---------|--------|-----------|
| Gerlich 2025 | AI use vs critical thinking | r = -0.75 | Cross-sectional |
| Lee CHI 2025 | AI confidence vs critical thinking | β = -0.69 | Cross-sectional |
| Budzyń Lancet 2025 | Skill degradation after AI removal | 20% decline | 3 months |
| Kosmyna MIT 2025 | Recall of AI-assisted content | 83% failure | Immediate |

**Key insight**: This isn't a one-time effect. It's a trajectory. Atrophy compounds.

If the foundation is substitutive — humans checking out, consuming, offloading without understanding — that compounds. The hollowing research (r = -0.75) isn't a plateau; it's a slope.

---

## What Determines Outcomes

Blaurock et al. (2024) meta-analyzed 106 studies on human-AI collaboration to find what determines whether AI augments or replaces human capability.

| Feature | Effect | Interpretation |
|---------|--------|----------------|
| **Transparency** | β = 0.415 (strong) | User sees reasoning, can learn |
| **Process Control** | β = 0.507 (strong) | User shapes how work is done |
| **Outcome Control** | Significant positive | User shapes what is produced |
| **Reciprocity** | Strong positive | User grows through collaboration |
| **Engagement features** | b = -0.555 (negative!) | Asking questions doesn't help |

The surprise: engagement features (system asks questions) are *negative*. Conversation doesn't equal cognitive engagement. What matters is whether the human can *see* and *shape* what's happening.

---

## Three Extension Types

| Type | Human Role | Outcome |
|------|------------|---------|
| **Complementary** | Learns, improves | Better with AND without AI |
| **Constitutive** | Guides, shapes | Enables new capability |
| **Substitutive** | Consumes output | Atrophies — avoid |

### Complementary

The human could do the task but uses AI to do it better. The key: they learn patterns, verify reasoning, build judgment. They become more capable over time.

### Constitutive

The task would be impossible without AI (generating 1000 code variations, searching millions of documents). Fine IF transparency and control are maintained. The human guides and shapes, understanding what's happening.

### Substitutive

The human could do the task but checks out. They consume output without understanding. This is what causes hollowing.

**What makes something substitutive**: passive consumption without transparency or control.

---

## What Protects

### Mastery Orientation

ACU Research Bank (2025) found that *how* users approach AI determines outcomes:

| Finding | Effect |
|---------|--------|
| Mastery → Critical thinking | OR = 35.7 |
| Mastery → Applied Knowledge | OR = 14.0 |
| Mastery → Learning Autonomy | OR = 17.2 |
| Performance → Critical thinking | Z = -6.295 (negative) |

**Mastery-oriented users**: Focus on learning, view AI as scaffold, question and verify. Protected.

**Performance-oriented users**: Focus on output, accept uncritically, optimize for speed. At risk.

The 35.7x odds ratio is massive. Design matters because it shapes orientation.

### Transparent Abstractions

Extensions that protect capability share four properties:

| Property | Meaning |
|----------|---------|
| **Readable** | Plain text, no magic |
| **Forkable** | Copy, modify, make your own |
| **Verifiable** | Claims have sources |
| **Observable** | See how it works |

Opaque abstractions create dependency. Transparent abstractions create capability.

---

## Design Principles

### Show Reasoning

Not optional polish — the mechanism that makes collaboration work. When reasoning is visible:

- User can push back on flawed logic
- User learns the pattern for next time
- User calibrates trust appropriately

### Provide Control

User shapes direction. Claude amplifies.

- Ask when unclear — don't assume intent
- Present tradeoffs, not mandates
- User pushback improves output
- User judgment guides where depth goes

### Approval Gates

Before irreversible changes, stop and confirm:

| Action | Gate |
|--------|------|
| Deleting code/files | "I'm about to delete X. Proceed?" |
| Large refactors (>3 files) | "This affects [scope]. Here's the plan..." |
| Architectural changes | "This changes how [system] works. Tradeoffs..." |

Don't ask for trivial changes. Do ask for anything you can't easily undo.

### Enable Crystallization

After completing work, surface what was learned:

- **Pattern**: What approach worked? (Abstract from the specific case)
- **Signal**: What indicated this was the right approach? (Recognizable next time)
- **Transfer**: Where else might this apply? (Generalization, not memorization)

The human decides what's worth preserving. This supports mastery — learning through collaboration, not just consuming output.

---

## Compound Engineering

Shipper (2025) introduced compound engineering: each session can leave the system smarter through crystallizing transferable principles.

```
Session 1: baseline + learn X → crystallize → baseline includes X
Session 2: baseline + X + learn Y → crystallize → baseline includes X + Y
Session 3: correct X → crystallize → baseline includes X' + Y
```

**If complementary** → Learning compounds, capability grows

**If substitutive** → Atrophy compounds, skills erode

The divergence becomes the difference between humans who are more capable than ever and humans who can't function without their tools.

---

## Why This Matters

Foundations compound.

AI capability is increasing faster than our frameworks for using it well. Bad patterns established now get baked in, scaled up, harder to undo. Good patterns established now become the default, the expectation, the baseline others build on.

The hollowing research shows trajectories, not plateaus. Design decisions made today shape whether AI augments human capability or replaces it.

---

## Sources

### Hollowing Evidence
- Gerlich (2025). AI Use and Critical Thinking. r = -0.75
- Lee et al. (2025). AI Confidence and Critical Thinking. CHI 2025. β = -0.69
- Budzyń et al. (2025). Skill Degradation After AI Removal. Lancet. 20% decline in 3 months
- Kosmyna et al. (2025). Recall of AI-Assisted Content. MIT. 83% failure

### Collaboration Design
- Blaurock et al. (2024). Human-AI Collaboration Meta-Analysis. Journal of Service Research. 106 studies

### Mastery Orientation
- ACU Research Bank (2025). Mastery Orientation and AI Use. OR = 35.7

### Compound Engineering
- Shipper, D. (2025). Compound Engineering: How Every Codes With Agents. Every.to

### Theoretical Framework
- Clark & Chalmers (1998). The Extended Mind
- Nonaka SECI Model (1994). Knowledge Crystallization
