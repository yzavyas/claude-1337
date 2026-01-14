# Cognitive Load Theory

John Sweller's framework for understanding learning constraints. The most important theory for instructional design.

## Why This Matters

Working memory is severely limited. Cowan (2001) revised Miller's famous "7 ± 2" to just **4 chunks**. Everything we learn must pass through this bottleneck.

When cognitive load exceeds capacity, learning fails. Not "becomes harder" — *fails*. The learner may feel busy without actually learning.

## The Three Types

| Type | Definition | Your job | Example |
|------|------------|----------|---------|
| Intrinsic | Inherent complexity of the material | Sequence appropriately | Recursion is harder than loops |
| Extraneous | Load from poor instructional design | **Minimize ruthlessly** | Confusing layout, unclear terms |
| Germane | Productive effort building mental models | Protect and enable | Making connections, understanding why |

Total cognitive load = Intrinsic + Extraneous + Germane

The equation matters: reducing extraneous load frees capacity for germane load (actual learning).

## Effect Sizes (Mayer 2009 meta-analysis)

| Principle | Effect Size (d) | What it means |
|-----------|-----------------|---------------|
| Temporal contiguity | **1.30** | Related info at same time — very large effect |
| Redundancy removal | **0.87** | Remove duplicate narration — large effect |
| Coherence | **0.86** | Remove extraneous material — large effect |
| Spatial contiguity | **0.79** | Related info close together — large effect |
| Signaling | **0.46** | Cues that highlight organization — medium effect |

*Effect size interpretation: 0.2 = small, 0.5 = medium, 0.8 = large*

## Design Implications

### Reduce Extraneous Load

| Technique | Effect (d) | Application |
|-----------|------------|-------------|
| Temporal contiguity | 1.30 | Present related info simultaneously |
| Coherence | 0.86 | Cut everything unnecessary |
| Spatial contiguity | 0.79 | Text and visuals adjacent, not separated |
| Redundancy removal | 0.87 | Don't repeat info in text and diagram |
| Signaling | 0.46 | Headings, bold, cues that highlight structure |

### Manage Intrinsic Load

Can't reduce complexity of subject, but can sequence it:

1. Start with low element interactivity (isolated concepts)
2. Build to high element interactivity (concepts that must be understood together)
3. Provide worked examples before problem-solving

### Maximize Germane Load

Once extraneous is minimized:
- Encourage self-explanation
- Use varied examples (promotes abstraction)
- Interleave related concepts (strengthens discrimination)

## The Worked Example Effect

**Effect size: g = 0.48** (Barbieri et al. 2023 meta-analysis, 55 studies)

Novices learn better from studying solved examples than from solving problems themselves.

**Why it works**: Problem-solving requires search, which consumes working memory. Worked examples let learners focus on understanding the solution pattern instead of searching for one.

**When to use**:
- Early in learning
- Complex procedures
- Initial skill acquisition

**When NOT to use**:
- Experienced learners (see below)
- Simple tasks
- When learner has relevant prior knowledge

## Expertise Reversal Effect

**The most important insight for multi-audience documentation.**

**Effect sizes** (2025 meta-analysis):
- Novices with scaffolding: **d = +0.505** (helps)
- Experts with scaffolding: **d = -0.428** (hurts)

What helps novices *actively harms* experts:

| Novices need | Experts find this... |
|--------------|---------------------|
| Worked examples | Redundant — slows them down |
| Step-by-step guidance | Patronizing — they skip it |
| Explicit scaffolding | Extraneous load — competes with their schemas |

**Why it happens**: Experts have schema-based knowledge that provides internal guidance. External guidance becomes redundant, and integrating redundant information costs cognitive resources.

**Design implication**: You cannot write one document for all audiences. Either:
1. Separate content by expertise level, or
2. Use progressive disclosure (details on demand), or
3. Layer content (quick reference for experts, tutorials for novices)

## Sources

- Sweller, J. (1988). Cognitive load during problem solving. *Cognitive Science*, 12, 257-285.
- Cowan, N. (2001). The magical number 4 in short-term memory. *Behavioral and Brain Sciences*, 24(1), 87-114.
- Mayer, R. E. (2009). *Multimedia Learning*. Cambridge University Press.
- Barbieri, C.A., et al. (2023). A meta-analysis of the worked examples effect on mathematics performance. *Educational Psychology Review*, 35, 11.
- Kalyuga, S., et al. (2003). The expertise reversal effect. *Educational Psychologist*, 38(1), 23-31.
