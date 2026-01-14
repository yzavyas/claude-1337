# Reasoning Verification

Two complementary techniques for catching reasoning failures.

---

## The Problem

Reasoning can fail in two distinct ways:

| Failure Mode | Example | Detection |
|--------------|---------|-----------|
| **Unverified claim** | "This approach is 10x faster" (no source) | CoVe process |
| **Procedural hallucination** | Counts r's in "strawberry" correctly, outputs wrong number | Pythea tools |

CoVe catches claims you never verified. Pythea catches evidence you verified but didn't use.

---

## Chain of Verification (CoVe)

Process-level verification before stating claims.

### The Pattern

```
Draft → Question → Check → Refine
```

| Step | Action |
|------|--------|
| **Draft** | State the claim you're about to make |
| **Question** | What was measured? Correlation or causation? Effect size? Replicated? Counter-evidence? |
| **Check** | Answer each question honestly, without defending the claim |
| **Refine** | Update claim based on answers |

### Evidence: +23% accuracy (Dhuliawala et al. 2023)

CoVe reduces hallucination by 50-70% on factual tasks.

### When to Apply

| Situation | CoVe Required |
|-----------|---------------|
| Stating a statistic | Yes |
| Recommending an approach | Yes |
| Explaining why something works | Yes |
| Describing what code does | No (read the code) |
| Repeating user's request | No |

### Evidence Levels

Label claim strength explicitly:

| Level | Description | Language |
|-------|-------------|----------|
| **Strong** | Meta-analyses, replications | "Research consistently shows..." |
| **Moderate** | Several studies | "Studies suggest..." |
| **Weak** | Single study | "One study found..." |
| **Speculative** | Theory only | "In principle..." |

---

## Pythea: Procedural Hallucination Detection

Output-level verification after reasoning chains.

### The Problem

> "Ask Claude to count the r's in 'strawberry.' It writes 's-t-r-a-w-b-e-r-r-y,' identifies each r, gets to 3. Then outputs '2.' The model didn't lack information. The answer was right there - in text it generated moments earlier. The computation worked. The routing failed."

This is **procedural hallucination**: correct information generated but not used.

### Detection Method

1. Scrub cited evidence from the response
2. Re-generate without it
3. Measure confidence change
4. No change = evidence was decorative, not functional

### Tools

When Pythea MCP server is configured:

| Tool | Use When |
|------|----------|
| `mcp__pythea__detect_hallucination` | After complex reasoning chains with citations |
| `mcp__pythea__audit_trace_budget` | Quantifying information budget vs. reliability |

### When to Apply

| Situation | Pythea Check |
|-----------|--------------|
| RAG retrieval + synthesis | Yes - verify retrieved docs influenced output |
| Multi-step reasoning | Yes - verify each step used prior steps |
| Chain-of-thought with citations | Yes - verify citations aren't decorative |
| Simple factual lookup | No - overkill |
| Code that can be run | No - just run the code |

---

## Integrated Workflow

### Before Complex Reasoning

```
1. Identify claims to be made
2. Run CoVe on each:
   - What's the evidence?
   - What level (strong/moderate/weak)?
   - Counter-evidence?
3. Proceed with verified claims only
```

### After Complex Reasoning

```
1. Did the output cite evidence?
2. Does the conclusion follow from that evidence?
3. If uncertain: run Pythea detect_hallucination
4. If evidence was decorative: re-derive conclusion
```

### Decision Framework

| Complexity | Process |
|------------|---------|
| **Simple claim** | Quick CoVe (30 seconds) |
| **Researched recommendation** | Full CoVe with evidence levels |
| **Multi-step with citations** | CoVe + Pythea verification |
| **High-stakes conclusion** | CoVe + Pythea + human review |

---

## The Information Budget

From arXiv 2509.11208 ("Predictable Compression Failures"):

Hallucinations aren't random - they're predictable compression failures. The model has an **information budget** per response. When complexity exceeds budget, failures occur at predictable points.

### Implications

| Factor | Effect on Budget |
|--------|------------------|
| Long reasoning chains | Depletes budget |
| Many citations | Depletes budget (if actually used) |
| Familiar patterns | Lower cost |
| Novel combinations | Higher cost |

### Practical Use

When `audit_trace_budget` shows budget exceeded:
- Break reasoning into smaller steps
- Verify intermediate conclusions
- Use external computation where possible

---

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|--------------|--------------|
| Decorative citations | Looks verified, isn't |
| CoVe theater | Going through motions without honest questioning |
| Over-verification | Verifying trivia, missing important claims |
| Assuming RAG = correct | Retrieved doesn't mean used |

---

## Sources

- Dhuliawala et al. (2023). Chain-of-Verification Reduces Hallucination in Large Language Models. ACL 2024.
- Hassana Labs. [Pythea: LLM Reliability Research](https://github.com/leochlon/pythea). GitHub.
- arXiv 2509.11208. Predictable Compression Failures: Why Language Models Actually Hallucinate.
