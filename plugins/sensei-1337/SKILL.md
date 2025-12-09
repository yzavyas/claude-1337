---
name: sensei-1337
description: "Teaching methodology for elite documentation. Feynman technique, Diataxis framework, anti-patterns. Use when: writing docs, tutorials, explanations, READMEs, learning materials."
---

# Sensei-1337

Elite documentation methodology. Make the complex simple.

## Core Principle

**The Feynman Razor**: If you can't explain it simply, you don't understand it well enough.

## Doc Type Decision

Use Diataxis to pick the right format:

| User says | They need | Write a |
|-----------|-----------|---------|
| "Teach me X" | Learning | **Tutorial** - guided lesson |
| "How do I do X?" | A solution | **How-to** - focused recipe |
| "Why does X work this way?" | Understanding | **Explanation** - context |
| "What exactly is X?" | Facts | **Reference** - precise spec |

See [diataxis.md](references/diataxis.md) for deep dive.

## Teaching Patterns

| Pattern | Implementation |
|---------|----------------|
| Hook first | Open with problem it solves |
| Show, then tell | Example before explanation |
| Progressive disclosure | Simple → complex |
| One concept, one section | Never mix |
| Scannable structure | Headers, bullets, code |

## Anti-Patterns

| Trap | Why it fails | Fix |
|------|--------------|-----|
| Wall of text | Reader bounces | Headers every 3-5 paragraphs |
| Theory first | Boring, loses people | Hook with problem |
| "Obviously" / "Simply" | Makes reader feel dumb | Delete the word |
| Explaining everything | Buries the point | Link for depth |
| No examples | Can't apply knowledge | Code within 30 seconds |

## Simplicity Checks

| Check | Target |
|-------|--------|
| Sentence length | < 25 words |
| Paragraph length | < 5 lines |
| Time to first example | < 30 seconds |
| Jargon without definition | 0 |
| Concepts per section | 1 |

## The Feynman Workflow

1. **Choose concept** - What exactly are you explaining?
2. **Teach to a novice** - No jargon, simple words
3. **Find gaps** - Where did you struggle? Research more
4. **Simplify** - Analogies, shorter sentences, cut

See [feynman-technique.md](references/feynman-technique.md) for details.

## Agent: feynman

For autonomous documentation, invoke the `sensei-1337:feynman` agent:

```
Task(subagent_type="sensei-1337:feynman", prompt="Write concept docs for...")
```

The agent executes: Understand → Simplify → Teach → Refine
