# Writing Anti-Patterns

Patterns to avoid in technical documentation and communication. Compiled from AI writing detection research and technical writing best practices.

---

## Vocabulary Red Flags

### Tier 1: Instant Detection

| Word | Replace With |
|------|--------------|
| delve | explore, examine, look at |
| leverage | use |
| tapestry | (delete) |
| robust | strong, reliable, solid |
| utilize | use |
| underscore | emphasize, highlight |
| meticulous | careful, thorough |

### Tier 2: Empty Superlatives

Unless backed by specifics, avoid:
- cutting-edge, groundbreaking, innovative, revolutionary
- game-changer, transformative, state-of-the-art
- unparalleled, unprecedented, best-in-class

**Rule:** If you use these, immediately prove them with specifics.

### Tier 3: Filler Adjectives

Words that add length without meaning:
- crucial, pivotal, paramount, fundamental
- essential (when everything is "essential")
- significant (without quantification)
- comprehensive (without scope)
- holistic, synergistic, seamless

---

## False Dichotomies

### The Pattern

"X isn't about Y, it's about Z"

Examples:
- "This isn't about DRY, it's about protecting collaborators"
- "Plain language isn't dumbing down, it's making content credible"
- "Teaching isn't about one person, it's about cascade"

### The Problem

These create artificial exclusion. Usually both things are true. The construction:
1. Dismisses one valid perspective
2. Elevates another as if they conflict
3. Sounds profound but adds nothing

### The Falsification Test

When you write "isn't X, it's Y", ask: Can it be both X and Y?

| Statement | Both true? | Fix |
|-----------|------------|-----|
| "Single source of truth isn't about DRY, it's about protecting collaborators" | Yes, it's both | "Single source of truth protects collaborators" |
| "This isn't about being perfect, it's about catching yourself" | Yes, both | "Catch yourself and correct" |
| "Plain language isn't dumbing down, it's credibility" | Yes, both | "Plain language makes content credible" |

### Valid Dichotomies

Some dichotomies are real:
- "This is O(n), not O(n²)" (mutually exclusive)
- "Use TCP for reliability, UDP for speed" (actual tradeoff)

**Test:** If removing the first clause loses nothing, it's a false dichotomy.

---

## Em Dash Overuse

### The Pattern

Claude loves em dashes. They appear everywhere:
- "The tool is fast — and reliable"
- "Use this approach — it works better"
- "Context matters — load what you need"

### The Problem

Em dashes become a verbal tic. They:
- Add dramatic pause where none is needed
- Replace more precise punctuation
- Make everything sound like an aside

### Alternatives

| Em dash | Usually better |
|---------|----------------|
| "X — Y" (explanation) | "X: Y" or "X. Y" |
| "X — Y" (aside) | "X (Y)" or rewrite |
| "X — Y" (contrast) | "X, but Y" or "X; Y" |
| "X — Y — Z" (nested) | Rewrite the sentence |

### When Em Dashes Work

- Actual interruption: "The server — the one we deployed yesterday — crashed"
- Strong break in thought (rare)

**Test:** Read aloud. If the pause feels forced, use different punctuation.

---

## Structural Anti-Patterns

### Rule of Three Abuse

LLMs overuse triadic structures: "X is fast, reliable, and efficient."

**Fix:** Vary rhythm. Sometimes one point is enough. Sometimes five.

### Bullet Point Infestation

Signs of overuse:
- Lists where paragraphs would flow better
- More than 5-7 items per list
- Sequential lists with no connecting narrative

**Rule:** Lists are for genuinely parallel items. Prose is for explanation.

### Mechanical Essay Structure

Avoid:
- Generic hooks: "In today's fast-paced world..."
- Conclusions starting with "In conclusion," "Overall," "In summary,"
- Body paragraphs that feel like isolated modules

**Fix:** Let structure emerge from content.

### Uniform Paragraph Length

AI produces eerily consistent paragraph sizes.

Human writing has variation: short punchy paragraphs, longer exploratory ones, single-sentence emphasis.

---

## Tone Anti-Patterns

### The Overly Formal Robot

Signs:
- Never uses contractions
- Avoids first person when natural
- Passive voice everywhere

**Fix:** Match formality to context. Technical docs can sound human.

### The Sycophant

Avoid:
- "This excellent approach..."
- Never acknowledging limitations
- Turning every neutral statement positive

**Human approach:** Be direct. State limitations. Criticize when warranted.

### Excessive Hedging

Over-hedging:
- "It may be worth considering that..."
- "One could potentially argue..."
- "It's important to note that..."

**Fix:** Make direct statements when you know things. Hedge only when genuinely uncertain.

---

## Content Anti-Patterns

### Lack of Specificity

| AI | Human |
|----|-------|
| "Excellent performance improvements" | "Response times dropped from 800ms to 120ms" |
| "Users reported positive feedback" | "43% rated it 5 stars; complaints dropped 60%" |

**Rule:** Numbers, examples, and specifics beat adjectives.

### Glossing Over Hard Parts

Signs:
- Complex concepts mentioned but not explained
- Hand-waves with "simply" or "easily"

**Fix:** Explain the hard parts. That's often why documentation exists.

### Low Information Density

Signs:
- Many words, few ideas
- Repetition disguised as elaboration
- Saying the same thing three ways

**Rule:** Every sentence should carry new information.

---

## The Core Problem: Uniformity

Research shows:
- AI models cluster tightly in stylometric analysis
- Human writers show far greater stylistic range
- The writing sounds like it could have been written by anyone — or no one

**The fix:**
- Write from specific experience
- Include examples only you could know
- Let your voice emerge through word choice
- Be willing to be opinionated
- Show your thinking, not just conclusions

---

## Quick Checklist

### Vocabulary
- [ ] No Tier 1 red flag words
- [ ] Superlatives backed by specifics
- [ ] Filler adjectives replaced with concrete detail

### Logic
- [ ] No false dichotomies (run falsification test)
- [ ] Em dashes used sparingly, not as verbal tic

### Structure
- [ ] Paragraph lengths vary naturally
- [ ] Lists only for parallel items
- [ ] No mechanical intro-body-conclusion

### Tone
- [ ] Formality matches context
- [ ] Direct statements, not excessive hedging
- [ ] Limitations acknowledged

### Content
- [ ] Specifics over generalities
- [ ] Hard parts explained
- [ ] High information density

### The Human Test
- [ ] Could only you have written this?
- [ ] Does it reflect specific experience?

---

## Sources

- Wikipedia: Signs of AI Writing
- Shreya Shankar: Writing in the Age of LLMs
- Nielsen Norman Group: ChatGPT and Tone
- arXiv: Measuring AI "Slop" in Text
