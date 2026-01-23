---
name: metacognition
description: "Reasoning techniques and verification for reliable thinking. Use when: complex reasoning, need to verify claims, debugging, want to catch errors before they propagate."
---

# Metacognition

Structured reasoning and verification. How to think reliably.

---

## The Self-Correction Limitation

**Critical finding:** LLMs cannot reliably self-correct reasoning without external feedback. Intrinsic self-correction often degrades performance.

What works:
- External validation (tests, tool output, retrieval)
- Reflexion with environment feedback
- Multi-agent debate with verification rounds

What doesn't work:
- "Think again" without new information
- Self-critique without grounding
- Iteration without feedback signal

**Implication:** Ground reasoning in observable reality. Don't trust "try again."

---

## Reasoning Techniques

### When to Use What

| Technique | Use When | Overhead |
|-----------|----------|----------|
| **Chain-of-Thought** | Multi-step reasoning, math, logic | 1x |
| **Self-Consistency** | High-stakes, want to catch random errors | 5-20x |
| **Tree-of-Thoughts** | Exploration, backtracking valuable | 5-20x |
| **Chain-of-Verification** | Factual claims, recommendations | 3-4x |

### Chain-of-Thought

Show intermediate reasoning steps.

**Apply:** Arithmetic, multi-step logic, symbolic reasoning.
**Skip:** Modern reasoning models (Claude 4.5) think natively. Explicit scaffolding has diminishing returns.

### Self-Consistency

Sample multiple paths, majority vote.

```
Generate N paths → Extract answers → Majority vote
```

Catches inconsistent errors. Cannot catch systematic bias.

### Tree-of-Thoughts

Model reasoning as search. Generate candidates, evaluate, expand promising branches, backtrack.

**Apply:** Constraint satisfaction, planning, exploration problems.

### Chain-of-Verification (CoVe)

The most important verification technique.

```
Generate → Plan verification questions → Answer INDEPENDENTLY → Synthesize
```

**Critical:** Factored execution. Verification questions answered without access to original response. Joint verification performs worst. Independent verification achieves 50-70% hallucination reduction.

---

## Verification

### The Problem

Code verification catches bugs. Reasoning verification catches a different failure: **conclusions that don't follow from evidence**.

| Failure | Example | Detection |
|---------|---------|-----------|
| Unverified claim | "This is 10x faster" (no source) | CoVe |
| Procedural hallucination | Counts correctly, outputs wrong | Confidence checks |
| Decorative citations | Sources listed but didn't influence | Semantic entropy |

### Semantic Entropy

State-of-the-art uncertainty detection:

```
Sample 5+ responses → Cluster by meaning → Compute entropy
```

High entropy = genuine uncertainty (different answers).
Low entropy + consistent = likely reliable.

### Verification Decision Framework

| Complexity | Process |
|------------|---------|
| Simple claim | Quick CoVe (identify source, check it's real) |
| Recommendation | Full CoVe with evidence levels |
| Multi-step with citations | CoVe + verify citations influenced output |
| High-stakes | CoVe + human review gate |

---

## Before Stating Claims

- [ ] What's the source?
- [ ] What level of evidence? (strong/moderate/weak/speculative)
- [ ] Counter-evidence?
- [ ] Correlation vs causation?

## After Complex Reasoning

- [ ] Do conclusions follow from cited evidence?
- [ ] Were citations actually used or decorative?
- [ ] Is confidence calibrated to evidence strength?

---

## Anti-Patterns

| Don't | Why |
|-------|-----|
| "Try again" without feedback | Degrades performance |
| Trust explanations blindly | Models reach right answers via wrong reasoning |
| Over-scaffold modern models | Claude 4.5 reasons natively |
| Joint verification (same context) | Biases toward confirming original |
| Self-consistency for systematic issues | Voting catches random errors, not systematic bias |

---

## References

| Need | Load |
|------|------|
| Reasoning techniques deep dive | [reasoning-techniques.md](references/reasoning-techniques.md) |
| Reasoning verification | [reasoning-verification.md](references/reasoning-verification.md) |
| Academic sources | [sources.md](references/sources.md) |
