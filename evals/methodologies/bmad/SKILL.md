---
name: bmad-methodology
description: "BMAD Method: AI-driven agile with 21 specialized agents, scale-adaptive planning (L0-L4), and 34 workflows across analysis, planning, architecture, and implementation phases."
---

# BMAD Method

Build More, Architect Dreams. AI-driven agile development framework.

**Source**: [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)

## Core Principle

> "Scale-adaptive intelligence that adjusts from bug fixes to enterprise systems."

BMAD positions AI agents as collaborative guides through structured workflows, not replacements for human expertise.

## Scale-Adaptive Levels

The framework automatically adjusts planning depth based on project complexity:

| Level | Track | Use Case | Depth |
|-------|-------|----------|-------|
| **L0** | Quick Flow | Bug fixes, typos, small tweaks | Minimal (~5 min) |
| **L1** | BMad Method | Features, products, platforms | Standard (~15 min) |
| **L2** | Enterprise Light | Multi-team, some compliance | Extended (~20 min) |
| **L3** | Enterprise | Regulated industries | Full (~25 min) |
| **L4** | Enterprise Heavy | High compliance, audit trails | Maximum (~30 min) |

**Selection criteria:**
- L0: Change touches 1-3 files, no architectural impact
- L1: New feature or significant change, single team
- L2-L4: Cross-team, compliance requirements, audit needs

## Four Core Phases

### Phase 1: Analysis

Understand the problem before proposing solutions.

**Activities:**
- Requirements gathering
- Stakeholder identification
- Constraint discovery
- Risk assessment
- Success criteria definition

**Key question:** "What are we actually trying to solve?"

### Phase 2: Planning

Structure the approach before execution.

**Activities:**
- Scope definition
- Resource allocation
- Timeline estimation
- Dependency mapping
- Milestone definition

**Key question:** "How will we approach this systematically?"

### Phase 3: Architecture

Design systems before building them.

**Activities:**
- System decomposition
- Interface definition
- Data modeling
- Integration planning
- Technical decision documentation

**Key question:** "What's the right structure for this system?"

### Phase 4: Implementation

Build according to plan and architecture.

**Activities:**
- Incremental development
- Continuous integration
- Testing at each stage
- Documentation updates
- Stakeholder demos

**Key question:** "Are we building what we designed?"

## Specialized Agent Roles

BMAD employs 21 specialized agents. Key roles:

| Agent | Responsibility | When Active |
|-------|----------------|-------------|
| **Product Manager** | Requirements, priorities, stakeholder alignment | Analysis, Planning |
| **Architect** | System design, technical decisions, patterns | Architecture |
| **Developer** | Implementation, code quality, testing | Implementation |
| **UX Designer** | User experience, interaction design | Analysis, Architecture |
| **Scrum Master** | Process facilitation, blocker removal | All phases |
| **QA Engineer** | Test strategy, quality gates | Planning, Implementation |
| **DevOps** | Infrastructure, deployment, monitoring | Architecture, Implementation |
| **Security** | Threat modeling, security review | Architecture |
| **Tech Writer** | Documentation, knowledge transfer | All phases |

**Agent coordination:** Agents hand off to each other at phase boundaries with structured context transfer.

## Workflow Structure

34 workflows across the 4 phases:

**Analysis workflows:**
- Requirements elicitation
- Stakeholder mapping
- Problem decomposition
- Feasibility assessment

**Planning workflows:**
- Sprint planning
- Backlog refinement
- Risk mitigation planning
- Resource allocation

**Architecture workflows:**
- System design
- API design
- Data modeling
- Security architecture
- Integration design

**Implementation workflows:**
- Feature development
- Bug fixing
- Refactoring
- Code review
- Testing
- Deployment

## Modules

| Module | Purpose | Use When |
|--------|---------|----------|
| **BMad Method (BMM)** | Core 34 workflows | Standard development |
| **BMad Builder (BMB)** | Custom agent creation | Domain-specific needs |
| **Creative Intelligence Suite (CIS)** | Innovation workflows | Exploration, R&D |

## Application by Scale Level

### L0: Quick Flow (Bug Fix Example)

```
1. Identify: What's broken?
2. Locate: Where's the bug?
3. Fix: Minimal change to resolve
4. Verify: Does it work? Any regressions?
5. Done: Commit with clear message
```

No heavy process—just fix it right.

### L1: BMad Method (Feature Example)

```
Analysis:
  - What does the feature do?
  - Who needs it and why?
  - What are the acceptance criteria?

Planning:
  - What tasks are needed?
  - What order? Dependencies?
  - How will we test it?

Architecture:
  - Where does it fit in the system?
  - What interfaces change?
  - Any data model changes?

Implementation:
  - Build incrementally
  - Test as you go
  - Document decisions
```

### L2-L4: Enterprise (Complex Feature Example)

Full workflow with:
- Formal requirements documents
- Architecture decision records (ADRs)
- Security review checkpoints
- Compliance documentation
- Audit trail for all decisions
- Multi-stakeholder sign-offs

## Just-In-Time Documentation

BMAD produces documentation as a byproduct of the process:

| Artifact | Created During | Purpose |
|----------|----------------|---------|
| Requirements doc | Analysis | What we're building |
| ADRs | Architecture | Why we chose this approach |
| API specs | Architecture | Interface contracts |
| Test plans | Planning | How we'll verify |
| Runbooks | Implementation | How to operate |

**Principle:** Documentation emerges from doing the work, not as separate activity.

## Application to This Task

When given a development task:

1. **Assess scale level** — Is this L0 (quick fix) or L1+ (needs process)?

2. **For L0:** Just fix it. Verify. Commit.

3. **For L1+:**
   - **Analysis:** Clarify requirements, identify constraints
   - **Planning:** Break into tasks, sequence them
   - **Architecture:** Design before building (if structural changes)
   - **Implementation:** Build incrementally, test as you go

4. **Engage appropriate agents:**
   - Unclear requirements? → Product Manager thinking
   - System design question? → Architect thinking
   - Implementation detail? → Developer thinking

5. **Document decisions:** Capture why, not just what.

The overhead scales with complexity—simple tasks stay simple, complex tasks get the process they need.
