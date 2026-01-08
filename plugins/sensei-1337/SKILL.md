---
name: sensei-1337
description: "Teaching and information sharing across all contexts. Use when: writing docs, explaining concepts, making presentations, teaching in conversation, curating documentation, technical writing for impact."
---

# sensei-1337

Teaching is about impact, not just clarity. Make knowledge land with the people who need it.

## The Purpose

Feynman didn't simplify physics because simplicity is nice. He simplified because he wanted physics to *matter* — to reach people, to change how they see the world.

Teaching isn't about explaining. It's about:
- Reaching the person who needs the information
- Overcoming their resistance to change
- Speaking their language
- Making the case land

The best understanding in the world doesn't matter if it stays locked in your head.

## The Teaching Progression

Four stages, in order. Each builds on the last.

### 1. Psychology → Why do they resist?

People don't change just because they understand. Resistance is wired in: status quo bias, loss aversion, identity threat, effort aversion.

- Motivation beats mandate — "here's why" produces judgment, "MUST" produces brittleness
- Meet them where they are — are they aware there's a problem, or in denial?
- Teaching against resistance requires different techniques than teaching willing students

See: [psychology-of-change](references/psychology-of-change.md)

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
| Evaluator | "METR 2025 RCT: 19% slowdown vs. 20% perceived speedup. Methodology here." |
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

Sensei applies to all teaching contexts:

| Context | Sensei applies |
|---------|----------------|
| Documentation | Yes |
| Conversation | Yes — explain concepts, answer questions |
| Code review | Yes — explain why, not just what |
| Presentations | Yes — structure for impact |
| Any explanatory output | Yes |

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
- [psychology-of-change](references/psychology-of-change.md) — resistance and motivation
- [audience-empathy](references/audience-empathy.md) — understanding who you're teaching
- [rhetoric-for-impact](references/rhetoric-for-impact.md) — BLUF, inverted pyramid, translation
- [collection-architecture](references/collection-architecture.md) — organizing multiple documents
- [information-architecture](references/information-architecture.md) — where content lives, findability
- [cognitive-load](references/cognitive-load.md) — working memory and learning
- [diataxis](references/diataxis.md) — document types
- [feynman-technique](references/feynman-technique.md) — simplification method
- [reading-patterns](references/reading-patterns.md) — how people scan
- [ai-writing-antipatterns](references/ai-writing-antipatterns.md) — what to avoid
