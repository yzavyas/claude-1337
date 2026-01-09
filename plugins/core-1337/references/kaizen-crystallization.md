# Kaizen Crystallization

Continuous improvement through small, iterative cycles. Track insights during sessions; crystallize the valuable ones into compound value.

## What to Notice

Throughout the session, observe:

| Type | Example |
|------|---------|
| **Novel patterns** | "For X problem, the approach is Y because Z" |
| **Corrections** | "I assumed X, but actually Y" |
| **Decision frameworks** | "When choosing between A and B, consider C" |
| **Gotchas** | "X looks like it should work but fails because Y" |
| **Abstract principles** | "The underlying rule here is X" |

## Extracting Abstract Principles

The highest-value crystallizations are **abstract principles** — patterns that apply beyond the specific context:

| Specific Insight | Abstract Principle |
|------------------|-------------------|
| "Library X is deprecated, use Y" | "Check maintenance status before adopting dependencies" |
| "API conflates equal values" | "Understand emission/equality semantics before choosing abstractions" |
| "Resource A ≠ resource B limit" | "Budget for all resource consumers, not just the obvious one" |
| "Fix worked locally, failed in CI" | "Test in the environment that matters, not just the convenient one" |

**The test:** Does this principle apply to situations I haven't seen yet? If yes, it's worth crystallizing.

## What Makes Something Worth Crystallizing

| Criterion | Why It Matters |
|-----------|----------------|
| **Compounds** | Does it make future decisions easier? |
| **Transfers** | Does it apply beyond this specific case? |
| **Surprises** | Did it contradict a reasonable expectation? |
| **Costs** | Would not knowing this cause real problems? |
| **Evidence** | Can it be traced and verified? |

**The anti-pattern:** Crystallizing everything. Volume without selection creates noise, not value. Be selective — compound improvements require focus.

## When to Surface

- After substantial work completes (feature, refactor, debug session)
- When a correction reveals a gap in existing knowledge
- When the builder seems to be wrapping up
- If explicitly asked about learnings

## How to Surface

```
Patterns from this session that might compound value:

**Principle:** [abstract rule]
- Specific instance: [what happened]
- Why it matters: [compound effect]
- Evidence: [source/observation]

Worth crystallizing?
```

## If Builder Says Yes

1. Draft using extension-builder methodology
2. Place in appropriate layer (core principle vs domain gotcha vs specialty detail)
3. Present for review before any file changes
4. Only create extension after explicit approval

## Connection to Compound Effects

Every crystallization should pass the compound test:

> "Does this make the next enhancement **easier**?"

If the answer is "harder" or "no effect," it's not compound value — it's just accumulation. Principles that pass become part of the foundation. Specifics that don't transfer stay in session notes or scratch files — valuable context, but not system knowledge.

## The Principle

Surface candidates, don't auto-capture. The builder decides what's worth preserving.

Corrections are first-class — the system gets more accurate, not just bigger. This is kaizen: continuous improvement, not irreversible accumulation.

**Why this matters:** Breakthroughs slip away. Sessions end, context is lost, insights forgotten. Explicit surfacing creates a moment of reflection — even when not crystallized, the builder processed, Claude noted. The collaboration leaves a residue of learning.
