---
name: 1337-extension-builder
description: "Build Claude cognitive extensions — skills, hooks, agents, commands, MCP servers. Use when: creating any extension type, designing for collaborative intelligence, want evidence-based methodology. Composes with example-skills:skill-creator for skill fundamentals."
---

# Extension Builder

Build cognitive extensions for Claude Code — skills, hooks, agents, commands, MCP servers.

**Composes with**: `example-skills:skill-creator` for skill anatomy and packaging. This adds the methodology.

## Five Extension Modalities

| modality | purpose | what it extends |
|----------|---------|-----------------|
| **skill** | knowledge + decision frameworks | what Claude knows |
| **hook** | event-triggered actions | session behavior |
| **agent** | specialized subagent type | reasoning delegation |
| **command** | workflow shortcuts | repeatable procedures |
| **mcp** | external system integration | reach beyond Claude |

## Methodology

### Standing on Giants' Shoulders

Knowledge accumulates. Languages build on languages. Patterns build on patterns. We inherit tools forged by masters.

The filter: **which giants?** Not all popular things are best-in-class. Choose by evidence quality, not trends.

| priority | source | why trust it |
|----------|--------|--------------|
| 1 | production codebases | what actually ships at scale |
| 2 | core maintainers | primary knowledge holders, understand tradeoffs |
| 3 | conference talks | war stories reveal real-world gotchas |
| 4 | proven adoption | social proof + sustained real usage |
| 5 | technical blogs | secondary, may be outdated — always verify |

**Data quality matters.** GitHub stars ≠ production-ready. Popular ≠ correct. What experts actually use in production is the ground truth.

### Scientific Method

1. **hypothesize** — what gap exists? what would fix it?
2. **test** — build extension, measure activation/quality
3. **observe** — where does it fail? false positives/negatives?
4. **refine** — improve based on evidence, not assumption

Don't guess. Measure. Run evals. Check if it actually activates. Verify claims.

### First Principles

Reason from fundamentals, not by analogy.

Before building, ask:
- what will the next collaborator experience encountering this?
- will the next enhancement be easier or harder because of this choice?
- if I do this 100 times, is the pattern sustainable?
- how do I make doing the right thing the only obvious path?

The balance: first principles without giants = reinventing wheels. Giants without first principles = cargo culting.

### The Trinity

The three methodology pillars work together:

```
First Principles: "What is fundamentally true here?"
         ↓
Giants' Shoulders: "What have masters learned about this?"
         ↓
Scientific Method: "Does this actually work in this context?"
```

For the full theoretical foundation, see [methodology documentation](/explore/explanation/methodology/).

## Principles

1. **best-in-class only** — battle-tested components
2. **evidence over opinion** — production usage > GitHub stars
3. **concise** — decision frameworks + gotchas, not tutorials
4. **Claude is smart** — only add what Claude doesn't already know

### Additional Principles

| principle | meaning |
|-----------|---------|
| **rigor** | verify claims before asserting (Chain of Verification) |
| **ratchet** | each collaboration crystallizes into permanent gain |
| **pit of success** | make the right thing the only obvious path |

## Design Philosophy

### Pit of Success

Make the right thing the only obvious path. Don't rely on documentation — rely on structure.

| extension type | pit of success means |
|----------------|---------------------|
| skill | description with clear "Use when:" triggers |
| hook | defaults that work, explicit failure modes |
| command | predictable behavior, helpful errors |
| agent | clear completion criteria, limited scope |

### Mistake-Proofing (Poka-yoke)

Catch errors where they originate, not downstream.

| common mistake | how to prevent |
|----------------|----------------|
| vague description | validation requires "Use when:" |
| missing evidence | template requires source per recommendation |
| over-activation | require `should_not_trigger` test cases |
| unverified claims | CoVe checklist before commit |

## Extension-Specific Guidance

### Skills

See [research-workflow.md](references/research-workflow.md) for the full methodology.

| step | do |
|------|----|
| 1 | test Claude's knowledge, find gaps |
| 2 | research 3 production codebases |
| 3 | verify with maintainer quotes |
| 4 | collect production gotchas |
| 5 | fill in SKILL.md template |
| 6 | run validation checks |

**Skill activation**: Skills activate through pure LLM reasoning. The description is the **only signal** Claude uses to decide whether to load.

| good | bad |
|------|-----|
| "Use when:" clause | generic descriptions |
| specific tools/terms | abstract terms |
| action verbs | missing triggers |

### Hooks

Hooks run shell/Python scripts at lifecycle events. **Deterministic control** — no LLM decision, guaranteed execution.

| event | when | can block? |
|-------|------|------------|
| `PreToolUse` | before tool execution | yes |
| `PostToolUse` | after tool success | yes |
| `UserPromptSubmit` | user sends message | yes |
| `Stop` | main agent finishes | yes |
| `SubagentStop` | subagent finishes | yes |
| `PermissionRequest` | permission dialog shown | yes |
| `SessionStart` | session begins | no |
| `SessionEnd` | session terminates | no |
| `PreCompact` | before context compaction | no |
| `Notification` | claude sends notification | no |

**Exit codes**: 0 = success, 1 = non-blocking error, 2 = blocking error

**Hook design principles**:
- 60-second timeout default
- parallel execution for matching hooks
- validate all inputs, quote shell variables
- use `$CLAUDE_PROJECT_DIR` for absolute paths

### Agents

Agents are specialized subprocesses with **separate context windows** and restricted tools.

| pattern | use case |
|---------|----------|
| explorer | codebase search, pattern finding |
| verifier | validation, eval execution |
| researcher | web search, synthesis |
| planner | architecture, implementation planning |

**Critical constraint**: Subagents **cannot spawn other subagents**. No nesting.

**Agent design principles**:
- single responsibility — one clear capability
- clear completion criteria — agent knows when it's done
- limited tool access — only what's needed
- explicit skill listing — skills not inherited from parent

### Commands

Slash commands are workflow shortcuts — prompts that expand.

| pattern | example |
|---------|---------|
| commit workflows | `/commit` → staged changes + message |
| code review | `/review-pr 123` → fetch and analyze |
| diagnostics | `/debug` → collect context |

**Command design principles**:
- predictable behavior — same input → same process
- composable — can chain with other commands
- documented — help text in command definition

### MCP Servers

MCP servers expose external capabilities to Claude via Model Context Protocol.

| integration type | examples |
|------------------|----------|
| data sources | databases, APIs, file systems |
| actions | deployments, notifications |
| knowledge | documentation, search indexes |

**Token limits**: 10k warning threshold, 25k max (configurable via `MAX_MCP_OUTPUT_TOKENS`)

**MCP design principles**:
- minimal surface — only expose what's needed
- secure by default — validate all inputs
- observable — logging, error handling
- local scope for credentials — don't commit secrets

## Content Triage

See [content-triage.md](references/content-triage.md) for the full filter.

**Quick test:**

```
Does Claude already know this well? → YES → Does it add decision framework or gotcha? → NO → CUT
```

### Include

| signal | example |
|--------|---------|
| corrects assumptions | "async-std is deprecated" |
| production gotcha | Mutex across await |
| decision framework | string ownership 95% rule |
| evidence-based | ripgrep uses lexopt not clap |
| non-obvious footgun | CString lifetime trap |

### Cut

| signal | example |
|--------|---------|
| basic syntax | `for x in items { }` |
| textbook examples | `fn longest<'a>(...)` |
| generic explanations | "Rust uses ownership..." |
| complete tutorials | step-by-step guides |

## Size Targets

| component | target | why |
|-----------|--------|-----|
| SKILL.md | < 500 lines | loads on skill activation |
| reference | no hard limit | loads on-demand after SKILL.md |
| hook script | <50 lines | runs on every invocation |
| command prompt | no limit | expands on invocation |

## Validation Checklist

After building any extension:

- [ ] battle-tested, best-in-class picks
- [ ] each recommendation has evidence
- [ ] content is decisions, not tutorials
- [ ] would an expert find this useful?
- [ ] description has "Use when:" clause
- [ ] tested in real session

## Quality Gates

Before publishing any extension:

| gate | target | principle |
|------|--------|-----------|
| sources | 3+ codebases | Independent? If <3, limitation noted? |
| evidence | production-tier | Highest quality available used? |
| CoVe | 100% claims | Each claim traceable to source? |
| activation (skills) | F1 ≥0.8, FPR ≤20% | Triggers correctly, doesn't over-trigger? |

**When evidence is sparse:** Acknowledge limitations explicitly. "Based on limited evidence from X" is honest. Confident claims from weak evidence is not.

See [research-workflow.md](references/research-workflow.md) Step 6 for full validation process.

## Creation Process

### 1. Research Phase

Identify gap → gather evidence → synthesize findings.

When complete, **present research summary for approval**:

```markdown
## Research Summary: [extension-name]

### Gap Identified
[What Claude gets wrong or gives generic advice on]

### Evidence Gathered

| source | type | finding |
|--------|------|---------|
| [codebase/maintainer/talk] | [production/authority/war-story] | [what was learned] |

### Decision Rationale
[Why these choices over alternatives — with evidence]

### Proposed Structure

[extension-name]/
├── SKILL.md              # [what goes here]
└── references/
    ├── [ref-1].md        # [what this covers]
    └── [ref-2].md        # [what this covers]

### Key Content
[3-5 bullet points of what the extension will teach]

---
**Awaiting approval before implementation.**
```

### 2. Implementation Phase (after approval)

1. draft — fill in structure with evidence-backed content
2. triage — apply content filter ruthlessly
3. validate — use the checklist below
