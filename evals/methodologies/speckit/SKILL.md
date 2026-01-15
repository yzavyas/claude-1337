---
name: speckit-methodology
description: "GitHub's spec-kit: Spec-Driven Development methodology. Constitution→Specify→Clarify→Plan→Analyze→Tasks→Implement workflow for structured, intent-first development."
---

# Spec-Kit Methodology

Spec-Driven Development from GitHub. Specifications become executable—define intent before implementation.

**Source**: [github/spec-kit](https://github.com/github/spec-kit)

## Core Principle

> "Flip the script on traditional software development."

Instead of jumping to code, create detailed specifications that serve as blueprints. The spec IS the implementation guide.

## The 7-Step Workflow

Execute these phases in order for any development task:

### Phase 1: Constitution

Establish governing principles before any work begins.

**Define:**
- Code quality standards (linting, formatting, patterns)
- Testing expectations (coverage, test types required)
- UX consistency requirements
- Performance requirements and budgets
- Security baseline

**Output:** Project principles that guide all subsequent decisions.

### Phase 2: Specify

Define requirements in natural language. Focus on WHAT and WHY, not HOW.

**Include:**
- User-facing features and behaviors
- Business constraints and rules
- Success criteria (how do we know it works?)
- Edge cases and error scenarios

**Key discipline:** No implementation details. Describe the problem and desired outcome only.

### Phase 3: Clarify

Before technical decisions, identify gaps in understanding.

**Ask:**
- What's underspecified?
- What assumptions am I making?
- What could be interpreted multiple ways?
- What edge cases aren't covered?

**Output:** Refined specification with all ambiguities resolved.

### Phase 4: Plan

Bridge from requirements to technical decisions.

**Define:**
- Technology stack choices (with rationale)
- Architectural approach
- System constraints and boundaries
- Integration points
- Data flow

**Key discipline:** Technical decisions traced back to requirements.

### Phase 5: Analyze

Cross-artifact consistency check before implementation.

**Verify:**
- All requirements have corresponding plan elements
- No plan elements without requirements justification
- Consistent terminology across artifacts
- No gaps or contradictions

**Output:** Confidence that spec and plan align.

### Phase 6: Tasks

Generate discrete, actionable work items.

**Each task should be:**
- Small enough to complete in one session
- Independent (minimal dependencies on other tasks)
- Testable (clear done criteria)
- Traceable to a requirement

**Output:** Ordered task list ready for execution.

### Phase 7: Implement

Execute tasks according to specifications and plans.

**For each task:**
1. Reference the specification
2. Follow the plan
3. Write tests first (TDD when appropriate)
4. Implement to spec
5. Verify against done criteria

## When to Use Each Phase

| Situation | Start At |
|-----------|----------|
| New project/feature | Phase 1 (Constitution) |
| Adding to existing project | Phase 2 (Specify) |
| Ambiguous requirements | Phase 3 (Clarify) |
| Clear requirements, need tech decisions | Phase 4 (Plan) |
| Have spec and plan, need work items | Phase 6 (Tasks) |
| Have tasks, ready to code | Phase 7 (Implement) |

## Artifacts Produced

| Phase | Artifact | Purpose |
|-------|----------|---------|
| Constitution | `PRINCIPLES.md` | Governing standards |
| Specify | `SPEC.md` | Requirements |
| Clarify | Updated `SPEC.md` | Refined requirements |
| Plan | `PLAN.md` | Technical approach |
| Analyze | Verification notes | Consistency check |
| Tasks | `TASKS.md` | Work items |
| Implement | Code + tests | Working software |

## Key Differentiators

**Intent-first**: Define what you're building before how you'll build it.

**Structured refinement**: Multi-step specification enhancement, not one-shot prompts.

**Technology-independent**: The methodology doesn't prescribe tech stacks—that's a planning decision.

**Traceable**: Every line of code traces back through tasks → plan → spec → requirements.

## Application to This Task

When given a development task:

1. **Don't start coding immediately**
2. Write a brief specification (Phase 2)
3. Identify ambiguities (Phase 3)
4. Make technical decisions explicit (Phase 4)
5. Break into tasks (Phase 6)
6. Implement with traceability (Phase 7)

The overhead pays off in:
- Fewer wrong turns
- Clearer thinking about edge cases
- Documented decisions for future reference
- Higher confidence in completeness
