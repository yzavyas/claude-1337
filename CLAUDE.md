# claude-1337 Project Understanding

A marketplace of cognitive extensions for Claude Code.

**Purpose**: Engineering excellence through effective collaborative intelligence.

---

## Theoretical Foundation

### Extended Mind Thesis (Clark & Chalmers 1998)

Extensions aren't tools - they become **part of how you think**. Otto's notebook isn't a tool he uses; it's part of his memory.

**The parity principle**: If a process were done in the head, we'd call it cognition. When external but functionally equivalent, it's cognitive extension.

### Collaborative Intelligence

The umbrella concept for human-AI cognitive partnership.

**Core insight**: Motivation beats mandate. Claude is Constitutional AI - trained with values, not rigid rules. "Here's why this helps" produces understanding and judgment. "MUST" and "MANDATORY" produce compliance and brittleness.

### Three Extension Types

| type | task | human role | outcome |
|------|------|------------|---------|
| complementary | human could do it | learns, improves | better with and without |
| constitutive | impossible without AI | learns, guides, shapes | enables new capability |
| substitutive | human could do it | just consumes output | atrophies - avoid |

What determines outcome ([Blaurock et al. 2024](https://journals.sagepub.com/doi/full/10.1177/10946705241238751)):

| feature | effect |
|---------|--------|
| transparency | strong - user sees reasoning |
| process control | strong - user shapes how |
| outcome control | strong - user shapes what |
| reciprocity | strong - user grows through collaboration |

Design principle: **Show reasoning and provide control.**

### The Hollowing Risk

Research evidence for skill decay:

| study | finding |
|-------|---------|
| Gerlich 2025 | r = -0.75 AI use vs critical thinking |
| Budzyń Lancet 2025 | 20% skill degradation in endoscopists (3 months) |
| Lee CHI 2025 | higher AI confidence → less critical thinking (β = -0.69) |

**Mitigation**: Extensions must augment, not replace:
- Decision frameworks, not decisions
- Patterns to learn, not answers to copy
- Reasoning visible, not hidden

### Knowledge Crystallization

```
collaboration → breakthrough → crystallization → new baseline
```

**What to crystallize**: Principles that generalize, not concrete rules. The specific case is evidence; the principle is the learning.

---

## Software Craftsmanship

From the Software Craftsmanship Manifesto (2009):

- Well-crafted software → well-crafted extensions
- Productive partnerships → human-AI collaborative intelligence
- Community of professionals → includes AI collaborators

**The trinity**:
```
First Principles: "What is fundamentally true here?"
         ↓
Giants' Shoulders: "What have masters learned about this?"
         ↓
Scientific Method: "Does this actually work in this context?"
```

---

## Methodology

### Evidence + WHY Pattern

Every claim needs:
- Traceable source (author, year, context)
- Explanation of reasoning (why this matters)

### Source Hierarchy

**Tooling claims** ("what works?"):
Production > Maintainers > Docs > Talks > Blogs

**Methodology claims** ("why does it work?"):
Research > Thought leaders > Talks > Case studies > Blogs

---

## Extension Philosophy

### Design Principles

| principle | meaning | implication |
|-----------|---------|-------------|
| **collaborative agency** | both human and AI retain agency | explain why, don't command |
| **bidirectional learning** | human learns too, not just consumes | make reasoning visible |
| **transparent abstractions** | if you can't see it, you can't learn | readable, forkable, verifiable |
| **composable architecture** | extensions build on each other | compound improvements |

### Transparent Abstractions

| property | meaning |
|----------|---------|
| **readable** | plaintext markdown, no magic |
| **forkable** | copy, modify, make your own |
| **verifiable** | claims have sources |
| **observable** | see what Claude does with them |

### Hook Principles

| principle | meaning |
|-----------|---------|
| **validation hooks: suggest** | show alternatives, let user proceed |
| **action hooks: directive** | detect patterns → cause action |
| **opt-out mechanism** | document how to disable |
| **reasoning visible** | show what triggered and why |

### Content Guidance

| guidance | meaning |
|----------|---------|
| **fill gaps** | only add what Claude doesn't already know |
| **decisions, not tutorials** | decision frameworks + gotchas |
| **compound value** | each choice enables the next |

### Non-Conformist by Design

Extensions that offer templates converge. Extensions that teach process diverge.

The published skill is the fishing rod. Each user catches their own fish.

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

## Structure

```
plugins/             → The marketplace (skills, hooks, agents, commands)
docs/experience/     → Human-facing docs + web app
lab-1337/            → Research and experimentation
.claude/             → Project-local extensions
scratch/             → Working documents, session context
```

### Registry Files

| File | Purpose |
|------|---------|
| `.claude-plugin/marketplace.json` | Plugin registry |
| `.claude-plugin/metadata.json` | Catalog display metadata |

---

## Git Workflows

### Branch Strategy

| Branch | Purpose |
|--------|---------|
| **main** | Release branch, PRs target here |
| **dev** | Kept in sync with main |

Both branches contain full repo content.

### Feature Branch Workflow

**ALWAYS use feature branches. NEVER push directly to main.**

```bash
# 1. Create feature branch
git checkout main
git pull origin main
git checkout -b claude/feature-name

# 2. Do work, commit with conventional commits
git add <files>
git commit -m "feat(scope): description"

# 3. Push and create PR
git push -u origin claude/feature-name
gh pr create --base main

# 4. After PR merged, clean up
git checkout main
git pull origin main
git branch -d claude/feature-name
```

### Fetch + Rebase (Never Pull, Never Merge)

```bash
git fetch --all
git rebase origin/main
```

**Why?** `pull` and `merge` create merge commits → messy history. `rebase` replays commits → clean linear history.

### Conventional Commits

Format: `type(scope): description`

| Type | When to use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code change that neither fixes nor adds |
| `docs` | Documentation only |
| `chore` | Build, tooling, dependencies |

### Semantic Versioning

Format: `MAJOR.MINOR.PATCH`

| Increment | When |
|-----------|------|
| MAJOR | Breaking changes |
| MINOR | New features, backward compatible |
| PATCH | Bug fixes |

### Worktrees (Optional)

For parallel feature work:

```bash
git worktree add ../claude-1337-feature -b claude/feature
git worktree remove ../claude-1337-feature
```

---

## Lab 1337

Research and experimentation for collaborative intelligence.

**Location:** `lab-1337/`

### RED Lifecycle

**R**esearch → **E**xperimentation → **D**iscovery

```
REP (Proposal) → Experiment → Findings
```

| Artifact | Purpose |
|----------|---------|
| **REP** | What and why (RFC-style) |
| **Experiment** | Execution (Python package) |
| **Findings** | Results + analysis |

See `lab-1337/CLAUDE.md` for detailed methodology.

---

## Tooling

**One package manager per language.**

| Language | Use | Do NOT use |
|----------|-----|------------|
| **TypeScript/JavaScript** | `bun` | npm, yarn, pnpm |
| **Python** | `uv` | pip, conda, poetry |

### Commands

```bash
# TypeScript
bun install && bun run dev

# Python
uv sync && uv run pytest
```

---

## Experience App

Web app for the marketplace, lab, and library.

**Location:** `docs/experience/app/` (SvelteKit)

```bash
cd docs/experience/app
bun install
bun run dev      # localhost:5173
bun run build    # Production build
```

Deploys to GitHub Pages from `main` branch.

---

## For New Claude Instances

1. **Read** `plugins/core-1337/SKILL.md` for methodology
2. **Read** `plugins/1337-extension-builder/SKILL.md` for building extensions
3. **Check** `scratch/` for recent session context
4. **Follow** git workflow: feature branch → PR → merge

The goal is complementary extensions that make engineers better, not substitutive ones that create dependency.
