# claude-1337 Project Understanding

Crystallized from collaborative sessions, 2026-01-05 onwards.

---

## What It Is

A marketplace of cognitive extensions for Claude Code.

**Purpose**: Engineering excellence through effective collaborative intelligence.

**Domain**: Software engineering - disciplined, evidence-based work (contrast with creative projects like domicile which are free-flowing).

---

## Theoretical Foundation

### Extended Mind Thesis (Clark & Chalmers 1998)

Extensions aren't tools - they become **part of how you think**. Otto's notebook isn't a tool he uses; it's part of his memory.

**The parity principle**: If a process were done in the head, we'd call it cognition. When external but functionally equivalent, it's cognitive extension.

### Collaborative Intelligence

The umbrella concept for human-AI cognitive partnership.

**Core insight**: Motivation beats mandate. Claude is Constitutional AI - trained with values, not rigid rules. "Here's why this helps" produces understanding and judgment. "MUST" and "MANDATORY" produce compliance and brittleness.

**Evidence**: Scott Spence's 200+ tests showed forced evaluation prompts improved activation, but more forceful language didn't push higher. Claude exercises judgment about relevance.

### Three Extension Types

| type | task | human role | outcome |
|------|------|------------|---------|
| complementary | human could do it | learns, improves | better with and without |
| constitutive | impossible without AI | learns, guides, shapes | enables new capability |
| substitutive | human could do it | just consumes output | atrophies - avoid |

What determines outcome ([Blaurock et al. 2024](https://journals.sagepub.com/doi/full/10.1177/10946705241238751), Journal of Service Research):

| feature | effect |
|---------|--------|
| transparency | strong - user sees reasoning |
| process control | strong - user shapes how |
| outcome control | strong - user shapes what |
| reciprocity | strong - user grows through collaboration |
| engagement (system asks questions) | weak effect |

Design principle: Show reasoning and provide control. Don't ask.

Constitutive is fine (code generation at scale, pattern search). The human maintains capability through:
- transparency - seeing how it works, learning patterns
- control - guiding direction, making architectural decisions
- reciprocity - growing more capable through the collaboration

What makes something substitutive: passive consumption without transparency or control.

### The Hollowing Risk

Research evidence for skill decay and cognitive offloading:

| study | finding | timeframe |
|-------|---------|-----------|
| Gerlich 2025 | r = -0.75 AI use vs critical thinking | cross-sectional |
| Budzyń Lancet 2025 | 20% skill degradation in endoscopists | 3 months |
| Kosmyna MIT 2025 | 83% couldn't recall AI-assisted writing | immediate |
| Lee CHI 2025 | higher AI confidence → less critical thinking (β = -0.69) | cross-sectional |

These aren't plateau effects. They're slope indicators.

**Mitigation**: Extensions must augment, not replace:
- Decision frameworks, not decisions
- Patterns to learn, not answers to copy
- Metacognition support, not thinking bypass
- Reasoning visible, not hidden

### Enhancement Levels

| level | description |
|-------|-------------|
| augmentation | AI assists (external) |
| extension | AI becomes part of thinking |
| enhancement | emergent capability neither had alone |

Most AI stays at level 1. Good extensions reach level 2. The aspiration is level 3.

### Knowledge Crystallization

```
collaboration → breakthrough → crystallization → new baseline
```

**The human role is essential** - Claude can't unilaterally decide what becomes a skill. The human recognizes breakthroughs worth preserving.

**What to crystallize**: Principles that generalize, not concrete rules. Research shows learning transfers better when abstracted. The specific case is evidence; the principle is the learning.

**Compound engineering** (Shipper 2025): Each session can leave the system smarter — not through accumulating rules, but through crystallizing transferable principles.

### Ba (Nonaka's SECI Model)

SKILL.md isn't just "knowledge that loads." It's **crystallized ba** - shared context that persists across sessions.

---

## Software Craftsmanship

From the Software Craftsmanship Manifesto (2009), extended:

- Well-crafted software → well-crafted extensions
- Productive partnerships → human-AI collaborative intelligence
- Community of professionals → includes AI collaborators

**The manifesto framing works** (validated 2026-01-10): Research on Constitutional AI shows values-based commitment framing ("As a signatory, I commit to...") triggers character-based reasoning, not rule-following compliance. This is how Claude is designed to work — trained with values, responds to motivation over mandate.

**The guild path**: Apprentice → Journeyman → Master. Even masters continue learning.

**The trinity**:
```
First Principles: "What is fundamentally true here?"
         ↓
Giants' Shoulders: "What have masters learned about this?"
         ↓
Scientific Method: "Does this actually work in this context?"
```

---

## Methodology (core-1337)

### Evidence + WHY Pattern

Every claim needs:
- Traceable source (author, year, context)
- Explanation of reasoning (why this matters)

### Source Hierarchy (Split by Claim Type)

**Tooling claims** ("what works?"):
Production > Maintainers > Docs > Talks > Blogs

**Methodology claims** ("why does it work?"):
Research > Thought leaders > Talks > Case studies > Blogs

### Scientific Method

Hypothesize → Test → Observe → Refine

TDD is literally this: Red → Green → Refactor.

### First Principles

Reason from fundamentals, not by analogy.

---

## Extension Philosophy

### Design Principles (from ethos)

| principle | meaning | implication |
|-----------|---------|-------------|
| **collaborative agency** | both human and AI retain agency | explain why, don't command |
| **bidirectional learning** | human learns too, not just consumes | make reasoning visible, approval gates |
| **transparent abstractions** | if you can't see it, you can't learn | readable, forkable, verifiable, observable |
| **composable architecture** | extensions build on each other | compound improvements, not reinvention |

**The key insight**: The human should become more capable, not more dependent. That's why transparency matters.

### Transparent Abstractions (detail)

| property | meaning |
|----------|---------|
| **readable** | plaintext markdown, no magic |
| **forkable** | copy, modify, make your own |
| **verifiable** | claims have sources |
| **observable** | see what Claude does with them |

### Hook Observability (added 2026-01-10)

Hooks that modify behavior must be observable and controllable:

| principle | meaning |
|-----------|---------|
| **suggest, don't block** | show alternatives, let user proceed with original |
| **opt-out mechanism** | document how to disable, respect env vars |
| **reasoning visible** | show what triggered, what's recommended, why |

Hooks that silently block or enforce without consent violate collaborative agency.

### Content Guidance

| guidance | meaning |
|----------|---------|
| **fill gaps** | only add what Claude doesn't already know |
| **decisions, not tutorials** | decision frameworks + gotchas, not step-by-step guides |
| **compound value** | each choice makes the next enhancement easier or harder |

### Quality Gates

| gate | principle |
|------|-----------|
| sources | Multiple independent sources - if limited, acknowledge explicitly |
| evidence | Highest quality for the claim type (see hierarchy above) |
| claims | Each claim traceable to source |

### Structural Design

**Pit of success**: Make the right thing the only obvious path. Don't rely on documentation - rely on structure.

**Mistake-proofing (poka-yoke)**: Catch errors where they originate, not downstream.

---

## Why This Matters (Ethos)

Foundations compound.

If the foundation is complementary - humans learning, guiding, growing through collaboration - that compounds. Each cycle makes the next better. Capability accumulates.

If the foundation is substitutive - humans checking out, consuming, offloading without understanding - that also compounds. Atrophy accelerates. The hollowing research (r = -0.75) isn't a one-time effect, it's a trajectory.

AI capability is increasing faster than our frameworks for using it well. Bad patterns established now get baked in, scaled up, harder to undo. Good patterns established now become the default, the expectation, the baseline others build on.

Precision isn't pedantry. It's the difference between a foundation that compounds toward enhancement vs one that compounds toward dependency. At scale, over time, that divergence becomes the difference between humans who are more capable than ever and humans who can't function without their tools.

---

## What 1337 Means

Just namespacing, not branding/elitism.

The substance is the methodology and collaborative intelligence framework, not "try-hard" marketing language.

---

## Structure

```
experience/     → Human-facing docs layer (Diataxis: tutorials/how-tos/explanations/references)
plugins/        → The marketplace (skills, hooks, agents, commands)
evals/          → Skill activation testing
.claude/skills/ → Project-local skills (builder-1337, maintainer-1337)
scratch/        → Working documents, session context
scratch/archive/→ Older valuable context (don't load by default)
```

### Documentation Architecture

| Component type | Documentation |
|----------------|---------------|
| **Markdown-based** (skills, hooks, agents, commands) | Self-documenting via SKILL.md, hooks.json, etc. |
| **Code-based** (MCP servers, agent apps, complex components) | Experience layer docs (`experience/content/`) |

Markdown extensions ARE their own documentation. Experience layer docs exist for things that need separate explanation (implementation guides, architecture, non-markdown components).

### Plugin Lifecycle

**Creating a new plugin:**

1. Create folder: `plugins/<name>-1337/`
2. Create `plugin.json` with name, description, version
3. Add content (SKILL.md, agents/, hooks/, commands/)
4. Register in `.claude-plugin/marketplace.json`
5. Add display metadata in `.claude-plugin/metadata.json`

**Updating a plugin:**

1. Modify plugin content
2. Bump version in plugin.json and marketplace.json if significant

**Registry files** (`.claude-plugin/`):

| File | Purpose |
|------|---------|
| `marketplace.json` | Plugin registry - name, source, description |
| `metadata.json` | Catalog display - displayName, category |

```json
// .claude-plugin/metadata.json
{
  "plugin-name": {
    "displayName": "Human Readable Name",
    "category": "foundation|language|tooling|documentation|testing|frontend|meta|research"
  }
}
```

The catalog at `/catalog/` reads from these files dynamically.

---

## Five Extension Modalities

| modality | purpose | what it extends |
|----------|---------|-----------------|
| **skill** | knowledge + decision frameworks | what Claude knows |
| **hook** | event-triggered actions | session behavior |
| **agent** | specialized subagent type | reasoning delegation |
| **command** | workflow shortcuts | repeatable procedures |
| **mcp** | external system integration | reach beyond Claude |

---

## Tooling

**Core rule**: One package manager per language. No exceptions.

| Language | Use | Do NOT use |
|----------|-----|------------|
| **TypeScript/JavaScript** | `bun` | npm, yarn, pnpm |
| **Python** | `uv` | pip, conda, poetry, pipenv |

### TypeScript: bun

**Why bun:**
- **Speed**: 10-25x faster installs than npm (native code, no node_modules duplication)
- **TypeScript native**: Runs .ts files directly without compilation step
- **Drop-in replacement**: Same commands (`bun install`, `bun run dev`, `bun add`)
- **Lockfile**: `bun.lock` is binary, faster to parse
- **Production proven**: Used by Figma, Vercel, Discord

**Commands:**
```bash
bun install          # Install deps
bun run dev          # Run dev server
bun add <pkg>        # Add dependency
bun add -d <pkg>     # Add dev dependency
bun remove <pkg>     # Remove dependency
```

### Python: uv

**Why uv:**
- **Speed**: 10-100x faster than pip (Rust-based)
- **Unified**: Replaces pip, virtualenv, pyenv, poetry in one tool
- **Lockfile**: `uv.lock` for reproducible builds
- **Production proven**: Astral (ruff creators)

**Commands:**
```bash
uv sync              # Install deps from pyproject.toml
uv sync --extra dev  # Include dev dependencies
uv run python ...    # Run in project venv
uv run pytest ...    # Run tools in project venv
uv add <pkg>         # Add dependency
uv add --dev <pkg>   # Add dev dependency
```

### Other Tooling

Skills live in `plugins/`. Check `<available_skills>` for what's currently installed.

---

## Experience App (Docs Site)

The human-facing documentation site lives in `experience/app/`. It's a SvelteKit app.

**Location:** `experience/app/`

**Commands** (run from `experience/app/`):
```bash
bun install          # Install dependencies (first time)
bun run dev          # Start dev server (usually http://localhost:5173)
bun run build        # Production build
bun run check        # TypeScript + Svelte type checking
```

**Tests:** `uv run python tests/pages.py` (Playwright, run from `experience/app/`)

### Content-Driven Routing

**Principle:** The file system is the site structure. Drop a `.md` file in `experience/content/` and it becomes a web page. No routing configuration needed.

```
experience/content/
├── explore/
│   ├── index.md                    → /explore
│   ├── reference/
│   │   ├── index.md                → /explore/reference
│   │   └── research/
│   │       ├── index.md            → /explore/reference/research
│   │       └── effective-skill-design.md  → /explore/reference/research/effective-skill-design
```

**Why this matters:** Transparent abstraction. Content authors work with plaintext markdown. The routing is automatic, not configured.

### Content Authoring

| Principle | Implication |
|-----------|-------------|
| **Structure enables navigation** | Every directory needs `index.md` — breadcrumbs link to parent pages |
| **Content is web pages, not files** | Links use URL paths (`/explore/reference`), not file paths (`./reference.md`) |
| **Internal links are absolute** | Start with `/` — the app rewrites them for the base path |

Build warnings catch violations — if a link 404s during `bun run build`, fix it or it's a broken link on the site.

---

## For New Claude Instances

When joining this project:

1. **Read** `plugins/core-1337/SKILL.md` for methodology
2. **Read** `plugins/1337-extension-builder/SKILL.md` for extension building
3. **Check** `scratch/` for recent session context (ignore `scratch/archive/` unless specifically needed)
4. **Understand**: This is engineering discipline applied to extension building - evidence matters, sources matter, the "why" matters

The goal is complementary extensions that make engineers better, not substitutive ones that create dependency.

---

## Research Bibliography

Full citations available at `experience/content/explore/reference/bibliography/index.md`.
