# Diataxis Framework

A systematic approach to technical documentation by Daniele Procida. Adopted by Gatsby, Cloudflare, Django, and many open-source projects.

## Why This Matters

Documentation fails when it mixes purposes. A tutorial that stops to explain theory loses momentum. A reference that guides step-by-step wastes expert time.

Diataxis separates content by **user intent**:
- **Action-oriented** (doing): Tutorials, How-tos
- **Knowledge-oriented** (understanding): Explanations, Reference

Each type serves a different cognitive mode. Mixing them creates cognitive dissonance.

## The Four Types

Documentation serves four distinct needs. Mixing them creates confusion.

### Tutorial (Learning-oriented)

**User mindset**: "I'm new, teach me"

| Attribute | Value |
|-----------|-------|
| Purpose | Learning through doing |
| Form | Lesson with guided steps |
| Outcome | User acquires skill |
| Analogy | Cooking class |

**Structure**:
1. Set clear learning goal
2. Provide working starting point
3. Guide through minimum steps to success
4. Let them complete something real

**Pitfall**: Don't explain everything - keep momentum.

### How-to (Task-oriented)

**User mindset**: "I need to do X"

| Attribute | Value |
|-----------|-------|
| Purpose | Solve specific problem |
| Form | Recipe - steps to follow |
| Outcome | Task completed |
| Analogy | Recipe in cookbook |

**Structure**:
1. Name the goal clearly
2. List prerequisites
3. Numbered steps to completion
4. Verification step

**Pitfall**: Don't teach - assume competence, give the recipe.

### Explanation (Understanding-oriented)

**User mindset**: "Why? How does this work?"

| Attribute | Value |
|-----------|-------|
| Purpose | Deepen understanding |
| Form | Discursive discussion |
| Outcome | User understands context |
| Analogy | History article |

**Structure**:
1. Frame the question
2. Provide context and background
3. Discuss tradeoffs, alternatives, reasons
4. Connect to bigger picture

**Pitfall**: Don't provide instructions - this is about understanding.

### Reference (Information-oriented)

**User mindset**: "What exactly is X?"

| Attribute | Value |
|-----------|-------|
| Purpose | Provide accurate information |
| Form | Dry, factual description |
| Outcome | User finds specific info |
| Analogy | Encyclopedia entry |

**Structure**:
1. Consistent structure across entries
2. Complete coverage
3. No narrative or opinion
4. Easy to scan

**Pitfall**: Don't explain or guide - just describe accurately.

## Decision Matrix

| Question to ask | Answer | Write a... |
|-----------------|--------|------------|
| Is user learning? | Yes | Tutorial |
| Is user doing a task? | Yes | How-to |
| Is user trying to understand? | Yes | Explanation |
| Is user looking up facts? | Yes | Reference |

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Tutorial with too much explanation | Loses momentum | Save "why" for explanation docs |
| How-to that teaches | Condescending to experts | Assume competence |
| Reference with narrative | Hard to scan | Strip to facts |
| Explanation with steps | Confuses purpose | Separate into how-to |

## Affordances: When to Use Each

| User says... | They want... | Write a... | Key affordance |
|--------------|--------------|------------|----------------|
| "Teach me X" | To acquire a skill | Tutorial | Guided success builds confidence |
| "How do I do X?" | To complete a task | How-to | Answers the question directly |
| "Why does X work?" | To understand context | Explanation | Connects to bigger picture |
| "What exactly is X?" | To look up a fact | Reference | Fast, accurate, scannable |

## Connection to Expertise Reversal

Diataxis implicitly handles the expertise reversal effect:

| Doc type | Audience expertise | Scaffolding level |
|----------|-------------------|-------------------|
| Tutorial | Novice | High (guided, sequential) |
| How-to | Competent | Medium (assumes basics) |
| Reference | Expert | Low (direct access) |
| Explanation | Any | Adaptive (reader controls depth) |

This is why mixing types fails: a tutorial written for novices will frustrate experts; a reference written for experts will lose novices.

## Sources

- [Diataxis.fr](https://diataxis.fr) — Daniele Procida's framework
- [Django Documentation](https://docs.djangoproject.com) — Exemplar implementation
- Kalyuga, S., et al. (2003). The expertise reversal effect. *Educational Psychologist*. — Why expertise level matters
