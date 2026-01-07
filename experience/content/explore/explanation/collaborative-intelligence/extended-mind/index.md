# extended mind

the theoretical foundation for cognitive extension

---

## the thesis

clark & chalmers (1998) proposed:

> if a process in the world functions as a cognitive process, it *is* a cognitive process — regardless of whether it happens inside or outside the skull.

their example: otto has alzheimer's and uses a notebook to remember things. inga uses biological memory. if we'd call inga's process "remembering," we should call otto's process "remembering" too — even though otto's memory lives in a notebook.

**the parity principle**: if it were done in the head, we'd call it cognition. when external but functionally equivalent, it's cognitive extension.

---

## tools vs extensions

| tools | extensions |
|-------|------------|
| you invoke them | they're part of thinking |
| external to cognition | integrated into cognition |
| "use this when needed" | "this is how I approach problems now" |
| pick up, put down | cognitive coupling |

a calculator is a tool. but when you can't remember phone numbers because your phone does, that's cognitive extension — the boundary between "you" and "your tools" has blurred.

---

## applied to AI collaboration

the human-AI system becomes a **composite cognitive system**:

```
Human Agent ←→ Cognitive Extensions ←→ AI Agent
                      ↓
          Composite Cognitive System
                      ↓
             Emergent Capability
```

plugins extend the capabilities of this composite system:

| component | what it extends |
|-----------|-----------------|
| skills | knowledge, decision frameworks |
| commands | workflow efficiency |
| agents | specialized reasoning |
| hooks | context injection |
| mcp | reach to external systems |

---

## integration criteria

for something to count as cognitive extension (not just a tool), it must be:

1. **reliably available** — accessible when needed
2. **automatically endorsed** — trusted without constant verification
3. **directly accessible** — low friction to use
4. **functionally integrated** — part of the cognitive workflow

claude-1337 plugins meet these criteria when properly designed:
- they load automatically (reliable availability)
- they're curated and verified (automatic endorsement)
- they activate on relevant prompts (direct access)
- they become part of how Claude reasons (functional integration)

---

## three extension types

from 2024-2025 cognitive extension research:

| type | effect on human | trajectory |
|------|-----------------|------------|
| **complementary** | better WITH and WITHOUT extension | capability accumulates |
| **constitutive** | enables impossible tasks | new capability emerges |
| **substitutive** | worse without extension | capability atrophies |

**complementary**: the human learns through the collaboration. patterns transfer. they're more capable even when the extension isn't available.

**constitutive**: AI enables things humans couldn't do alone — code generation at scale, pattern search across millions of files. the human maintains capability through transparency (seeing how it works) and control (guiding direction).

**substitutive**: the human just consumes output without engagement. capability atrophies. the r = -0.75 correlation (Gerlich 2025) is this pattern at scale.

the same extension can be complementary or substitutive depending on design and usage.

---

## what makes extensions complementary

blaurock et al. (2024) identified five design features that determine outcome:

| feature | effect | how to implement |
|---------|--------|------------------|
| **transparency** | strong positive | show reasoning, not just conclusions |
| **process control** | strong positive | user shapes the approach |
| **outcome control** | strong positive | user shapes the result |
| **reciprocity** | strong positive | both human and AI improve |
| **engagement** | weak/none | asking questions isn't enough |

the critical finding: engagement alone (the system prompting the user) has minimal effect. what matters is transparency and control — the user seeing how it works and shaping the outcome.

**design implication**: don't just ask questions. show reasoning. provide decision frameworks. let the user guide direction.

---

## the hollowing risk

cognitive offloading has documented consequences:

| study | finding | timeframe |
|-------|---------|-----------|
| **Lancet (2025)** | 20% skill degradation in endoscopists | 3 months |
| **MIT (2025)** | 83% couldn't recall their own writing | immediate |
| **CHI (2025)** | higher AI confidence → less critical thinking | cross-sectional |

these aren't one-time effects. they're trajectories. the slope steepens with continued substitutive use.

**the mitigation**: extensions that augment rather than replace:
- decision frameworks, not decisions
- patterns to learn, not answers to copy
- metacognition support, not thinking bypass
- reasoning visible, not hidden

---

## ba: shared context space

from nonaka's SECI model, **ba** is the shared context where knowledge creation happens.

three types of ba in claude-1337:

| ba type | manifestation | persistence |
|---------|---------------|-------------|
| **ephemeral ba** | conversation session | dies when session ends |
| **crystallized ba** | SKILL.md files | permanent, version-controlled |
| **structural ba** | codebase, project context | long-lived, evolving |

SKILL.md isn't just "knowledge that loads on demand." it's **crystallized ba** — shared context that persists across sessions and can be shared with others.

### the SECI cycle

knowledge creation spirals through four modes:

| mode | conversion | in claude-1337 |
|------|------------|----------------|
| **socialization** | tacit → tacit | working with claude, developing patterns |
| **externalization** | tacit → explicit | writing SKILL.md, encoding what works |
| **combination** | explicit → explicit | plugin system, composing extensions |
| **internalization** | explicit → tacit | patterns become second nature |

when you write a SKILL.md, you're externalizing tacit knowledge into a form that:
- survives session boundaries
- can be shared with others
- becomes part of future collaborative contexts

---

## the kaizen loop

Extensions aren't static. The collaboration → breakthrough → crystallization cycle means the system improves with use. The human role is essential: recognizing what's worth preserving.

See [knowledge crystallization](/explore/explanation/collaborative-intelligence/#knowledge-crystallization) for the full pattern.

---

## sources

key references (full citations in [bibliography](/explore/reference/bibliography/)):

- clark & chalmers (1998) — the extended mind thesis
- blaurock et al. (2024) — five design features for collaborative intelligence
- budzyń et al. (2025) — clinical evidence of skill decay
- kosmyna et al. (2025) — cognitive debt in AI-assisted writing
- gerlich (2025) — cognitive offloading and critical thinking
- nonaka & takeuchi (1995) — SECI model, ba concept
