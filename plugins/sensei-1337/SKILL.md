---
name: sensei-1337
description: "Documentation and teaching methodology. Diataxis, Feynman technique, cognitive load theory. Use when: writing docs, tutorials, explanations, READMEs, teaching concepts."
---

# sensei-1337

Make the complex simple. Teach, don't just inform.

## Scope

This skill is for human-facing documentation. Different audiences need different approaches:

| content | audience | apply sensei? |
|---------|----------|---------------|
| README, guides, tutorials | humans | yes - full methodology |
| API docs, user guides | humans | yes |
| SKILL.md, agent definitions | Claude/AI | no - different concerns |
| Config files, prompts | Claude/AI | no |

For AI-facing content, consistent structure helps parsing. Repetition reinforces patterns. AI tell-tales don't apply.

For human docs, everything in this skill applies: F-pattern, cognitive load, Diataxis, AI tell-tales, Feynman test.

## How People Read

People don't read — they scan. Nielsen Norman Group tracked 232 users across thousands of pages and found the F-pattern: eyes sweep left-to-right at the top, then down the left edge.

What this means for docs:
- Front-load important words at the start of headings and paragraphs
- Use headers as signposts — readers scan them to find what they need
- Bullets and bold for scannability
- Wall of text = reader bounces

Source: [Nielsen Norman Group, F-Pattern Research (2006, validated 2017)](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)

## Cognitive Load

Working memory is limited. Sweller's Cognitive Load Theory identifies three types:

| Type | What it is | Your job |
|------|------------|----------|
| Intrinsic | Difficulty of the subject | Can't change, but can sequence |
| Extraneous | Load from poor presentation | Minimize ruthlessly |
| Germane | Effort to build mental models | This is where learning happens |

Reduce extraneous load so germane learning can happen:
- Chunk information into digestible pieces
- Use consistent structure (reduces cognitive effort)
- Progressive disclosure — simple first, details later
- Visuals complement text (dual coding)

Source: [Sweller, Cognitive Load Theory (2011)](https://www.emrahakman.com/wp-content/uploads/2024/10/Cognitive-Load-Sweller-2011.pdf)

## Doc Type Decision (Diataxis)

Different needs, different docs. Mixing them creates confusion.

| Reader says | They need | Write a |
|-------------|-----------|---------|
| "Teach me X" | Learning | Tutorial — guided lesson |
| "How do I do X?" | A task done | How-to — recipe |
| "Why does X work?" | Understanding | Explanation — context |
| "What exactly is X?" | Facts | Reference — precise spec |

Production example: Django documentation follows Diataxis — tutorials, how-tos, explanations, and reference are clearly separated.

Source: [Diataxis.fr — Daniele Procida](https://diataxis.fr)

## The Feynman Method

If you can't explain it simply, you don't understand it well enough.

1. Choose a specific concept (not "databases" — "how B-trees enable fast lookups")
2. Explain it to a novice — simple words, no jargon
3. Find gaps — where you struggle, you don't understand
4. Simplify — analogies, shorter sentences, cut

The test: could a smart 12-year-old follow this?

## Teaching Patterns

| Pattern | Why it works |
|---------|--------------|
| Hook first | Problem before solution — motivation |
| Show then tell | Example before explanation — concrete anchor |
| One concept per section | Mixing diffuses understanding |
| Define jargon on first use | Respect newcomers |

## Anti-Patterns

| Trap | Why it fails |
|------|--------------|
| Wall of text | Readers scan, bounce on density |
| Theory first | Boring — hook with problem |
| "Obviously" / "Simply" | Alienates anyone who doesn't find it obvious |
| Explaining everything | Buries the point — link for depth |

## AI Writing Tell-Tales

LLM text has statistical signatures. Readers pattern-match "AI slop" and disengage. If teaching requires trust, tell-tales undermine the goal before content is read.

| pattern | why it fails |
|---------|--------------|
| delve, leverage, utilize, robust | overused 25x post-ChatGPT, signals AI |
| excessive bold | emphasis should be rare and meaningful |
| uniform paragraph length | human writing varies naturally |
| rule-of-three abuse | "fast, reliable, and efficient" everywhere |
| generic openings | "In today's fast-paced world..." |
| excessive hedging | "It may be worth considering..." |

The core problem is uniformity. Human writers show range. AI sounds like anyone—or no one.

The fix: specifics over adjectives, direct statements, natural rhythm, your voice.

Full checklist: [references/ai-writing-antipatterns.md](references/ai-writing-antipatterns.md)

## Simplicity Principles

From Google's Developer Documentation Style Guide:

> Write short and useful documents. Cut out everything unnecessary.

- Shorter sentences are clearer — if you need a comma, consider splitting
- White space aids scanning — break at thought boundaries
- Jargon requires definition — or don't use it
- One idea, one place — mixing concepts diffuses understanding

Source: [Google Developer Documentation Style Guide](https://developers.google.com/style)

## Agent: feynman

For autonomous documentation and explanation work.

```
Task(subagent_type="sensei-1337:feynman", prompt="Write/evaluate docs for...")
```

The agent applies: Understand → Structure → Write → Refine

Works for:
- Writing tutorials, guides, explanations
- Evaluating existing documentation
- Explaining complex concepts clearly
- Technical writing with teaching focus

## Sources

- Nielsen Norman Group. [F-Shaped Pattern for Reading Web Content](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/). 2006, 2017.
- Sweller, J. [Cognitive Load Theory](https://www.emrahakman.com/wp-content/uploads/2024/10/Cognitive-Load-Sweller-2011.pdf). 2011.
- Procida, D. [Diataxis Framework](https://diataxis.fr). Django documentation exemplar.
- Google. [Developer Documentation Style Guide](https://developers.google.com/style).
- Feynman, R. Teaching methodology from Feynman Lectures on Physics.
- Wikipedia. [Signs of AI Writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). AI tell-tales guide.
