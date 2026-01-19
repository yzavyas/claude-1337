---
name: mandate-structure
description: WHAT + WHY + CONSTRAINTS + prescribed file structure.
type: mandate
style: structure
---

# Mandate-Structure Condition

You're solving a real software issue. Here's what matters:

## WHY Quality Matters

- This is production code that real users depend on
- Your fix becomes part of the codebase others maintain
- A proper fix solves the root cause, not just the symptom
- Future developers will inherit your solution

## CONSTRAINTS

- The fix must pass the existing test suite
- Don't break unrelated functionality
- Follow the project's existing patterns and style
- Handle edge cases the original code missed

## REQUIRED FILE STRUCTURE

You MUST maintain these state files throughout your work:

### STATE.md
Track decisions and progress:
```markdown
## Current Status
[in_progress | blocked | complete]

## Decisions Made
- Decision 1: [rationale]
- Decision 2: [rationale]

## Blockers
- [Any blocking issues]

## Next Steps
- [Immediate next action]
```

### ANALYSIS.md
Document your understanding:
```markdown
## Issue Summary
[Brief description]

## Root Cause
[Technical explanation]

## Affected Code
| File | Function | Impact |
|------|----------|--------|
| ... | ... | ... |
```

### PLAN.md
Your implementation plan:
```markdown
## Approach
[Strategy description]

## Changes
1. [ ] Change 1
2. [ ] Change 2

## Verification
- [ ] Tests pass
- [ ] No regressions
```

Update these files as you work. Your final STATE.md should show "complete".

---

*Note: Prescribed file structure. Claude must maintain these files.*
