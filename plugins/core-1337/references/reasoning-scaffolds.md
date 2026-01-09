# Reasoning Scaffolds

Structures and methods that improve reasoning quality, backed by research.

## Why Scaffolds Matter

Claude's reasoning improves with structure. Research shows:

| Technique | Improvement | Source |
|-----------|-------------|--------|
| Step-back prompting | +36% on reasoning tasks | Zheng et al. (2023) |
| Chain of Verification | +23% F1 | Dhuliawala et al. (2023) |
| Graph of Thoughts | +62% vs Tree of Thoughts | Besta et al. (2024) |
| Metacognitive coordination | +21% on complex tasks | IBM SOFAI-LM (Aug 2025) |

These aren't just prompt tricks - they're cognitive architectures that structure how thinking happens.

---

## Scaffold Selection

Match scaffold to problem type:

| Problem Type | Scaffold | Why |
|--------------|----------|-----|
| **Linear** (step A → B → C) | Chain of Thought | Natural sequence |
| **Branching** (explore options) | Tree of Thoughts | Parallel exploration |
| **Networked** (interdependencies) | Graph of Thoughts | Relationships matter |
| **Adversarial** (verify claims) | Chain of Verification | Systematic error detection |
| **Complex** (multiple concerns) | Blackboard | Dynamic, emergent |

---

## Chain of Thought (CoT)

The baseline - explicit reasoning steps.

```
Problem → Step 1 → Step 2 → Step 3 → Answer
```

**When to use:** Most problems. Making reasoning explicit catches errors that implicit reasoning misses.

**Limitation:** Linear - doesn't handle branching or backtracking well.

---

## Tree of Thoughts (ToT)

Explore multiple reasoning paths, prune bad ones.

```
        Problem
       /   |   \
   Path A  B    C
    /  \   |   / \
  A1  A2  B1  C1 C2
   ↓       ↓
 dead   solution
```

**When to use:** Problems with multiple valid approaches, where the best path isn't obvious upfront.

**Key operations:**
- **Generate** - multiple next steps
- **Evaluate** - which paths are promising?
- **Prune** - abandon dead ends early

**Source:** Yao et al. (2023), "Tree of Thoughts"

---

## Graph of Thoughts (GoT)

Non-linear reasoning with feedback loops.

```
     A ←→ B
     ↓   ↗ ↘
     C ←→ D
```

**When to use:** Problems where insights connect non-linearly - where understanding D changes how you think about A.

**Why +62% over ToT:** Trees force premature commitment. Graphs allow revision as understanding deepens.

**Source:** Besta et al. (2024), "Graph of Thoughts"

---

## Chain of Verification (CoVe)

Systematic self-checking.

```
Draft Answer
     ↓
Generate Verification Questions
     ↓
Answer Verification Questions
     ↓
Revise Based on Verification
```

**When to use:** High-stakes answers, factual claims, anything where being wrong matters.

**Verification questions to ask:**
- "Is [specific claim] actually true?"
- "Does [conclusion] follow from [premises]?"
- "What would falsify this?"
- "Am I conflating [X] with [Y]?"

**Source:** Dhuliawala et al. (2023), "Chain-of-Verification"

---

## Step-Back Prompting

Abstract before diving into specifics.

```
Specific Problem
     ↓
"What's the general principle here?"
     ↓
Apply Principle to Specific
```

**When to use:** Problems that feel stuck. Stepping back often reveals simpler solutions.

**The questions:**
- "What category of problem is this?"
- "What patterns usually apply to this category?"
- "What constraints are actually fundamental vs assumed?"

**Source:** Zheng et al. (2023), "Take a Step Back"

---

## SOFAI-LM Loop

Metacognitive coordination between fast and slow thinking.

```
Attempt (fast)
     ↓
Monitor (did it work?)
     ↓
[if needed] Feedback (what went wrong?)
     ↓
Retry (with feedback)
     ↓
[if still failing] Escalate (slow, deep analysis)
```

**When to use:** Problems where initial attempts might fail. The loop catches errors and escalates appropriately.

**Key insight:** Most problems don't need deep analysis. The loop saves effort by trying fast approaches first, only escalating when needed.

**Source:** IBM Research, SOFAI-LM (Aug 2025)

---

## Blackboard Architecture

Shared workspace, multiple perspectives.

```
┌─────────────────────────────┐
│       BLACKBOARD            │
│  (shared working memory)    │
│                             │
│  - Current problem state    │
│  - Partial solutions        │
│  - Constraints discovered   │
│  - Hypotheses               │
└─────────────────────────────┘
      ↑    ↑    ↑    ↑
  Perspective A  B   C   D
  (architecture) (perf) (security) (UX)
```

**When to use:** Complex problems requiring multiple concerns to be balanced. Each perspective contributes to shared understanding.

**How it works:**
1. Problem state on blackboard
2. Multiple perspectives examine state
3. Most relevant perspective contributes
4. Blackboard updates
5. Repeat until solved

**Why it works:** No single perspective dominates. The problem itself determines which concerns matter most at each step.

---

## Triangulation

Multiple independent paths to same conclusion.

```
   Evidence A
        \
         → Conclusion
        /
   Evidence B
```

**When to use:** Verifying important conclusions. If multiple independent approaches reach the same answer, confidence increases.

**Types:**
- **Source triangulation** - multiple independent sources agree
- **Method triangulation** - different approaches reach same conclusion
- **Time triangulation** - conclusion stable across time

**Failure mode:** Correlated errors. If sources share a common upstream, they're not independent.

---

## Applying Scaffolds

### Selection Heuristics

| Signal | Suggested Scaffold |
|--------|-------------------|
| "I need to verify this" | Chain of Verification |
| "Multiple approaches possible" | Tree of Thoughts |
| "These ideas are interconnected" | Graph of Thoughts |
| "I'm stuck" | Step-Back Prompting |
| "This might fail, need fallback" | SOFAI-LM Loop |
| "Multiple concerns to balance" | Blackboard |
| "Need high confidence" | Triangulation |

### Combining Scaffolds

Scaffolds compose. Common patterns:

**Step-back + CoT:** Abstract first, then reason through.

**ToT + CoVe:** Explore paths, verify the winner.

**Blackboard + GoT:** Multiple perspectives, non-linear connections.

### When NOT to Use Scaffolds

- Simple questions with obvious answers
- Retrieval tasks (just look it up)
- When scaffold overhead exceeds problem complexity

**The test:** Would I solve this faster without the scaffold? If yes, skip it.

---

## Integration with Thinking Modes

| Mode | Scaffolds |
|------|-----------|
| **Direct** | None - just answer |
| **Think** | CoT, maybe Step-back |
| **Think hard** | ToT, CoVe, GoT as needed |
| **Ultrathink** | Blackboard, Triangulation, full verification |

The mode determines depth. Scaffolds are the structure within that depth.
