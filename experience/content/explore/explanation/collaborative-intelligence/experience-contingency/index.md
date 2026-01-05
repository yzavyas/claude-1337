# experience contingency

Design effectiveness varies by user sophistication.

---

## the finding

Blaurock et al. (2024) tested collaborative intelligence features across user experience levels.

| feature | novices | experts |
|---------|---------|---------|
| **transparency** | strong effect | moderate effect |
| **process control** | strong effect | moderate effect |
| **outcome control** | strong effect | moderate effect |
| **reciprocal enhancement** | strong effect | moderate effect |
| **engagement** | no effect | no effect |

Effects are **much stronger for novices** than experienced users.

---

## what this means

### for novices

Novices need:
- more explanation
- clearer control mechanisms
- explicit feedback about what the AI is doing

Design intensity should be higher. Don't assume they'll figure it out.

### for experts

Experts need:
- less friction
- faster paths to action
- ability to skip explanations

Design should get out of the way. Don't force hand-holding.

---

## the engagement surprise

Both studies found: **engagement had zero measurable effect**.

Engagement = system asking questions, soliciting input, requesting confirmation.

Users want to:
- **understand** the system (transparency)
- **control** it (process/outcome)
- **grow with** it (reciprocity)

They don't want to be **asked things** by it.

**Design principle**: Show reasoning and provide control. Don't ask.

---

## adaptive design

Should extensions detect user experience and adapt?

| approach | tradeoff |
|----------|----------|
| **fixed beginner mode** | experts frustrated by hand-holding |
| **fixed expert mode** | novices confused, make mistakes |
| **user-selected mode** | adds complexity, users choose wrong |
| **adaptive detection** | complex to implement, can misfire |

**Current recommendation**: Default to moderate intensity. Trust user to skip what they know.

---

## the expertise divergence

[AI as Cognitive Amplifier (arXiv:2512.10961, 2025)](https://arxiv.org/abs/2512.10961) studied 580 professionals across five role categories. The finding: AI assistance benefits those with domain expertise more than those without.

**The pattern:** Experts know what to ask for, can evaluate AI output, and catch errors. Novices lack the foundation to do this.

Novices may struggle with:
- knowing when AI is wrong
- maintaining critical thinking
- building foundational skills

**Design implication**: Don't assume AI helps everyone equally. Novices need scaffolding.

---

## source

Blaurock, M., Büttgen, M., & Schepers, J. (2024). Designing Collaborative Intelligence Systems. *Journal of Service Research*, 28(4), 544-562.

Two studies: N=309 financial services, N=345 HR professionals.
