# Prompt Craft

Engineering prompts for different model architectures. The technique varies by model type.

---

## Model Architectures

| Type | Examples | Technique |
|------|----------|-----------|
| **Autoregressive** | Claude, GPT-4 | Chain-of-thought, structured reasoning |
| **Reasoning/RL** | Gemini Deep Think, o1, o3 | Search space constraints |

The same prompt optimized for Claude will underperform on o1, and vice versa.

---

## Autoregressive Models (Claude, GPT-4)

These models generate token-by-token. They benefit from:

- **Chain-of-thought** — "Think step by step"
- **Structured output** — XML, JSON schemas
- **Role definition** — persona and expertise
- **Examples** — few-shot demonstrations

The model follows the path you lay out.

---

## Reasoning Models (Deep Think, o1)

These models have internal reinforcement learning. They don't need you to tell them HOW to think — they need you to define WHERE to search.

**Key insight:** You're building a gym, not writing instructions.

### The Constraint Philosophy

| Don't | Do |
|-------|-----|
| "Think step by step" | Define the destination |
| "Consider multiple options" | Force triangulation between named positions |
| "Be thorough" | Set electric fences (hard constraints) |
| "Check your work" | Define what failure looks like |

### Core Patterns

**Scenario Injection**
Abstract requests → specific high-stakes simulations.

| Abstract | Injected Scenario |
|----------|-------------------|
| "Check for bugs" | "Simulate a race condition in a high-frequency trading engine" |
| "Critique this plot" | "Rewrite the climax assuming the protagonist fails" |
| "Evaluate this team" | "The team just lost their lead engineer. What breaks first?" |

**Triangulation Constraint**
Force the model to hold conflicting hypotheses simultaneously.

```
Simulate a debate: X wants speed, Y wants safety, Z wants simplicity.
Synthesize a position that addresses all three.
```

**Negative Constraints**
Remove easy outs.

- NO happy paths (force failure handling)
- NO hedging (force decisions)
- NO generic advice (force specificity)

**Technical Density**
Demand domain jargon to anchor the search space.

```
Use terms: idempotency, CRDTs, backpressure, eventual consistency
```

---

## References

- `references/deep-think.md` — Full deep think prompting guide

---

## When to Use This Skill

- Engineering prompts for reasoning models (o1, Deep Think)
- Optimizing existing prompts for different architectures
- Designing agent system prompts
- Creating evaluation criteria that force rigorous thinking
