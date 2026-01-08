# Rhetoric for Impact

Structures and techniques that make information land. From journalism, military communication, and persuasion research.

## Why This Matters

Understanding the audience and having clear information isn't enough. Structure determines whether the message lands. The right structure respects the reader's time, meets their needs immediately, and creates the conditions for change.

Teaching isn't just about clarity — it's about impact. The best research in the world doesn't matter if it's structured in a way nobody reads.

## BLUF: Bottom Line Up Front

From military communication. The conclusion comes first.

### The Pattern

```
[Bottom line / Key point / What you need to know]
[Supporting evidence]
[Background and context]
[Additional details]
```

### Why It Works

| Traditional structure | BLUF structure |
|----------------------|----------------|
| Background → Analysis → Conclusion | Conclusion → Evidence → Background |
| Reader must read everything to get the point | Reader gets the point immediately |
| Busy reader stops before the conclusion | Busy reader gets what they need, can stop |

Decision-makers don't read to the end. Give them the bottom line first.

### Examples

**Traditional (bury the lead):**
> "We conducted a study examining AI tool usage among 16 developers over several months. Using randomized controlled methodology, we measured both perceived and actual productivity impacts. The results showed an interesting divergence between perception and reality..."

**BLUF:**
> "AI tools reduced developer productivity by 19%, despite developers perceiving a 20% improvement. Here's the evidence and what to do about it."

### When to Use

| Context | Use BLUF? |
|---------|-----------|
| Executive communication | Always |
| Status updates | Always |
| Technical recommendations | Yes — lead with recommendation |
| Tutorials | No — learning requires progression |
| Explanations | Sometimes — depends on audience |

## The Inverted Pyramid

From journalism. Most important information first, decreasing importance as you go down.

```
        [Most critical]
      [Important details]
    [Supporting information]
  [Background and context]
[Nice to have / can be cut]
```

### Why It Works

1. **Readers who leave early still get the main point**
2. **Editors can cut from the bottom** without losing essential info
3. **Scanning readers find what they need** at the top

### Applied to Documentation

| Layer | Contains | Reader who stops here gets |
|-------|----------|---------------------------|
| 1 | The key insight | The bottom line |
| 2 | The evidence | Proof it's true |
| 3 | The methodology | How we know |
| 4 | The background | Full context |
| 5 | Related reading | Further exploration |

See also: [reading-patterns.md](reading-patterns.md) for the inverted pyramid in context of how people scan.

## Translation: Speaking Survival Language

Different audiences have different "survival languages" — the terms that connect to what they actually care about.

### The Insight

Information presented in your terms may not resonate. The same information, translated into their survival language, creates urgency.

### Survival Languages by Role

| Role | Survival concerns | Translate into |
|------|-------------------|----------------|
| Decision-maker | Risk, returns, competitive position | Dollars, percentages, market share |
| Practitioner | Effectiveness, craft, time | Concrete improvements, "try this" |
| Evaluator | Being fooled, rigor | Methodology, limitations, effect sizes |
| Learner | Being overwhelmed, looking stupid | Clear steps, encouragement |

### Translation Examples

**The finding**: Collaborative AI approaches outperform default usage.

| For decision-maker | "Teams using these approaches shipped 40% faster with fewer defects. Here's the implementation cost." |
| For practitioner | "Here's a workflow that makes AI actually useful instead of getting in your way." |
| For evaluator | "Meta-analysis of 106 studies (preregistered). Effect size g = 0.34 for structured approaches vs. g = -0.23 for unstructured." |
| For learner | "AI tools aren't magic — but with the right approach, they genuinely help. Let me show you how." |

### The Feynman Connection

Feynman didn't simplify physics because simplicity is nice. He simplified because he wanted physics to *matter* — to reach people, to change how they see the world. Translation is simplification with purpose: making the message land with the specific person who needs to hear it.

## Layered BLUF for Mixed Audiences

When a single document serves multiple audiences:

```markdown
## The Bottom Line
[30-second version for decision-makers]
[The key number. The key risk. The key action.]

## For Practitioners
[5-minute version with actionable guidance]

## The Evidence
[For evaluators who need to verify]

## Deep Dive
[Full context for those who want it]
```

Each section is complete for its audience. Nobody reads more than they need.

## Making the Case Land

### The Structure for Persuasion

1. **Hook**: Connect to something they already care about
2. **Problem**: Make the cost of the current state visceral
3. **Evidence**: Prove the problem is real (in their language)
4. **Solution**: Clear path forward
5. **Action**: Specific next step

### What Doesn't Land

| Approach | Why it fails |
|----------|--------------|
| Leading with background | Busy readers leave before the point |
| Burying the evidence | Skeptics don't reach it |
| Abstract benefits | Doesn't connect to survival concerns |
| No clear action | Understanding without path forward |

### What Lands

| Approach | Why it works |
|----------|--------------|
| Lead with the number | Undeniable, concrete, memorable |
| Make inaction costly | Loss aversion is powerful |
| Show the path | Reduces effort aversion |
| Speak their language | Signals "this is for you" |

## Applying to Different Contexts

### Documents

- Start page → Full BLUF with layered depth
- Tutorial → Progressive (not BLUF — learning needs sequence)
- How-to → Mini-BLUF per section (goal first, then steps)
- Explanation → Can use BLUF to frame, then explore
- Reference → Structure for scanning, not persuasion

### Conversation

- Start with the answer, then explain
- Check if they want more depth before providing it
- Match their energy — short question, short answer
- Translate to their apparent concerns

### Complex Topics

Even complex topics can lead with the bottom line:

> "The short answer is X. Here's why, and here are the nuances..."

Complexity doesn't excuse burying the point.

## Sources

- U.S. Military. BLUF communication standard.
- Journalism training. Inverted pyramid structure.
- Nielsen Norman Group. [Inverted Pyramid Writing](https://www.nngroup.com/articles/inverted-pyramid/). Eye-tracking validation.
- Cialdini, R. (2006). *Influence: The Psychology of Persuasion*. (Persuasion principles)
- Aristotle. *Rhetoric*. (Logos, pathos, ethos — the original framework)
