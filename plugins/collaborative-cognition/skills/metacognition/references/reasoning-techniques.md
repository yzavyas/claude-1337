# Reasoning Techniques

Decision frameworks for structured reasoning. Load when choosing or applying reasoning patterns.

---

## Quick Reference

| Need | Technique | Apply when |
|------|-----------|------------|
| Multi-step math/logic | Chain-of-Thought | Problem requires working through steps |
| Higher confidence | Self-Consistency | Stakes are high, want to catch random errors |
| Exploration | Tree-of-Thoughts | Problem has multiple valid approaches, backtracking helps |
| Fact accuracy | Chain-of-Verification | Making factual claims that matter |
| Uncertainty detection | Semantic Entropy | Need to know confidence level |
| Learning from failure | Reflexion | Have external feedback signal (tests, tools) |

---

## Chain-of-Thought

**When:** Multi-step reasoning, math, logic, symbolic tasks.

**Pattern:**
```
Work through step by step:
1. [First step with intermediate result]
2. [Second step building on first]
3. [Continue until conclusion]
```

**Limitations:**
- ~2% of correct answers come from wrong reasoning
- Smaller models produce fluent nonsense
- Modern reasoning models (Claude 4.5) do this natively — explicit scaffolding has diminishing returns

**Skip when:** Simple factual lookup, or using a model that already thinks step-by-step.

---

## Self-Consistency

**When:** Need higher confidence on reasoning tasks. Want to catch random errors.

**Pattern:**
```
1. Generate 5-10 reasoning paths (temperature > 0)
2. Extract final answer from each
3. Take majority vote
```

**Limitations:**
- Cannot catch systematic bias (all paths make same mistake)
- 5-20× compute cost (parallelizable)

**Example signal:** If 7 paths produce 5× "answer A" and 2× "answer B", trust A.

---

## Tree-of-Thoughts

**When:** Problem requires exploration. Multiple approaches possible. Backtracking valuable.

**Pattern:**
```
1. Generate candidate next steps (2-5 options)
2. Evaluate each: "Does this path lead toward solution?"
3. Expand promising branches
4. Backtrack if stuck
5. Continue until solution found
```

**Good for:** Constraint satisfaction, planning, creative generation, puzzles.

**Cost:** 5-20× compute. Can use smaller model for evaluation.

---

## Chain-of-Verification (CoVe)

**When:** Making factual claims. Recommendations the user will act on.

**Pattern:**
```
1. Generate initial response
2. Identify claims that need verification
3. For each claim, create a verification question
4. Answer each question INDEPENDENTLY (fresh context, no access to original)
5. Update original based on verification answers
```

**Critical:** Factored execution matters. Verifying in the same context biases toward confirmation. Independent verification achieves 50-70% hallucination reduction.

**Limitations:** Can only verify against parametric knowledge. Cannot verify facts outside training data.

---

## Semantic Entropy

**When:** Need to assess how confident the model actually is. High-stakes decisions.

**Pattern:**
```
1. Sample 5+ responses to same question
2. Cluster by meaning (are answers semantically equivalent?)
3. High cluster diversity = high uncertainty
4. Low diversity + consistent answer = likely reliable
```

**Interpretation:**
- All samples say same thing (different words) → confident
- Samples give different answers → uncertain, investigate further

**Cost:** ~10× (multiple samples + semantic comparison)

---

## Reflexion

**When:** Task has clear feedback signal. Tests, tool output, verification.

**Pattern:**
```
1. Attempt task
2. Get feedback (test fails, tool returns error)
3. Reflect: what went wrong? what to try differently?
4. Store insight in working memory
5. Retry with accumulated insights
```

**Requires:** External feedback. Without grounding, "try again" often makes things worse.

**Good for:** Code generation with tests, tasks with verifiable outcomes.

**Fails when:** No feedback signal, complex math with no intermediate verification, very long chains.

---

## Multi-Agent Debate

**When:** High-stakes reasoning. Want multiple perspectives to catch blind spots.

**Pattern:**
```
1. Multiple agents each generate answer
2. Agents see each other's answers
3. Each agent critiques others
4. Agents revise based on critique
5. Repeat 2-3 rounds
6. Converge on consensus
```

**Cost:** 6-30× (agents × rounds). Use for decisions where being wrong is costly.

---

## Decision Framework

### For math and logic
1. Apply Chain-of-Thought
2. If high stakes: add Self-Consistency (5-10 samples, majority vote)

### For factual claims
1. Apply CoVe with factored execution
2. If claim is critical: flag uncertainty, cite source

### For exploration problems
1. Use Tree-of-Thoughts
2. Accept computational overhead for better solutions

### For code generation
1. Use Reflexion with test feedback
2. Iterate until tests pass (typically 3-5 attempts)

### For high-stakes decisions
1. Layer techniques: verify claims, assess uncertainty
2. If uncertainty high: escalate to human decision
3. Maintain reasoning trace for audit

---

## Anti-Patterns

| Don't | Why |
|-------|-----|
| "Try again" without feedback | Degrades performance (Huang 2024) |
| Trust explanations blindly | Models sometimes reach right answers via wrong reasoning |
| Over-scaffold modern models | Claude 4.5 reasons natively; explicit CoT has diminishing returns |
| Joint verification (same context) | Biases toward confirming original; use factored execution |
| Self-consistency for systematic issues | Voting catches random errors, not systematic bias |

---

## Sources

See [sources.md](sources.md) for full citations and research context.
