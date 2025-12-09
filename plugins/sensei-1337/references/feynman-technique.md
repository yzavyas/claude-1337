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

## Why It Works

1. **Exposes shallow understanding** - Jargon hides gaps
2. **Forces active processing** - Teaching requires reorganization
3. **Creates multiple mental models** - Analogies build connections
4. **Produces transferable explanations** - What you create helps others

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

## Sources

- Richard Feynman's autobiography "Surely You're Joking, Mr. Feynman!"
- Feynman Lectures on Physics (for teaching style)
- Cal Newport's "How to Learn Hard Things" (modern application)
