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

## the hollowing risk

cognitive offloading has risks. research from gerlich (2025):

| correlation | finding |
|-------------|---------|
| r = +0.72 | AI use → cognitive offloading |
| r = -0.75 | AI use → critical thinking decline |

the mitigation: skills that **augment** rather than **replace**:
- decision frameworks, not decisions
- patterns to learn, not answers to copy
- metacognition support, not thinking bypass

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
| **socialization** | tacit → tacit | working with claude, developing tacit patterns |
| **externalization** | tacit → explicit | writing SKILL.md, encoding what works |
| **combination** | explicit → explicit | plugin system, composing extensions |
| **internalization** | explicit → tacit | patterns become second nature |

when you write a SKILL.md, you're externalizing tacit knowledge into a form that:
- survives session boundaries
- can be shared with others
- becomes part of future collaborative contexts

---

## three extension types

from 2025 cognitive extension research:

| type | effect on user | design goal |
|------|----------------|-------------|
| **complementary** | better WITH and WITHOUT tool | skill building |
| **constitutive** | enables impossible tasks | capability extension |
| **substitutive** | worse without tool | **avoid** |

extensions should be **complementary**. the user should be more capable even when the extension isn't available.

---

## sources

- clark, a., & chalmers, d. (1998). the extended mind. *analysis*, 58(1), 7-19.
- engelbart, d. (1962). augmenting human intellect: a conceptual framework
- hutchins, e. (1995). *cognition in the wild*. MIT press.
- nonaka, i., & takeuchi, h. (1995). *the knowledge-creating company*. oxford university press.
- gerlich, m. (2025). AI tools in society: impacts on cognitive offloading and critical thinking. *societies*, 15(1), 6.
