# ethos

cognitive extensions for enhanced collaborative intelligence

---

## the positioning

claude-1337 builds **cognitive extensions** — not tools, not plugins, not add-ons.

the difference matters:

| term | relationship | integration |
|------|--------------|-------------|
| **tool** | external, used but separate | pick up, put down |
| **plugin** | modular addition | installed but distinct |
| **extension** | expands existing capability | becomes part of cognition |

when you use a calculator, it's a tool. when you can't remember phone numbers because your phone does, that's cognitive extension — the boundary between "you" and "your tools" has blurred.

---

## extended mind thesis

the theoretical foundation comes from clark & chalmers (1998):

> if a process in the world functions as a cognitive process, it *is* a cognitive process — regardless of whether it happens inside or outside the skull.

their famous example: otto has alzheimer's and uses a notebook to remember things. inga uses biological memory. if we'd call inga's process "remembering," we should call otto's process "remembering" too — even though otto's memory lives in a notebook.

**the parity principle**: if it were done in the head, we'd call it cognition. when external but functionally equivalent, it's cognitive extension.

### applied to claude-1337

| component | what it provides |
|-----------|-----------------|
| skills | knowledge, decision frameworks |
| commands | workflow shortcuts |
| agents | specialized reasoning |
| hooks | context injection |
| mcp | external system integration |

plugins extend the capabilities of the human + AI system.

---

## ba: shared context space

from nonaka's knowledge creation theory (SECI model), **ba** is the shared context where knowledge creation happens.

three types of ba in claude-1337:

| ba type | manifestation | persistence |
|---------|---------------|-------------|
| **ephemeral ba** | conversation session | dies when session ends |
| **crystallized ba** | SKILL.md files | permanent, version-controlled |
| **structural ba** | codebase, project context | long-lived, evolving |

### why SKILL.md works

a skill isn't just "knowledge that loads on demand." it's **crystallized ba** — shared context that persists across sessions.

when you write a SKILL.md, you're externalizing tacit knowledge into a form that:
- survives session boundaries
- can be shared with others
- becomes part of future collaborative contexts

this is the SECI cycle in action:

| mode | in claude-1337 |
|------|----------------|
| **socialization** | working with claude, developing tacit patterns |
| **externalization** | writing SKILL.md, encoding what works |
| **combination** | plugin system, composing extensions |
| **internalization** | patterns become second nature |

---

## multi-modal extensions

the ecosystem supports five modalities:

| modality | what it extends |
|----------|-----------------|
| **skills** | knowledge — decision frameworks, expertise |
| **commands** | efficiency — workflow shortcuts |
| **agents** | reasoning — specialized problem-solving |
| **hooks** | context — session behavior, environment |
| **mcp** | reach — access to external data, agency on external systems |

together they extend knowledge, efficiency, reasoning, context, and reach.

---

## the ratchet mechanism

collaboration with AI produces a specific pattern:

```
collaboration → breakthrough → permanent augmentation → new baseline → enhanced collaboration
```

each cycle:
1. human + AI collaborate on a problem
2. breakthrough insight emerges (neither would reach alone)
3. knowledge crystallizes into permanent form (SKILL.md, documentation)
4. new baseline enables more sophisticated collaboration
5. repeat at higher level

this is **progressive augmentation**, not dependency. each cycle leaves permanent gains while enabling new frontiers.

### evidence from practice

- learning semiotics through collaboration → now permanently accessible
- discovering SECI applies to AI plugins → crystallized into methodology
- finding 84% activation rate fix → encoded in core-1337 hook

the ratchet only turns forward.

---

## empirical foundations: what the research says

### the meta-analysis (vaccaro et al., 2024)

the flagship study: 106 experiments, 370 effect sizes, preregistered systematic review in *nature human behaviour*.

| finding | implication |
|---------|-------------|
| human-AI combos often **worse** than best alone (g = -0.23) | don't assume collaboration always helps |
| **content creation**: gains | skills for building, writing, creating |
| **decision-making**: losses | frameworks, not decisions |
| synergy is rare | design for augmentation, not replacement |

### cognitive offloading (gerlich, 2025; lee et al., CHI 2025)

empirical correlations from 319 knowledge workers:

| correlation | finding |
|-------------|---------|
| r = +0.72 | AI use → cognitive offloading |
| r = -0.68 | AI use → critical thinking decline |
| β = -0.69 | confidence in AI → reduced critical thinking |

the more we trust AI to think for us, the less we think critically.

### the perception-reality gap (METR, 2025)

RCT with 16 experienced open-source developers, 246 real issues:
- actual: **19% slower** with AI tools
- perceived: **20% faster**

we systematically misjudge AI's impact on our work.

### design implications

| principle | implementation in claude-1337 |
|-----------|------------------------------|
| **augment, don't replace** | decision frameworks, not decisions |
| **enable validation** | readable skills, explicit boundaries |
| **support metacognition** | skills explain patterns, not just apply |
| **preserve autonomy** | user chooses, user controls, user validates |

forcing skills to activate violates autonomy. that's why the observability principle matters.

---

## the autonomy principle

from the extended mind thesis: cognitive extension requires **integration**, not **compliance**.

otto's notebook works because he trusts it and uses it naturally. if someone forced him to check the notebook before every thought, it would break the cognitive coupling.

same with claude and skills:

| approach | result |
|----------|--------|
| "you MUST use skills" | compliance, brittleness, ceiling at ~84% |
| "here's why skills help" | understanding, appropriate judgment |

the 16% non-activation represents appropriate judgment — cases where skills genuinely weren't relevant.

### implementation

core-1337's hook doesn't command. it explains:
- what skills contain (curated, production-tested knowledge)
- why they help (better answers, faster, backed by evidence)
- the process (evaluate, activate if relevant, respond)

understanding over compliance. motivation over mandate.

---

## methodology: how we build extensions

four principles guide extension development:

### 1. standing on giants' shoulders

inherit proven wisdom. the evidence hierarchy:

| priority | source | why |
|----------|--------|-----|
| 1 | production codebases | what actually ships |
| 2 | core maintainers | primary knowledge holders |
| 3 | conference talks | war stories from practitioners |
| 4 | proven adoption | social proof + real usage |
| 5 | technical blogs | secondary, always verify |

### 2. scientific method

hypothesis → test → observe → refine

- write skill with description
- run eval suite, measure F1
- observe false positives and negatives
- improve description based on failures
- repeat until metrics meet threshold

### 3. first principles

reason from fundamentals, question assumptions.

"why does skill activation fail?" → not a bug, emergent behavior from how `<available_skills>` surfaces → description is the only signal → optimize descriptions.

### 4. rigor

evidence-backed decisions. document the trail.

every recommendation has a source. every claim can be verified. updates happen when new evidence emerges.

---

## the composite cognitive system

putting it together:

```
Human Agent ←→ Cognitive Extensions ←→ AI Agent
                      ↓
          Composite Cognitive System
                      ↓
             Emergent Capability
```

neither human nor AI alone produces the same outcomes. the extensions mediate and enhance the collaboration.

evidence: breakthroughs in this project (semiotics learning, SECI application, activation rate research) emerged from collaboration — neither party would have reached them independently.

---

## open questions

this is a living framework. unresolved:

| question | current thinking |
|----------|-----------------|
| experience contingency | should extensions adapt to user sophistication? |
| enhancement measurement | how to validate emergent capability empirically? |
| tacit knowledge boundaries | some knowledge resists externalization (polanyi's paradox) |
| reciprocal enhancement | how do extensions improve through usage? |
| community curation scaling | how to maintain quality as community grows? |

---

## sources

### foundational philosophy

- clark, a., & chalmers, d. (1998). the extended mind. *analysis*, 58(1), 7-19. [paper](https://www.alice.id.tue.nl/references/clark-chalmers-1998.pdf)
- engelbart, d. (1962). augmenting human intellect: a conceptual framework
- hutchins, e. (1995). *cognition in the wild*. MIT press.

### knowledge creation theory

- nonaka, i. (1991). the knowledge-creating company. *harvard business review*
- nonaka, i., & takeuchi, h. (1995). *the knowledge-creating company*. oxford university press.

### collaborative intelligence research (2024-2025)

- vaccaro, m., almaatouq, a., & malone, t. w. (2024). [when combinations of humans and AI are useful: a systematic review and meta-analysis](https://www.nature.com/articles/s41562-024-02024-1). *nature human behaviour*, 8(12), 2293-2303.
- gerlich, m. (2025). [AI tools in society: impacts on cognitive offloading and critical thinking](https://www.mdpi.com/2075-4698/15/1/6). *societies*, 15(1), 6.
- lee et al. (2025). [the impact of generative AI on critical thinking](https://dl.acm.org/doi/10.1145/3706598.3713778). *CHI 2025*.
- METR (2025). [measuring the impact of early-2025 AI on developer productivity](https://arxiv.org/abs/2507.09089). arXiv:2507.09089.
- [human-generative AI collaboration enhances task performance but undermines intrinsic motivation](https://www.nature.com/articles/s41598-025-98385-2). *scientific reports*, april 2025.

### software craftsmanship

- software craftsmanship manifesto (2009): [manifesto.softwarecraftsmanship.org](https://manifesto.softwarecraftsmanship.org/)
- martin, r. c. (2008). *clean code*
- mancuso, s. (2014). *the software craftsman*

---

## next

- [concepts](../concepts.md) — how the plugin system actually works
- [architecture](../architecture/) — technical implementation details
- [autonomy](../autonomy/) — collaborative intelligence patterns
