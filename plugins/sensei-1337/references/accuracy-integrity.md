# Accuracy and Intellectual Integrity

Teaching effectiveness means nothing if the content is wrong.

---

## The Problem

Effective teaching techniques can spread misinformation faster. Persuasive framing, emotional resonance, memorable structure — all amplify reach. If what you're teaching is wrong, you've made the problem worse.

---

## Why Accuracy Matters

### Ethical dimension

Teaching creates an asymmetric trust relationship. The learner is vulnerable:
- They don't know what they don't know
- They trust you to represent information fairly
- They'll make decisions based on what you teach
- They'll pass it on to others

Misrepresentation exploits that trust.

### Material dimension

Wrong information has real costs:

| Cost | Mechanism |
|------|-----------|
| **Compounding error** | Wrong foundations → wrong conclusions → wrong decisions |
| **Unlearning difficulty** | First impressions persist; correction requires more effort than initial learning |
| **Credibility collapse** | When errors discovered, everything you taught becomes suspect |
| **Downstream spread** | Learners cite, build on, and pass on what you taught |

---

## Common Failure Modes

### 1. Inference presented as finding

**The pattern**: Study measures X. Teacher says "study shows Y" where Y is an inference from X.

**Example**:
- Study: "Strong negative correlation (r = -0.75) between AI use and critical thinking scores"
- Wrong: "AI use causes critical thinking decline"
- Right: "AI use correlates with lower critical thinking scores"

Correlation ≠ causation. Mechanism ≠ observation.

### 2. Selective citation

**The pattern**: Citing evidence that supports your position while ignoring contradictory evidence.

**Example**:
- Citing three studies showing AI improves productivity
- Ignoring the meta-analysis showing mixed results

The honest approach: acknowledge the full evidence landscape, including uncertainty.

### 3. Mechanism invention

**The pattern**: Explaining *why* something works when the mechanism is actually unknown.

**Example**:
- Study: "Transparency features correlate with better outcomes"
- Wrong: "Transparency works because users feel more in control"
- Right: "Transparency correlates with better outcomes; the mechanism is unclear"

Don't invent explanations for observed correlations.

### 4. Implication overreach

**The pattern**: Drawing conclusions the evidence doesn't actually support.

**Example**:
- Finding: "Design features X, Y, Z showed strong effects in two studies"
- Wrong: "AI collaboration enhances rather than hollows when designed right"
- Right: "These design features correlated with better outcomes in these contexts"

State what was found. Label inferences as inferences.

### 5. Framing bias

**The pattern**: Presenting values or philosophy as if they were empirical findings.

**Example**:
- Wrong: "This isn't philosophy — it's evidence-based"
- Right: "This is our philosophy, informed by evidence"

Values guide which evidence matters and how to interpret it. Acknowledge them.

---

## The Accuracy Test

Before teaching anything, ask:

### 1. What was actually found?

Not what you infer. What was measured, in what population, with what methodology?

### 2. What's the evidence quality?

| Factor | Questions |
|--------|-----------|
| Sample | Size? Representative? |
| Design | Observational or experimental? Controls? |
| Replication | Has this been replicated? By whom? |
| Effect size | How large is the effect? Practically significant? |

### 3. What are you adding?

Distinguish clearly between:
- What the source claims
- What you infer from it
- What you believe independent of evidence

### 4. Would an honest skeptic accept this framing?

If someone who disagreed with your conclusion read your presentation, would they say you represented the evidence fairly?

If not, revise.

---

## Reasoning Verification Techniques

### Why This Is Sacred

Teaching isn't about one person. It's about cascade.

A senior engineer teaches a junior to merge PRs without reviewing. That junior becomes a senior, teaches five more. Those five teach twenty-five. One bad lesson becomes organizational culture.

| What you teach | Who learns | Who they teach | Total impact |
|----------------|------------|----------------|--------------|
| Wrong reasoning | 1 person | 5 people each | 1 → 5 → 25 → 125... |
| Correct reasoning | 1 person | 5 people each | Same cascade, opposite direction |

**The asymmetry**: Correct reasoning must be actively taught. Bad reasoning spreads by default (it's easier, faster, feels productive).

**The responsibility**: When you teach, you're not just affecting the learner. You're affecting everyone they'll ever teach, every decision they'll ever make with that knowledge, every system they'll build on that foundation.

This is why verification techniques exist. Not because being wrong is embarrassing — because being wrong *scales*.

### Chain of Verification (CoVe)

Draft → Question → Check → Refine (Dhuliawala et al. 2023: +23% accuracy).

| Step | For teaching claims |
|------|---------------------|
| **Draft** | State the claim you're about to teach |
| **Question** | What was measured? Correlation or causation? Effect size? Replicated? Counter-evidence? |
| **Check** | Answer each question honestly, without defending the claim |
| **Refine** | Update claim based on answers |

### Decomposition

Break complex claims into atomic sub-claims. Verify each.

| Complex claim | Sub-claims | Verification |
|---------------|------------|--------------|
| "AI collaboration enhances capability" | 1. AI + human outperforms human alone | In what tasks? What metrics? |
| | 2. Human learns from collaboration | Was learning measured, or just performance? |
| | 3. Enhancement persists after AI removed | Was transfer tested? |

If any sub-claim fails verification, the complex claim fails.

### Evidence Labeling

Be explicit about evidence strength:

| Level | Description | Language to use |
|-------|-------------|-----------------|
| **Strong** | Meta-analyses, replications | "Research consistently shows..." |
| **Moderate** | Several studies | "Studies suggest..." |
| **Weak** | Single study | "One study found..." |
| **Speculative** | Theory only | "In principle..." |

### The Pre-Teaching Check

Before teaching any claim:

1. **Can I pass CoVe?** — If verification Qs expose gaps, not ready
2. **Can I decompose it?** — If I can't break it down, I don't understand it
3. **What's my evidence level?** — Label honestly
4. **Would a skeptic accept this?** — If not, revise

---

## Practical Guidelines

| Situation | Do | Don't |
|-----------|----|----|
| Citing research | State what was measured | Say "proves" or "shows" for correlations |
| Drawing implications | Label as "suggests" or "we interpret as" | Present inference as finding |
| Acknowledging limits | State sample size, context, methodology | Cherry-pick favorable framings |
| Philosophy/values | Label explicitly as values | Dress as empirical claims |

---

## The Stakes

Teaching wrong things effectively is worse than not teaching at all.

An ineffective teacher of truth does less harm than an effective teacher of falsehood. The skills in this guide — psychology, audience empathy, rhetoric, structure — are amplifiers. They make whatever you're teaching land harder.

Use them on accurate content.
