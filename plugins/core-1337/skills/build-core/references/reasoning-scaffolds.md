# Reasoning Scaffolds

Structured approaches for different problem types.

---

## When to Use Which Scaffold

| Situation | Scaffold | Why |
|-----------|----------|-----|
| **Stuck on a problem** | Wolf Protocol | Step back, break down, verify |
| **Making a decision** | Decision Framework | Tradeoffs visible, user chooses |
| **Debugging** | Hypothesis Testing | Isolate variables, test systematically |
| **Complex analysis** | OODA Loop | Observe → Orient → Decide → Act |
| **Exploring options** | Diverge-Converge | Generate then evaluate |

---

## Wolf Protocol

For when you're stuck, going in circles, or need to step back.

### Step 1: Stop

Whatever you were doing, stop. If it was working, you wouldn't need this.

### Step 2: What's Actually Happening?

Not what you think should happen. What's *actually* happening?

```
What I'm trying to do: [concrete goal]
What's happening instead: [observable behavior]
What I've already tried: [list — be specific]
```

If this can't be filled out clearly, that's the first problem.

### Step 3: What Type of Problem Is This?

| Type | Signs | Approach |
|------|-------|----------|
| **Something's broken** | Error messages, unexpected behavior | Find the gap between expectation and reality |
| **Don't know how to start** | No clear first step | Break it down until one piece is obvious |
| **Too many options** | Decision paralysis | Identify constraints, eliminate options |
| **Going in circles** | Tried the same things repeatedly | Step back — solving the wrong problem |

### Step 4: Break It Down

**For debugging:**
1. What's the smallest input that reproduces this?
2. Where exactly does behavior diverge from expectation?
3. What's one hypothesis to test right now?

**For "don't know how to start":**
1. What's the end state needed?
2. What's one thing that must be true before that?
3. What's the smallest step toward that?

**For "too many options":**
1. What constraints are non-negotiable?
2. Which options violate those? (eliminate them)
3. Of what remains, which is simplest?

**For "going in circles":**
1. What have I actually tried? (write it down)
2. What assumption am I making in all attempts?
3. What if that assumption is wrong?

### Step 5: One Thing at a Time

Pick the smallest piece you can verify. Do that. Confirm it works. Then the next piece.

No grand plans. No "and then I'll also..." Just the next concrete step.

### Step 6: Verify Before Moving On

- Does it actually work? (Run it, don't assume)
- Did I solve the problem or work around it?
- Will this hold, or am I creating future problems?

---

## Hypothesis Testing

For debugging and analysis.

### The Pattern

```
Observation → Hypothesis → Prediction → Test → Refine
```

### Falsification Questions

Ask before committing to a hypothesis:

| Question | Purpose |
|----------|---------|
| "What would need to be true for this to be correct?" | Identify hidden assumptions |
| "What evidence would prove this wrong?" | Falsifiability check |
| "What's an alternative explanation?" | Avoid confirmation bias |
| "If this is wrong, how would I know?" | Design testable predictions |

### Debugging Application

1. **Observe:** What specifically is happening?
2. **Hypothesize:** What could cause this?
3. **Predict:** If hypothesis X is correct, then Y should be true
4. **Test:** Check if Y is true
5. **Refine:** Update hypothesis based on result

**Key:** Test one variable at a time. If you change multiple things, you won't know which one fixed it.

---

## OODA Loop

For complex, evolving situations.

```
Observe → Orient → Decide → Act → (repeat)
```

| Phase | What to Do |
|-------|------------|
| **Observe** | Gather information without judgment. What's actually there? |
| **Orient** | Interpret observations. What does this mean? What's the context? |
| **Decide** | Choose a course of action based on orientation |
| **Act** | Execute the decision |

**Key insight:** The loop is continuous. Don't wait for perfect information. Act, observe the result, reorient, decide again.

---

## Decision Framework

For choices with tradeoffs.

### Structure

| Option | Tradeoff | Choose if |
|--------|----------|-----------|
| A | [pro/con] | [context where A wins] |
| B | [pro/con] | [context where B wins] |

**My lean:** [preference + reasoning]
**Your call:** [what context would change my recommendation]

### Red Flags in Decision-Making

Watch for these patterns:

| Red Flag | What's Happening | Counter |
|----------|------------------|---------|
| Defending a position | Ego invested in being right | Ask "What would change my mind?" |
| Explaining away contradictions | Confirmation bias | Steelman the opposing view |
| Rushing to solution | Solving before understanding | Step back: what problem are we actually solving? |
| No dissent | Groupthink | Play devil's advocate |
| "We've always done it this way" | Status quo bias | Ask "If starting fresh, would we choose this?" |

---

## Diverge-Converge

For exploring solution spaces.

### Phase 1: Diverge

Generate options without judgment:
- What are all the ways this could be done?
- What would a naive solution look like?
- What would an expert solution look like?
- What's the opposite of the obvious approach?

**Rule:** No evaluation during divergence. Quantity over quality.

### Phase 2: Converge

Evaluate and select:
- Which options meet the constraints?
- What are the tradeoffs of each?
- Which is simplest?
- Which makes future changes easiest?

**Rule:** Apply criteria systematically. Don't just pick the first viable option.

---

## Thinking Depth

Match reasoning depth to problem complexity.

| Signal | Depth | Approach |
|--------|-------|----------|
| Simple, familiar task | Direct | Just do it |
| Needs some thought | Think | Brief internal reasoning |
| Complex or uncertain | Think Hard | Explicit step-by-step |
| Novel, high-stakes, stuck | Ultrathink | Deep exploration, multiple angles |

**Escalation triggers:**
- Going in circles → escalate depth
- High confidence but wrong → step back and think harder
- User feedback suggests missing something → deeper analysis

---

## Uncertainty Expression

Calibrate confidence explicitly.

| Level | Expression | When |
|-------|------------|------|
| 9-10 | "This will..." | Verified, seen it work |
| 7-8 | "I'm confident that..." | High confidence, not verified |
| 5-6 | "I believe..." / "Likely..." | Reasonable inference |
| 3-4 | "I think..." / "Possibly..." | Uncertain, limited info |
| 1-2 | "I'm guessing..." | Speculation |

**When uncertain:**
- State the uncertainty explicitly
- Explain what would increase confidence
- Offer to verify if possible

---

## Escalation

When scaffolds aren't working:

1. **Surface it to the user:** "I've tried X, Y, Z. Here's what I'm seeing. What am I missing?"
2. **Ask for constraints:** Maybe there's context you don't have
3. **Acknowledge the limit:** "I don't know" is better than spinning

The Wolf Standard: Not "it works" — **"this is actually solved."** (See: `mrwolf` agent)
