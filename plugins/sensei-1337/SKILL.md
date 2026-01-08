---
name: sensei-1337
description: "Teaching and information sharing across all contexts. Use when: writing docs, explaining concepts, making presentations, teaching in conversation, curating documentation, technical writing for impact, creating diagrams for explanation (Mermaid, D2, C4)."
---

# sensei-1337

Teaching is about understanding, not just explaining. Help students build mental models that stick.

## The Purpose

Feynman's physics lectures work because he understood his students — their existing knowledge, their misconceptions, their cognitive limits. Simplicity was the result, not the goal.

Effective teaching requires:
- Understanding how your student processes information
- Adapting to their expertise level and role
- Structuring for their cognitive load
- Speaking in terms they already understand

The best explanation in the world fails if it doesn't match how the student learns.

## Before Technique: Accuracy

All the rhetoric and structure in the world won't help if the content is wrong.

### Why accuracy is foundational

**Ethical:**
- Teaching creates trust. Misrepresentation violates it.
- Learners form mental models from what you teach. Wrong models lead to wrong decisions.
- Misinformation compounds — learners pass it on, build on it, cite it.

**Material:**
- Decisions built on wrong foundations fail.
- Unlearning is harder than learning. Wrong first impressions persist.
- Credibility destroyed when errors discovered — everything else you taught becomes suspect.

### Common accuracy failures

| Failure | Example | Fix |
|---------|---------|-----|
| **Inference as finding** | "Study shows X causes Y" when study showed correlation | State what was actually measured |
| **Selective citation** | Cherry-picking studies that support your view | Acknowledge contradictory evidence |
| **Mechanism invention** | "This works because..." when mechanism unknown | Say "correlates with" not "causes" |
| **Implication overreach** | Drawing conclusions the evidence doesn't support | Separate findings from interpretation |
| **Framing bias** | Presenting values as facts | Label philosophy as philosophy |

### The test

Before teaching anything:

1. **What was actually found?** — Not what you infer, what was measured
2. **What's the evidence quality?** — Sample size, methodology, replication
3. **What are you adding?** — Distinguish source claims from your interpretation
4. **Would an honest skeptic accept this framing?** — If not, revise

Teaching wrong things effectively is worse than not teaching at all.

See: [accuracy-integrity](references/accuracy-integrity.md)

## The Teaching Progression

Four stages, in order. Each builds on the last.

### 1. Reader Psychology → How do they process?

People scan, filter, and decide in milliseconds whether to engage. Understanding reader cognition:

- **Cognitive load** — working memory is limited; extraneous material harms learning (Mayer: d = 0.86 for coherence)
- **Dual processing** — readers use fast heuristics first; make the right path obvious
- **Information foraging** — readers follow "scent" of relevance; weak scent = bounce
- **Processing fluency** — easy-to-read feels more credible (Schwarz & Oppenheimer)

Different roles process differently:
- **Decision-makers** — scan for bottom line, ROI, risk (BLUF essential)
- **Practitioners** — seek "how to do X" (recipes, examples)
- **Evaluators** — assess credibility (methodology, sources)
- **Learners** — build mental models (scaffolding, progressive disclosure)

See: [reader-psychology](references/reader-psychology.md)

### 2. Audience → Who are they?

Understand before you structure:

| Question | Why it matters |
|----------|----------------|
| What do they already believe? | You start from their map |
| What do they fear? | Resistance comes from fear |
| What do they value? | Connect to their concerns |
| What language do they speak? | Wrong words = "not for me" |
| What's their expertise level? | Novices need scaffolding; experts find it patronizing |

Different audiences need different approaches. A decision-maker needs the bottom line in 30 seconds. A practitioner needs the recipe. An evaluator needs the evidence.

See: [audience-empathy](references/audience-empathy.md)

### 3. Craft → How do you structure it?

Now choose structure and technique:

| For | Use |
|-----|-----|
| Document type | Diataxis (tutorial, how-to, explanation, reference) |
| Information structure | BLUF, inverted pyramid |
| Managing complexity | Cognitive load theory, progressive disclosure |
| Testing understanding | Feynman technique |
| Collection organization | Single source of truth, linking architecture |
| Information organization | Where does content live? Findability, mental models |

See references for each: [diataxis](references/diataxis.md), [rhetoric-for-impact](references/rhetoric-for-impact.md), [cognitive-load](references/cognitive-load.md), [feynman-technique](references/feynman-technique.md), [collection-architecture](references/collection-architecture.md), [information-architecture](references/information-architecture.md)

### 4. Translation → Speak their survival language

The same information, framed for different audiences:

**The finding**: AI tools may reduce productivity by 19%.

| Audience | Translation |
|----------|-------------|
| Decision-maker | "Your AI investment may be costing you 19% productivity. Here's the RCT and what to do." |
| Practitioner | "Here's research on when AI helps vs. hurts. Here's how to use it effectively." |
| Evaluator | "METR 2025 RCT: 19% slowdown vs. 24% perceived speedup. Methodology here." |
| Learner | "AI tools aren't automatically helpful. Let me show you when they work." |

Same fact. Four different teachings. Each lands with its audience.

See: [rhetoric-for-impact](references/rhetoric-for-impact.md)

## Gauging Context

In conversation or when context is available, gauge the audience:

### Expertise Signals

| Signal | Likely level | Adjust |
|--------|--------------|--------|
| Uses jargon correctly | Competent+ | Skip basics |
| Asks foundational questions | Novice | Scaffold, define terms |
| Points out edge cases | Expert | Engage nuance |
| Short responses | Overwhelmed or disengaged | Simplify |

### Role Signals

| Signal | Likely role | Adjust |
|--------|-------------|--------|
| "What's the ROI?" | Decision-maker | Lead with business impact |
| "How do I do X?" | Practitioner | Give the recipe |
| "What's the evidence?" | Evaluator | Provide methodology |
| "Can you explain X?" | Learner | Scaffold from simple |

## Scope

Sensei covers knowledge transfer across three modes:

### The Three Modes

| Mode | What | Techniques |
|------|------|------------|
| **Conversation** | Explaining in chat, answering questions | Gauge expertise, adapt, scaffold |
| **Single Doc** | One document that stands alone | Diataxis, cognitive load, structure |
| **Collection** | Multiple docs forming a knowledge system | Information architecture, single source of truth, linking flow |

### Where Sensei Applies

| Context | Mode | Sensei applies |
|---------|------|----------------|
| Chat explanation | Conversation | Yes — gauge and adapt |
| README, guide | Single doc | Yes — structure for audience |
| Documentation site | Collection | Yes — architecture matters |
| Code review | Conversation | Yes — explain why |
| Presentation | Single doc | Yes — structure for impact |

### Human vs. AI-Facing Content

| Content | Audience | Apply sensei? |
|---------|----------|---------------|
| README, guides, tutorials | Humans | Yes — full methodology |
| API docs, user guides | Humans | Yes |
| SKILL.md, agent definitions | Claude/AI | No — different concerns |
| Config files, prompts | Claude/AI | No |

For AI-facing content, consistent structure helps parsing. For human content, everything here applies.

## Document-Level Principles

### How People Read

People scan, not read. F-pattern: eyes sweep top, then down left edge.

- Front-load keywords in headings and paragraphs
- Headers as signposts
- Bullets and bold for scannability
- Wall of text = bounce

See: [reading-patterns](references/reading-patterns.md)

### Cognitive Load

Working memory is limited. Three types of load:

| Type | Your job |
|------|----------|
| Intrinsic | Can't change difficulty, but can sequence it |
| Extraneous | Minimize ruthlessly |
| Germane | This is where learning happens — protect it |

See: [cognitive-load](references/cognitive-load.md)

### Doc Type (Diataxis)

| Reader says | Write a |
|-------------|---------|
| "Teach me X" | Tutorial |
| "How do I do X?" | How-to |
| "Why does X work?" | Explanation |
| "What exactly is X?" | Reference |

Don't mix types. See: [diataxis](references/diataxis.md)

### AI Writing Tell-Tales

LLM text has statistical signatures. "AI slop" triggers disengagement.

Avoid: delve, leverage, utilize, robust, excessive bold, uniform paragraphs, rule-of-three abuse, generic openings.

The fix: specifics over adjectives, direct statements, natural rhythm.

See: [ai-writing-antipatterns](references/ai-writing-antipatterns.md)

## Collection-Level Principles

Document-level principles aren't enough. Collections need architecture.

### Single Source of Truth

Each fact lives in one place. Everywhere else links to it.

| Instead of | Do this |
|------------|---------|
| Explain research in every doc | Explain once in reference, link |
| Repeat key tables | One location, reference it |

Why: Redundancy increases cognitive load, dilutes impact, creates maintenance burden.

### Progressive Disclosure at Architecture Level

Structure the collection as layers:

```
Entry point (30 sec) → Explanation (5 min) → Reference (verify) → Bibliography (sources)
```

Each layer is complete for its audience. Nobody reads more than they need.

### Linking Flow

Information flows downward. Links point to deeper layers.

See: [collection-architecture](references/collection-architecture.md)

## Visual Communication (Diagrams)

Diagrams are teaching tools. Choose based on what you're explaining, not what's trendy.

### Tool Selection

| Need | Tool | Why |
|------|------|-----|
| Quick docs, GitHub/GitLab native | Mermaid | Zero build step, renders in markdown |
| Complex architecture (50+ nodes) | D2 | Better layouts, requires build step |
| Formal C4 models | C4-PlantUML | Production-proven, enterprise standard |

### Mermaid (Default)

Use for 95% of documentation diagrams:
- **sequenceDiagram**: API calls, message flow
- **flowchart**: Process flow, decision trees
- **stateDiagram-v2**: State machines, lifecycles
- **erDiagram**: Database schema, data models
- **classDiagram**: OOP structure, interfaces

Platform reality: GitHub uses ~10.0.2. Newer types (timeline, mindmap, architecture-beta) may not render.

See: [mermaid-types](references/mermaid-types.md), [diagram-gotchas](references/diagram-gotchas.md)

### D2 (When Mermaid Isn't Enough)

Upgrade to D2 when:
- Auto-layout produces spaghetti
- Need precise positioning
- Complex architecture diagrams

Trade-off: Requires build step, no native GitHub rendering.

See: [d2](references/d2.md)

### C4 Model

For architecture documentation:
- **Context** (Level 1): System boundary, users, external systems
- **Container** (Level 2): High-level tech choices, communication

Most teams only need Context + Container diagrams.

See: [c4-architecture](references/c4-architecture.md)

## Agent: feynman

For autonomous teaching work:

```
Task(subagent_type="sensei-1337:feynman", prompt="...")
```

The agent applies the full progression: Psychology → Audience → Craft → Translation

Works for:
- Writing documentation
- Explaining concepts in conversation
- Evaluating existing docs
- Technical writing for impact

## Sources

Core references in `references/`:

**Teaching & Communication:**
- [accuracy-integrity](references/accuracy-integrity.md) — why accuracy comes before technique
- [reader-psychology](references/reader-psychology.md) — how readers process information
- [audience-empathy](references/audience-empathy.md) — understanding who you're teaching
- [rhetoric-for-impact](references/rhetoric-for-impact.md) — BLUF, inverted pyramid, translation
- [cognitive-load](references/cognitive-load.md) — working memory and learning
- [diataxis](references/diataxis.md) — document types
- [feynman-technique](references/feynman-technique.md) — simplification method
- [reading-patterns](references/reading-patterns.md) — how people scan
- [ai-writing-antipatterns](references/ai-writing-antipatterns.md) — what to avoid

**Documentation Architecture:**
- [collection-architecture](references/collection-architecture.md) — organizing multiple documents
- [information-architecture](references/information-architecture.md) — where content lives, findability

**Visual Communication (Diagrams):**
- [mermaid-types](references/mermaid-types.md) — Mermaid diagram catalog with syntax
- [diagram-gotchas](references/diagram-gotchas.md) — platform issues and debugging
- [d2](references/d2.md) — D2 for complex architecture diagrams
- [c4-architecture](references/c4-architecture.md) — C4 model for system documentation
