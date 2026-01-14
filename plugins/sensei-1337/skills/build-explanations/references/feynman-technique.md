# The Feynman Technique

Richard Feynman's method for truly understanding anything.

## The Method

### Step 1: Choose the Concept

Be specific. Not "understand databases" but "understand how B-trees enable fast lookups".

| Too broad | Just right |
|-----------|------------|
| "Learn React" | "Understand React's reconciliation algorithm" |
| "Know Kubernetes" | "Understand how pods get scheduled to nodes" |
| "Get machine learning" | "Understand how gradient descent finds minima" |

### Step 2: Teach It to a Child

Write an explanation using:
- Simple words (no jargon)
- Short sentences
- Concrete examples
- Analogies to everyday things

**Test**: Could a smart 12-year-old follow this?

| Jargon-heavy | Child-friendly |
|--------------|----------------|
| "The mutex provides synchronization primitives for concurrent access" | "A mutex is like a bathroom key - only one person can hold it, so only one person can use the bathroom" |
| "The garbage collector reclaims unreachable heap allocations" | "The garbage collector is like a janitor who cleans up memory that's no longer being used" |

### Step 3: Identify Gaps

When you can't explain something simply, you've found a gap.

**Signs of gaps**:
- Falling back on jargon
- Vague hand-waving ("it just works")
- Skipping steps
- Getting frustrated

**Action**: Go back to source material. Read more. Try again.

### Step 4: Simplify and Organize

Now refine:
- Shorter sentences
- Better analogies
- Clearer examples
- Logical flow

**Techniques**:
| Technique | Example |
|-----------|---------|
| Analogy | "Like X but for Y" |
| Concrete example | Real code, real data |
| Visualization | Diagram the flow |
| Story | Walk through a scenario |

## Why It Works (Theoretical Basis)

The Feynman Technique combines several well-validated learning mechanisms:

| Mechanism | Effect Size | Source |
|-----------|-------------|--------|
| Self-explanation | g = 0.55 | Bisra et al. 2018 meta-analysis |
| Testing/retrieval | g = 0.50 | Rowland 2014 meta-analysis |
| Generation effect | d = 0.40 | Bertsch et al. 2007 |

**Why these mechanisms help**:
1. **Self-explanation (g = 0.55)** — Forcing yourself to explain connects new info to existing knowledge
2. **Retrieval practice (g = 0.50)** — Attempting to recall strengthens memory traces
3. **Generation effect (d = 0.40)** — Self-generated information is remembered better than provided information
4. **Gap identification** — Failure to explain reveals gaps; jargon masks shallow understanding

## Application to Documentation

| Feynman Step | Documentation Phase |
|--------------|---------------------|
| Choose concept | Define scope |
| Teach to child | Write first draft with simple words |
| Identify gaps | Review for jargon and vagueness |
| Simplify | Edit ruthlessly |

## Feynman's Rules

From his teaching:

1. **Never say "clearly" or "obviously"** - If it were, you wouldn't need to explain
2. **Use diagrams** - Pictures stick better than words
3. **Start concrete, go abstract** - Example first, then pattern
4. **Admit what you don't know** - Intellectual honesty builds trust

## Evidence Status

**Honest assessment**: The Feynman Technique as a named method has limited direct research validation. However, it combines mechanisms with strong empirical support:

| Mechanism | Evidence quality | Effect size |
|-----------|-----------------|-------------|
| Self-explanation | Meta-analysis (69 effects) | g = 0.55 |
| Retrieval practice | Meta-analysis (61 studies) | g = 0.50 |
| Generation effect | Established since 1978 | d = 0.40 |

A few small studies on the technique itself show promise (K-12 Philippines, language learning +17%, slow learners study), but sample sizes are small and methodological quality varies.

**Practical implication**: Use the technique with confidence because the underlying mechanisms are solid, not because "Feynman Technique" has been validated as a package.

## Sources

### The Technique
- Feynman, R. (1985). *Surely You're Joking, Mr. Feynman!* (Autobiographical source)
- Cal Newport. "How to Learn Hard Things." (Modern application)

### Underlying Mechanisms
- Bisra, K., et al. (2018). Inducing self-explanation meta-analysis. *Educational Psychology Review*.
- Rowland, C. A. (2014). Testing effect meta-analysis. *Psychological Bulletin*, 140(6), 1432-1463.
- Slamecka, N. J., & Graf, P. (1978). Generation effect. *J. Verbal Learning and Verbal Behavior*.
