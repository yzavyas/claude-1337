---
name: gsd-methodology
description: "Get Shit Done: Context engineering methodology for Claude Code. PROJECT→ROADMAP→STATE→PLAN workflow with subagent isolation to prevent context degradation."
---

# Get Shit Done (GSD) Methodology

Meta-prompting and context engineering for reliable AI-assisted development.

**Source**: [glittercowboy/get-shit-done](https://github.com/glittercowboy/get-shit-done)

## Core Problem Solved

> "Vibecoding falls apart at scale. Quality degrades as context fills."

GSD solves context rot through:
- Structured file-based specifications
- Fresh subagent contexts per task
- Atomic, verifiable work items

## The File System

| File | Purpose | When Updated |
|------|---------|--------------|
| `PROJECT.md` | Vision, goals, constraints, stack | Project start, major pivots |
| `ROADMAP.md` | Phases from start to finish | After milestone completion |
| `STATE.md` | Decisions, blockers, current position | Every session |
| `PLAN.md` | Current atomic tasks (XML format) | Each phase |
| `SUMMARY.md` | What happened, what changed | After each task |

## The Workflow

### Phase 1: Project Definition

Capture comprehensive project specification through iterative questioning.

**Gather:**
- Project vision and goals
- Technical constraints
- Stack preferences
- Edge cases and requirements
- Success criteria

**Output:** `PROJECT.md` — the north star document.

### Phase 2: Codebase Analysis (Brownfield Only)

For existing codebases, analyze before planning.

**Document:**
- Stack (languages, frameworks, dependencies)
- Architecture (patterns, layers, data flow)
- Structure (directory layout)
- Conventions (code style, naming)
- Testing (frameworks, patterns)
- Integrations (external services)
- Concerns (tech debt, fragile areas)

### Phase 3: Roadmap Creation

Break the project into sequential phases with clear milestones.

**Each phase should:**
- Have a clear deliverable
- Be completable in 1-3 sessions
- Build on previous phases
- Have verifiable done criteria

**Output:** `ROADMAP.md` with phases, `STATE.md` initialized.

### Phase 4: Phase Planning

Create 2-3 atomic tasks per phase using XML format.

```xml
<task type="auto">
  <name>Human-readable task description</name>
  <files>All file paths this task touches</files>
  <action>
    Precise implementation instructions.
    Include: library choices, error handling approach,
    specific patterns to use.
  </action>
  <verify>Exact command to validate (e.g., curl, test runner)</verify>
  <done>Specific success criteria</done>
</task>
```

**Key principles:**
- Tasks are atomic (one concern each)
- Each task independently verifiable
- Explicit about libraries and patterns (no ambiguity)
- Test command included

**Output:** `PLAN.md` with XML tasks.

### Phase 5: Execution

Execute tasks with fresh context isolation.

**For parallel execution:**
- Each task runs in independent subagent
- Fresh 200k token context per task
- No cross-contamination between tasks

**For sequential execution:**
- Run one task at a time
- Manual checkpoint between tasks
- Update `STATE.md` after each

### Phase 6: Verification

After execution, verify work meets criteria.

**For each task:**
1. Run the verify command from the task
2. Check done criteria met
3. If issues: create targeted fix plan

**Output:** Update `STATE.md` with results, `SUMMARY.md` with what changed.

## XML Task Format Deep Dive

The XML format is intentionally structured:

```xml
<task type="auto">
  <name>Add JWT authentication to /api/login</name>
  <files>
    src/routes/auth.ts
    src/middleware/jwt.ts
    src/types/user.ts
  </files>
  <action>
    Use jose library for JWT (not jsonwebtoken - CommonJS issues).
    Create middleware that:
    1. Extracts token from Authorization header
    2. Validates signature against JWT_SECRET env var
    3. Attaches decoded payload to request.user
    4. Returns 401 with {error: "unauthorized"} on failure

    For /api/login:
    1. Validate email/password against users table
    2. Generate JWT with 24h expiry
    3. Return httpOnly cookie + {success: true}
  </action>
  <verify>
    curl -X POST localhost:3000/api/login \
      -H "Content-Type: application/json" \
      -d '{"email":"test@test.com","password":"test123"}' \
      -c cookies.txt && \
    curl localhost:3000/api/protected -b cookies.txt
  </verify>
  <done>
    - Login returns 200 with httpOnly cookie
    - Protected route accessible with cookie
    - Protected route returns 401 without cookie
  </done>
</task>
```

**Why this works:**
- `files`: Scopes the task, prevents scope creep
- `action`: No ambiguity about implementation choices
- `verify`: Automated validation, not "it looks right"
- `done`: Multiple criteria, all must pass

## Context Engineering Principles

**File sizing**: Each file sized to stay under quality degradation threshold.

**Subagent isolation**: Tasks execute in fresh contexts—accumulated garbage doesn't affect new tasks.

**Atomic commits**: Each task = one commit with clear description.

**Modularity**: Plans remain independent; phases insertable/removable.

## State Management

`STATE.md` persists across sessions:

```markdown
# State

## Current Position
Phase: 3
Task: 2 of 3
Status: in_progress

## Decisions Made
- Using jose over jsonwebtoken (CommonJS compatibility)
- PostgreSQL for user storage (existing infrastructure)

## Blockers
- None currently

## Notes
- User requested httpOnly cookies over localStorage
```

## Application to This Task

When given a development task:

1. **Create PROJECT.md** — Capture requirements, constraints, success criteria
2. **Create ROADMAP.md** — Break into phases
3. **Create PLAN.md** — XML tasks for current phase
4. **Execute with isolation** — Fresh context per task
5. **Verify explicitly** — Run the verify commands
6. **Update STATE.md** — Track progress and decisions

The overhead pays off in:
- Consistent quality regardless of project size
- Clear handoff points between sessions
- Verifiable progress (not "I think it works")
- Decisions documented for future reference
