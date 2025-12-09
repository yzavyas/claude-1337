# Skill Creation Process

End-to-end workflow for creating elite skills.

## Phase 1: Gap Analysis

**Goal**: Find what Claude doesn't know (or gets wrong).

```
1. Pick domain
   ├── What am I expert at?
   └── Where does Claude give generic/outdated advice?

2. Test Claude's knowledge
   ├── Ask: "What's the best X for Y?"
   ├── Is the answer current? Evidence-based?
   └── Does it match production reality?

3. Document gaps
   ├── Wrong defaults
   ├── Missing gotchas
   ├── Outdated recommendations
   └── No decision framework
```

## Phase 2: Research

**Goal**: Evidence-based best practices, not opinion.

### Source Hierarchy

| Priority | Source | Why |
|----------|--------|-----|
| 1 | Production codebases | What actually ships |
| 2 | Core maintainers | Primary knowledge |
| 3 | Conference talks | War stories |
| 4 | GitHub stars with usage | Social proof + adoption |
| 5 | Blog posts | Secondary, verify |

### Research Questions

- What do elite teams actually use?
- What footguns appear in production?
- What's the 95% case vs edge cases?
- What changed recently? (deprecations, new winners)
- What compiles but fails at scale?

### Evidence Capture

```markdown
## [Topic]

**Claim**: [What you learned]
**Source**: [URL/reference]
**Evidence**: [Quote or example]
**Applies to**: [SKILL.md or reference?]
```

## Phase 3: Structure

**Goal**: Organize for progressive disclosure.

### SKILL.md Core (~100-200 lines)

```markdown
---
name: domain-1337
description: "What + Use when: triggers"
---

# Title

One sentence purpose.

## Decision Framework
[Tables for common choices]

## Production Gotchas
[Non-obvious traps]

## Domain Routing
[Link to references/]
```

### Reference Files (~100-150 lines each)

| File Type | Contains |
|-----------|----------|
| Subdomain | Deep patterns for specific use case |
| Ecosystem | Crate/tool comparisons with evidence |
| Recipes | Multi-step patterns, config snippets |

### File Naming

```
skill-name/
├── SKILL.md              # Always loaded when triggered
└── references/
    ├── subdomain-a.md    # Loaded on: "X detection"
    ├── subdomain-b.md    # Loaded on: "Y detection"
    └── ecosystem.md      # Loaded on: "crate/tool questions"
```

## Phase 4: Write

**Goal**: Apply content triage to every line.

See [content-triage.md](content-triage.md) for the full filter.

### Writing Rules

1. **Tables over prose** - Scannable decisions
2. **Code shows, prose tells** - Minimal explanation
3. **Bold the winner** - Clear recommendations
4. **Cite evidence** - Production usage > stars
5. **Version things** - What might change

### Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| "There are many options..." | Pick THE answer |
| "You could use X or Y" | "Use X. Y is deprecated." |
| Teaching basics | Assume Claude knows syntax |
| Complete tutorials | Decision points only |
| Marketing language | Evidence-based claims |

## Phase 5: Validate

**Goal**: Ensure skill triggers and loads correctly.

### Pre-Commit Checklist

```
[ ] Description < 600 chars, has "Use when:" triggers
[ ] No YAML multiline (>-, |) - use quoted strings
[ ] SKILL.md < 500 lines (target 100-200)
[ ] References < 250 lines each (target 100-150)
[ ] All linked files exist
[ ] Evidence cited for recommendations
[ ] No catalogs - winners picked
```

### Trigger Testing

1. Start fresh Claude session
2. Ask related question (don't mention skill name)
3. Check: Does skill appear in response?
4. Check: Is full content loading, or truncated?

### Size Verification

```bash
# Check line counts
wc -l SKILL.md references/*.md

# Check char count for description
grep "description:" SKILL.md | wc -c
```

## Maintenance

**Goal**: Keep skill current.

### Update Triggers

| Signal | Action |
|--------|--------|
| Major version release | Review breaking changes |
| Deprecation notice | Find replacement |
| New crate gains traction | Validate production use, consider |
| Bug reports on advice | Fix with evidence |

### Update Process

1. Research the change
2. Verify evidence (production > hype)
3. Update affected files only
4. Test trigger still works
5. Commit with evidence in message
