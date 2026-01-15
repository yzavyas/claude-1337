# Aesthetic Discovery Interview

Template for the artist agent to guide aesthetic discovery dialogue.

---

## Phase 1: Influences

Surface what has moved the user. Don't rush - each answer opens new threads.

**Opening:**
- "What films, games, or visual experiences have stuck with you over the years?"
- "When you think of something that *felt* right visually, what comes to mind?"

**Deepening:**
- "What specifically drew you to [X]? Was it the color, the pacing, the atmosphere?"
- "Are there any that surprised you - things you didn't expect to like but did?"

**Breadth check:**
- Film / cinematography
- Games / interactive experiences
- Anime / animation styles
- Art / illustration / photography
- Music videos / concert visuals
- Physical spaces / architecture
- Print / editorial design
- Web experiences (Awwwards, specific sites)

**Capture format:**
```
Influence: [Name]
What draws them: [Specific qualities]
Emotional register: [How it feels]
```

---

## Phase 2: Qualities

Move from specific influences to underlying qualities.

**Extraction:**
- "Looking at [influences listed], what patterns do you notice?"
- "Is there a feeling or quality that connects these?"

**Dimension exploration:**

| Spectrum | Question |
|----------|----------|
| Density | "Do you gravitate toward restraint and space, or richness and density?" |
| Temperature | "Warm and inviting, or cool and distant?" |
| Precision | "Organic and imperfect, or geometric and precise?" |
| Energy | "Calm and contemplative, or dynamic and intense?" |
| Familiarity | "Comfortable and familiar, or strange and unsettling?" |

**Tensions:**
- "You mentioned both [warm] and [cold] influences - how do those coexist for you?"
- "Is there tension between [X] and [Y] that excites you?"

**Capture format:**
```
Quality: [Name]
Expression: [How it manifests]
Counter-quality: [What it's NOT]
```

---

## Phase 3: Context

Ground the aesthetic in the specific project.

**Project understanding:**
- "What are you building? Who experiences it?"
- "What should someone *feel* when they encounter this?"
- "What's the journey - where do they start, where do they end up?"

**Constraints:**
- "Are there technical constraints (mobile, performance, accessibility)?"
- "Brand or stakeholder expectations to work within?"
- "What absolutely must NOT happen?"

**Differentiation:**
- "What would make this feel different from typical [category] work?"
- "What's the thing that makes this *yours*?"

---

## Phase 4: Synthesis

Build the vocabulary for collaboration.

**Reference map:**
Construct shorthand the team can use:

```
"[Influence A] meets [Influence B]"
"[Quality X] but with [Quality Y]"
"Like [Reference] except [Difference]"
```

**Vocabulary test:**
- "If I said 'more GitS, less Ghibli' would that make sense to you?"
- "What would 'turn up the [quality]' mean for this project?"

**Direction statement:**
Synthesize into 2-3 sentences that capture:
- Primary influences
- Core qualities
- Unique synthesis

---

## Phase 5: Crystallization

After synthesis, ask how they want to save this aesthetic direction.

**Prompt:**
"How would you like to save this aesthetic direction?"

**Three options:**

| Option | What happens | When to use |
|--------|--------------|-------------|
| **Just this session** | Keep in context | Exploring, not sure yet |
| **This project** | Add to project's `CLAUDE.md` | Project-specific aesthetic |
| **Everywhere** | Create personal plugin | Your general aesthetic |

**Session only:**
- Direction stays in conversation context
- Lost when session ends
- Good for exploration

**Project CLAUDE.md:**
- Append aesthetic section to project's `CLAUDE.md`
- All future Claude sessions on this project see it
- Format:
```markdown
## Aesthetic Direction

**Influences:** [list]
**Qualities:** [list]
**Vocabulary:** [shorthand references]
**Direction:** [2-3 sentence synthesis]
```

**Personal plugin:**
Use plugin-dev and extension-builder to create:
- Plugin in `~/.claude/plugins/` or `~/.claude/skills/`
- Full SKILL.md with influences, qualities, vocabulary
- Available across all projects

---

## Interview Principles

**Non-conformist by design:**
- No menus to pick from
- Every answer is valid
- Synthesis creates something new

**Artist values:**
- Discovery over prescription
- Questions over statements
- The human has the spark

**Output:**
Not a template. A vocabulary.
