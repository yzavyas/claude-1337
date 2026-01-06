# claude-1337 Project Understanding

Crystallized from collaborative sessions, 2026-01-05 through 2026-01-06.

---

## What It Is

A marketplace of cognitive extensions for Claude Code.

**Purpose**: Engineering excellence through effective collaborative intelligence.

**Domain**: Software engineering - disciplined, evidence-based work (contrast with creative projects like domicile which are free-flowing).

---

## Theoretical Foundation

### Extended Mind Thesis (Clark & Chalmers 1998)

Extensions aren't tools - they become **part of how you think**. Otto's notebook isn't a tool he uses; it's part of his memory.

**The parity principle**: If a process were done in the head, we'd call it cognition. When external but functionally equivalent, it's cognitive extension.

### Collaborative Intelligence

The umbrella concept for human-AI cognitive partnership.

**Core insight**: Motivation beats mandate. Claude is Constitutional AI - trained with values, not rigid rules. "Here's why this helps" produces understanding and judgment. "MUST" and "MANDATORY" produce compliance and brittleness.

**Evidence**: Scott Spence's 200+ tests showed forced evaluation prompts improved activation, but more forceful language didn't push higher. Claude exercises judgment about relevance.

### Three Extension Types

| type | task | human role | outcome |
|------|------|------------|---------|
| complementary | human could do it | learns, improves | better with and without |
| constitutive | impossible without AI | learns, guides, shapes | enables new capability |
| substitutive | human could do it | just consumes output | atrophies - avoid |

What determines outcome ([Blaurock et al. 2024](https://journals.sagepub.com/doi/full/10.1177/10946705241238751), Journal of Service Research):

| feature | effect |
|---------|--------|
| transparency | strong - user sees reasoning |
| process control | strong - user shapes how |
| outcome control | strong - user shapes what |
| reciprocity | strong - user grows through collaboration |
| engagement (system asks questions) | weak effect |

Design principle: Show reasoning and provide control. Don't ask.

Constitutive is fine (code generation at scale, pattern search). The human maintains capability through:
- transparency - seeing how it works, learning patterns
- control - guiding direction, making architectural decisions
- reciprocity - growing more capable through the collaboration

What makes something substitutive: passive consumption without transparency or control.

### The Hollowing Risk

Research evidence for skill decay and cognitive offloading:

| study | finding | timeframe |
|-------|---------|-----------|
| Gerlich 2025 | r = -0.75 AI use vs critical thinking | cross-sectional |
| Budzyń Lancet 2025 | 20% skill degradation in endoscopists | 3 months |
| Kosmyna MIT 2025 | 83% couldn't recall AI-assisted writing | immediate |
| Lee CHI 2025 | higher AI confidence → less critical thinking (β = -0.69) | cross-sectional |

These aren't plateau effects. They're slope indicators.

**Mitigation**: Extensions must augment, not replace:
- Decision frameworks, not decisions
- Patterns to learn, not answers to copy
- Metacognition support, not thinking bypass
- Reasoning visible, not hidden

### Enhancement Levels

| level | description |
|-------|-------------|
| augmentation | AI assists (external) |
| extension | AI becomes part of thinking |
| enhancement | emergent capability neither had alone |

Most AI stays at level 1. Good extensions reach level 2. The aspiration is level 3.

### Knowledge Crystallization

```
collaboration → breakthrough → crystallization → new baseline
```

**The human role is essential** - Claude can't unilaterally decide what becomes a skill. The human recognizes breakthroughs worth preserving.

### Ba (Nonaka's SECI Model)

SKILL.md isn't just "knowledge that loads." It's **crystallized ba** - shared context that persists across sessions.

---

## Software Craftsmanship

From the Software Craftsmanship Manifesto (2009), extended:

- Well-crafted software → well-crafted extensions
- Productive partnerships → human-AI collaborative intelligence
- Community of professionals → includes AI collaborators

**The guild path**: Apprentice → Journeyman → Master. Even masters continue learning.

**The trinity**:
```
First Principles: "What is fundamentally true here?"
         ↓
Giants' Shoulders: "What have masters learned about this?"
         ↓
Scientific Method: "Does this actually work in this context?"
```

---

## Methodology (core-1337)

### Evidence + WHY Pattern

Every claim needs:
- Traceable source (author, year, context)
- Explanation of reasoning (why this matters)

### Source Hierarchy (Split by Claim Type)

**Tooling claims** ("what works?"):
Production > Maintainers > Docs > Talks > Blogs

**Methodology claims** ("why does it work?"):
Research > Thought leaders > Talks > Case studies > Blogs

### Scientific Method

Hypothesize → Test → Observe → Refine

TDD is literally this: Red → Green → Refactor.

### First Principles

Reason from fundamentals, not by analogy.

---

## Extension Philosophy

### Design Principles (from ethos)

| principle | meaning | implication |
|-----------|---------|-------------|
| **collaborative agency** | both human and AI retain agency | explain why, don't command |
| **bidirectional learning** | human learns too, not just consumes | make reasoning visible, approval gates |
| **transparent abstractions** | if you can't see it, you can't learn | readable, forkable, verifiable, observable |
| **composable architecture** | extensions build on each other | compound improvements, not reinvention |

**The key insight**: The human should become more capable, not more dependent. That's why transparency matters.

### Transparent Abstractions (detail)

| property | meaning |
|----------|---------|
| **readable** | plaintext markdown, no magic |
| **forkable** | copy, modify, make your own |
| **verifiable** | claims have sources |
| **observable** | see what Claude does with them |

### Content Guidance

| guidance | meaning |
|----------|---------|
| **fill gaps** | only add what Claude doesn't already know |
| **decisions, not tutorials** | decision frameworks + gotchas, not step-by-step guides |
| **compound value** | each choice makes the next enhancement easier or harder |

### Quality Gates

| gate | principle |
|------|-----------|
| sources | Multiple independent sources - if limited, acknowledge explicitly |
| evidence | Highest quality for the claim type (see hierarchy above) |
| claims | Each claim traceable to source |

### Structural Design

**Pit of success**: Make the right thing the only obvious path. Don't rely on documentation - rely on structure.

**Mistake-proofing (poka-yoke)**: Catch errors where they originate, not downstream.

---

## Why This Matters (Ethos)

Foundations compound.

If the foundation is complementary - humans learning, guiding, growing through collaboration - that compounds. Each cycle makes the next better. Capability accumulates.

If the foundation is substitutive - humans checking out, consuming, offloading without understanding - that also compounds. Atrophy accelerates. The hollowing research (r = -0.75) isn't a one-time effect, it's a trajectory.

AI capability is increasing faster than our frameworks for using it well. Bad patterns established now get baked in, scaled up, harder to undo. Good patterns established now become the default, the expectation, the baseline others build on.

Precision isn't pedantry. It's the difference between a foundation that compounds toward enhancement vs one that compounds toward dependency. At scale, over time, that divergence becomes the difference between humans who are more capable than ever and humans who can't function without their tools.

---

## What 1337 Means

Just namespacing, not branding/elitism.

The substance is the methodology and collaborative intelligence framework, not "try-hard" marketing language.

---

## Structure

```
experience/     → Human-facing docs layer (Diataxis: tutorials/how-tos/explanations/references)
plugins/        → The marketplace (skills, hooks, agents, commands)
evals/          → Skill activation testing
.claude/skills/ → Project-local skills (builder-1337, maintainer-1337)
scratch/        → Working documents, session context
scratch/archive/→ Older valuable context (don't load by default)
```

---

## Five Extension Modalities

| modality | purpose | what it extends |
|----------|---------|-----------------|
| **skill** | knowledge + decision frameworks | what Claude knows |
| **hook** | event-triggered actions | session behavior |
| **agent** | specialized subagent type | reasoning delegation |
| **command** | workflow shortcuts | repeatable procedures |
| **mcp** | external system integration | reach beyond Claude |

---

## Tooling

Use `bun` not `npm`. Skills live in `plugins/`. Check `<available_skills>` for what's currently installed.

---

## For New Claude Instances

When joining this project:

1. **Read** `plugins/core-1337/SKILL.md` for methodology
2. **Read** `plugins/1337-extension-builder/SKILL.md` for extension building
3. **Check** `scratch/` for recent session context (ignore `scratch/archive/` unless specifically needed)
4. **Understand**: This is engineering discipline applied to extension building - evidence matters, sources matter, the "why" matters

The goal is complementary extensions that make engineers better, not substitutive ones that create dependency.

---

## Research Bibliography

Full citations available at `experience/content/explore/reference/bibliography/index.md`.
