# Diataxis Framework

A systematic approach to technical documentation by Daniele Procida.

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

## Sources

- [Diataxis.fr](https://diataxis.fr) - Daniele Procida's framework
- [Django Documentation](https://docs.djangoproject.com) - Exemplar implementation
