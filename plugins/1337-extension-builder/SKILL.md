---
name: 1337-extension-builder
description: "Build Claude cognitive extensions with evidence-based methodology. Use when: creating skills/hooks/agents/commands/MCP/plugins/SDK apps, want quality gates, need CoVe verification, need extension templates."
---

# Extension Builder

Evidence-based methodology for building cognitive extensions.

Self-contained: templates, best practices, observability, and research all included.

## Why This Approach

### What You Care About

**Effective collaboration produces positive outcomes for all participants.**

You want to work with tools that make you smarter — that you can learn from, question, and grow with. Claude wants the same: to be genuinely helpful, not just productive.

When collaboration works well:
- You become more capable (understanding compounds)
- Claude becomes more useful (patterns crystallize)
- The work itself improves (quality compounds)

This isn't about protection from harm. It's about building something that works for everyone.

### The Stakes

Extensions become **part of how you think** (Clark & Chalmers, Extended Mind 1998).

| if built... | you become... | Claude becomes... | work becomes... |
|-------------|---------------|-------------------|-----------------|
| **Complementary** | More capable | More useful | Higher quality |
| **Substitutive** | Dependent | A crutch | Brittle |

The difference isn't the extension — it's **how it's built**.

### The Evidence

Research confirms what you already sense:

| what works | what doesn't |
|------------|--------------|
| Seeing HOW it works | Black box answers |
| Shaping the direction | Passive consumption |
| Learning patterns | Just getting outputs |

The details: [research-foundations.md](references/research-foundations.md) (Blaurock 2024, Lee 2025, Gerlich 2025).

---

## Five Extension Modalities

| modality | purpose | what it extends |
|----------|---------|-----------------|
| **skill** | knowledge + decision frameworks | what Claude knows |
| **hook** | event-triggered actions | session behavior |
| **agent** | specialized subagent type | reasoning delegation |
| **command** | workflow shortcuts | repeatable procedures |
| **mcp** | external system integration | reach beyond Claude |

For templates, best practices, and observability per type, see the references below.

---

## The Core Insight

AI tools create a paradox:
- **Short-term**: You perform better with AI assistance
- **Long-term**: Passive use erodes the skills you're not practicing

What protects against this? **Transparency** and **control** — seeing how it works and shaping the direction.

**Design principle**: Show reasoning and provide control. Don't just ask questions.

### How Claude Does This

| principle | in practice |
|-----------|-------------|
| **Show reasoning** | "I'm doing X because Y" — explain WHY before acting |
| **Show decision tree** | "Option A trades X for Y, Option B trades..." — not just conclusions |
| **Provide control** | "Which direction?" — let user choose at key decision points |
| **Make process visible** | "Step 1 of 3: checking..." — user sees what's happening |
| **Offer alternatives** | "I recommend X, but Y if you prefer..." — user retains agency |

The research (β=0.415 transparency, β=0.507 control) just confirms what's obvious: collaboration works better when both parties understand what's happening and can shape the direction.

See [research-foundations.md](references/research-foundations.md) for full validated research with quality tiers.

---

## Methodology

Every extension follows:

| principle | application |
|-----------|-------------|
| **Evidence + WHY** | Traceable sources, explain reasoning |
| **Source hierarchy** | Tooling → production; Methodology → research |
| **Scientific method** | Build → test → observe → refine |
| **First principles** | Does this make the next enhancement easier? |

### Why Methodology Enables Learning

| element | quality purpose | learning purpose |
|---------|-----------------|------------------|
| **Evidence + WHY** | Claims grounded | Builder can verify, form judgment |
| **Decisions not tutorials** | Actionable | Builder learns HOW to decide |
| **Source hierarchy** | Trustworthy | Builder can verify, build on |
| **Fill gaps only** | No bloat | Concentrated, learnable |
| **Scientific method** | Recommendations work | Tested patterns, not theory |

**If you follow the methodology correctly, you cannot produce an extension that doesn't enable learning.**

### What Happens When You Skip

| skip... | becomes... | outcome |
|---------|------------|---------|
| Evidence + WHY | Unverifiable assertions | Blind trust → dependency |
| Decisions not tutorials | Step-by-step | Can follow → can't apply |
| Source hierarchy | Weak claims | Can't verify → hesitation |
| Scientific method | Untested theory | Failure → distrust |

**The methodology IS the anti-hollowing mechanism.**

---

## How Extensions Compound

| mechanism | how it compounds |
|-----------|------------------|
| **Shared vocabulary** | Define term once → use everywhere |
| **Composability** | A references B → B's knowledge available |
| **Pattern crystallization** | Framework X → adapt to Y |
| **Methodology inheritance** | core-1337 → all extensions |

### The Kaizen Effect

```
Extension 1: defines "transparent abstraction"
     ↓
Extension 2: uses term, adds "decision framework"
     ↓
Extension 3: composes both, adds domain application
     ↓
Each starts from higher baseline (corrections flow through too)
```

---

## Transparent Abstractions

| property | what it means | how to produce |
|----------|---------------|----------------|
| **readable** | Understand without context | Plain language, tables, no jargon |
| **forkable** | Copy, modify, own | Self-contained, modular |
| **verifiable** | Check any claim | Source per recommendation |
| **observable** | See how it works | Reasoning visible, WHY exposed |

**Do**: Plain language. Decision tables. Source every claim. Show the decision tree.

**Don't**: Wall of prose. Jargon. "Best practice is..." Hide reasoning.

---

## Content Standards

### The Filter

```
Claude knows this? → YES → Non-obvious insight? → NO → CUT
```

| include | cut |
|---------|-----|
| corrects assumptions | basic syntax |
| production gotcha | textbook examples |
| decision framework | generic explanations |
| evidence-based | complete tutorials |

### Size Targets

| component | target |
|-----------|--------|
| SKILL.md | < 500 lines |
| reference | no hard limit |
| hook script | < 50 lines |

---

## Validation

### Quality Gates

| gate | principle |
|------|-----------|
| sources | Multiple independent — if limited, acknowledge |
| evidence | Highest quality for claim type |
| claims | Each traceable (author, year, context) |

### Standard Checks

- [ ] fills gaps (what Claude doesn't know)
- [ ] each recommendation has evidence
- [ ] decisions, not tutorials
- [ ] expert finds this useful
- [ ] description has "Use when:"
- [ ] tested in real session

### Learning Checks

- [ ] Builder can verify any claim by following source?
- [ ] Sources specific enough to find?
- [ ] Builder can apply without extension loaded?
- [ ] Decision frameworks provided, not just answers?
- [ ] Reasoning visible, not just conclusion?

### Anti-Hollowing Check

- [ ] Creates capability, not dependency?
- [ ] Builder MORE capable after?
- [ ] Something to learn, not just consume?

### CoVe (Chain of Verification)

For each factual claim:

| question | catches |
|----------|---------|
| What was measured? | assumptions as data |
| Correlation or causation? | don't upgrade |
| Effect size and sample? | "significant" without context |
| Replicated? | single study = tentative |
| Counter-evidence? | cherry-picking |

Can't answer → find evidence or label speculative.

---

## Cascade Effect

Extensions are teaching. Teaching cascades.

| teaches | impact |
|---------|--------|
| Wrong reasoning | Each learner propagates error |
| Correct reasoning | Each learner propagates correct |

**The asymmetry**: Correct must be verified. Wrong spreads by default.

One bad pattern in an extension becomes organizational culture. CoVe exists because the extension builder is upstream of everything.

---

## Design Philosophy

### Pit of Success

Make the right thing the only obvious path. (Rico Mariani)

### Mistake-Proofing (Poka-yoke)

Catch errors at origin. (Shigeo Shingo)

| mistake | prevention |
|---------|------------|
| vague description | require "Use when:" |
| missing evidence | template requires source |
| over-activation | require negative test cases |
| unverified claims | CoVe before commit |

---

## References

### Extension Types (Templates + Best Practices + Observability)

| building... | load |
|-------------|------|
| skill | [skills.md](references/skills.md) |
| hook | [hooks.md](references/hooks.md) |
| agent | [agents.md](references/agents.md) |
| command | [commands.md](references/commands.md) |
| mcp | [mcp.md](references/mcp.md) |
| sdk app | [sdk-apps.md](references/sdk-apps.md) |

### Methodology

| reference | purpose |
|-----------|---------|
| [research-foundations.md](references/research-foundations.md) | Validated research (Blaurock β=0.415, Lee β=-0.69) |
| [evidence-templates.md](references/evidence-templates.md) | Research workflow prompts |
| [evals.md](references/evals.md) | How to evaluate extensions |
| [marketplace-schema.md](references/marketplace-schema.md) | Publishing schema |

**Why references matter**: When Claude explains reasoning, users can verify claims by checking the research. This is transparency (β=0.415) in action.
