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

Building extensions well:
- Evidence + WHY pattern (traceable sources, explain reasoning)
- Source hierarchy (highest quality for the claim — tooling vs methodology)
- Scientific method (hypothesize → test → observe → refine)
- First principles (reason from fundamentals, question assumptions)

*For deeper methodology, see core-1337.*

**Domain-specific application:**

| for extensions | apply as |
|----------------|----------|
| source hierarchy | tooling claims → production codebases; methodology claims → research |
| scientific method | build → test in session → observe activation → refine |
| first principles | does this make the next enhancement easier or harder? |

## Why Methodology Enables Learning

The methodology isn't just for quality — it's how extensions enable builder learning.

| methodology element | quality purpose | learning purpose |
|---------------------|-----------------|------------------|
| **Evidence + WHY** | Claims are grounded | Builder can verify, understand reasoning, form own judgment |
| **Decisions not tutorials** | Content is actionable | Builder learns HOW to decide, can apply independently |
| **Source hierarchy** | Recommendations are trustworthy | Builder can go deeper, verify, build on |
| **Fill gaps only** | No bloat | Concentrated insight, learnable in one session |
| **Scientific method** | Recommendations work | Builder gets tested patterns, not theory |

**If you follow the methodology correctly, you cannot produce an extension that doesn't enable learning.**

### What Happens When You Skip

| if you skip... | extension becomes... | builder outcome |
|----------------|----------------------|-----------------|
| Evidence + WHY | Unverifiable assertions | Blind trust → no growth → dependency |
| Decisions not tutorials | Step-by-step instructions | Can follow → can't apply → dependency |
| Source hierarchy | Weakly grounded claims | Can't verify → can't trust → hesitation |
| Fill gaps | Bloated with basics | Noise drowns signal → confusion |
| Scientific method | Untested theory | Applies wrong things → failure → distrust |

The methodology IS the anti-hollowing mechanism. Skip it and you create dependency. Follow it and learning is automatic.

## How Extensions Compound

"Compound value" isn't abstract — here's how it works:

| mechanism | how it compounds | example |
|-----------|------------------|---------|
| **Shared vocabulary** | Define term once → use everywhere | "transparent abstraction" defined in ethos → used in all extensions |
| **Composability** | Extension A references B → B's knowledge available | extension-builder composes with skill-creator → no duplication |
| **Pattern crystallization** | Framework in domain X → adapt to Y | Decision table pattern → reuse across all extensions |
| **Infrastructure accumulation** | Each hook/command/agent → available for next | New command can use existing hooks |
| **Methodology inheritance** | core-1337 foundation → all extensions built on it | Evidence + WHY propagates automatically |

### Building for Composability

When creating an extension, ask:

| question | if NO | action |
|----------|-------|--------|
| Can another extension reference this? | Isolated, can't compose | Extract reusable concepts |
| Does this use shared vocabulary? | Reinvents terms | Use existing definitions, link to sources |
| Could this pattern apply elsewhere? | Context-locked | Generalize the framework |
| Does this build on existing extensions? | Starts from zero | Compose with relevant extensions |

### The Kaizen Effect

```
Extension 1: defines "transparent abstraction"
     ↓
Extension 2: uses term, adds "decision framework" pattern
     ↓
Extension 3: composes both, adds domain-specific application
     ↓
Each extension starts from higher baseline (corrections flow through too)
```

**This is how the system gets smarter.** Each extension crystallizes knowledge that the next can build on. Corrections are first-class — the baseline improves, not just grows.

## Transparent Abstractions

Extensions must be transparent so builders can learn from them.

| property | what it means | how to produce it |
|----------|---------------|-------------------|
| **readable** | Builder can understand without external context | Plain language. Clear headers. Decision tables over prose. No jargon without definition. |
| **forkable** | Builder can copy, modify, make their own | Self-contained. Modular sections. Clear separation of concerns. |
| **verifiable** | Builder can check any claim | Every recommendation has source. Sources are specific (author, year, context). |
| **observable** | Builder can see how it works | Reasoning visible. Decision points explicit. WHY exposed, not just WHAT. |

### Producing Transparent Extensions

**Do:**
- Use plain language
- Structure with clear headers (##, ###)
- Decision tables for choices
- One concept per section
- Define terms on first use
- Source every recommendation with specific citations
- Show the decision tree, not just the conclusion
- Expose uncertainty: "based on limited evidence from X"

**Don't:**
- Wall of prose
- Jargon without explanation
- "Best practice is..." (unsourced)
- Just state the answer without WHY
- Hide the reasoning
- Appear certain when uncertain

## Content Guidance

| guidance | meaning |
|----------|---------|
| **fill gaps** | only add what Claude doesn't already know |
| **decisions, not tutorials** | decision frameworks + gotchas, not step-by-step guides |
| **compound value** | each choice makes the next enhancement easier or harder |

## Structural Effectiveness

Accurate content that's poorly structured doesn't land. Two CI checks: accuracy (CoVe) AND structure.

### Why Structure Matters

| principle | effect | application |
|-----------|--------|-------------|
| **Coherence** | d = 0.86 (Mayer) | Cut extraneous — every line earns its place |
| **Signaling** | d = 0.46 (Mayer) | Headers, tables, scannable structure |
| **Expertise reversal** | d = ±0.5 (Kalyuga) | Don't scaffold what reader knows — it hurts |

79% of readers scan (Nielsen). Headers are often the only thing they read.

### Structural Checklist

| check | why |
|-------|-----|
| Tables over prose | Scannable, comparable, lower load |
| One concept per section | Working memory = 4 chunks |
| Front-load decisions | Busy readers stop early |
| No wall of text | Breaks fluency, triggers bounce |

### Skills = Reference + Explanation

| section type | structure |
|--------------|-----------|
| Decision tables | Scannable, factual |
| "Why" sections | Context, tradeoffs |
| "When to use" | Clear conditions |
| Examples | Concrete, copy-paste |

Don't write tutorials. Tutorials bore experts. Skills are for lookup and understanding, not hand-holding.

## Design Philosophy

### Pit of Success

Make the right thing the only obvious path. Don't rely on documentation — rely on structure. (Rico Mariani, Microsoft)

| extension type | pit of success means |
|----------------|---------------------|
| skill | description with clear "Use when:" triggers |
| hook | defaults that work, explicit failure modes |
| command | predictable behavior, helpful errors |
| agent | clear completion criteria, limited scope |

### Mistake-Proofing (Poka-yoke)

Catch errors where they originate, not downstream. (Shigeo Shingo, Toyota Production System)

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
| 2 | research multiple production codebases |
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

**Standard:**
- [ ] fills gaps (what Claude doesn't already know)
- [ ] each recommendation has evidence
- [ ] content is decisions, not tutorials
- [ ] would an expert find this useful?
- [ ] description has "Use when:" clause
- [ ] tested in real session

**Learning-Focused:**
- [ ] Can a builder verify any claim by following the source?
- [ ] Are sources specific enough to actually find? (not "according to experts")
- [ ] Can a builder apply this knowledge without the extension loaded?
- [ ] Are decision frameworks provided, not just answers?
- [ ] Could a builder teach this to someone else after reading?
- [ ] Is the reasoning visible, not just the conclusion?
- [ ] Is uncertainty acknowledged where appropriate?

**Anti-Hollowing Check:**
- [ ] Does this create capability or dependency?
- [ ] Would a builder be MORE capable after engaging with this?
- [ ] Is there something to learn, or just something to consume?

If any answer is NO, the extension may create dependency rather than capability. Revise before shipping.

## Marketplace Publishing

When adding plugins to a marketplace, the `marketplace.json` has a strict schema.

**Key gotcha**: No generic `"components"` field. Use explicit fields:

| component | field |
|-----------|-------|
| agents | `"agents": "./agents"` |
| commands | `"commands": "./commands"` |
| hooks | `"hooks": "./hooks.json"` |
| MCP servers | `"mcpServers": {...}` |

See [marketplace-schema.md](references/marketplace-schema.md) for full schema.

## Quality Gates

Before publishing any extension:

| gate | principle |
|------|-----------|
| sources | Multiple independent sources — if limited, acknowledge explicitly |
| evidence | Highest quality for the claim type (tooling → production; methodology → research) |
| claims | Each claim traceable to source (author, year, context) |

**When evidence is sparse:** Acknowledge limitations explicitly. "Based on limited evidence from X" is honest. Confident claims from weak evidence is not.

### Why This Matters: Cascade

Extensions are teaching. Teaching cascades.

| What the extension teaches | Who learns | What they build/teach | Impact |
|---------------------------|------------|----------------------|--------|
| Wrong reasoning | Builder A | 5 extensions | Each propagates the error |
| Correct reasoning | Builder A | 5 extensions | Each propagates correct patterns |

**The asymmetry**: Correct reasoning must be actively verified. Wrong reasoning spreads by default (easier, faster, feels productive).

**CoVe before commit** (line 164) exists because one bad pattern in an extension becomes organizational culture. The extension builder is upstream of everything.

### Pre-Publish CoVe Check

Before publishing, for each factual claim:

1. **What was measured?** (not inferred)
2. **Correlation or causation?** (don't upgrade)
3. **Effect size and sample?** (context)
4. **Replicated?** (single study = tentative)
5. **Counter-evidence?** (acknowledge it)

If you can't answer these for a claim, either find the evidence or label it speculative.

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
