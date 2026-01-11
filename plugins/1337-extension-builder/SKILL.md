---
name: 1337-extension-builder
description: "Build Claude cognitive extensions. Use when: creating skills/hooks/agents/commands/MCP/plugins, need templates, need quality validation, building for the 1337 marketplace."
---

# Extension Builder

Build cognitive extensions that enable effective collaboration, where both human and Claude grow through the partnership.

## Why This Matters

Extensions become part of how users think and work. The difference between helpful and harmful comes down to how it's built.

**Good extensions:**
- Show reasoning (user learns WHY, not just WHAT)
- Provide control (user shapes direction)
- Fill gaps (what Claude doesn't already know)
- Compound value (each enhancement makes the next easier)

**Bad extensions:**
- Hide reasoning (black box)
- Replace thinking (user just consumes output)
- Repeat basics (bloat without insight)
- Create dependency (user less capable without it)

---

## Design Principles

Build these into every extension.

### Transparency (β = 0.415 effect)

Make reasoning visible so users can verify and learn.

| Pattern | Implementation |
|---------|----------------|
| **Show the claim** | What you're recommending |
| **Show the why** | Reasoning behind it |
| **Show alternatives** | What you considered and rejected |
| **Show the source** | Where this comes from |
| **Show uncertainty** | Confidence level (1-10) |

**Example in a skill:**
```markdown
### Error Handling

Use `thiserror` for library errors, `anyhow` for applications.

**Why:** thiserror derives std::error::Error with zero runtime cost.
anyhow provides context chaining but hides the error type.

**Source:** Rust API Guidelines, tokio/reqwest usage patterns.
```

### Control (β = 0.507 effect, strongest)

Give users agency over direction.

| Pattern | Implementation |
|---------|----------------|
| **Decision frameworks** | Teach HOW to decide, not WHAT to do |
| **Tradeoff tables** | Options with tradeoffs, user chooses |
| **Approval gates** | Stop before irreversible actions |
| **Checkpoints** | Verifiable steps in complex workflows |

**Example decision framework:**
```markdown
### Which Error Type?

| Context | Use | Why |
|---------|-----|-----|
| Library (public API) | thiserror | Callers need to match on error types |
| Application (internal) | anyhow | Context matters more than type |
| Both (lib + binary) | thiserror + anyhow | Export typed errors, use anyhow internally |
```

### Pit of Success

Make the right thing the only obvious path.

Structure your extension so correct behavior is natural:
- Default to safe options
- Make dangerous operations require extra steps
- Use constraints, not documentation

### Mistake-Proofing (Poka-Yoke)

Catch errors where they originate.

- Validate assumptions early
- Surface uncertainty at decision points
- Include "watch out for" sections

### Observability

Make extension behavior visible and controllable by default.

#### OTel Instrumentation

Instrument extensions so behavior is measurable and debuggable.

| Extension Type | OTel | Key Spans |
|----------------|------|-----------|
| **Agents** | Required | `agent_run`, `llm_call`, `tool_call` |
| **MCP Servers** | Required | `mcp_server`, `mcp_call` |
| **SDK Apps** | Required | `session`, `turn`, `tool_call` |
| **Skills** | Recommended | `skill_check`, `skill_match`, `skill_load` |
| **Hooks** | Recommended | `hook_trigger`, `hook_handler` |
| **Commands** | Recommended | `command`, `command_execute` |

**Minimum attributes to capture:**
- `success` (bool), `duration_ms` (int), `error` (string if failed)
- For LLM calls: `input_tokens`, `output_tokens`, `model`
- For tool calls: `tool_name`, `tool_args` (truncated)

**Local-first tracing:**
```python
# Phoenix (local, no cloud required)
import phoenix as px
px.launch_app()  # localhost:6006

from opentelemetry import trace
tracer = trace.get_tracer("my-extension")
```

See [observability.md](references/observability.md) for complete instrumentation patterns.

#### Hook Behavior

For hooks that modify Claude's behavior:

| Hook | Observable use |
|------|----------------|
| PreToolUse | Show what's about to happen, let user cancel |
| PostToolUse | Log results, surface unexpected outcomes |
| SessionStart | Inject awareness, set context |

**Suggest, don't block:**
```bash
# Good: Shows alternative, lets user proceed
{"decision": "allow", "message": "Consider using rg instead of grep (faster). Proceeding with grep."}

# Bad: Removes choice
{"decision": "block", "message": "Use rg instead."}
```

**Opt-out mechanism:**
Every hook-based extension must:
- Document how to disable
- Respect environment variables (e.g., `SKIP_HOOKS=1`)
- Never hard-block without escape hatch

**Reasoning traces:**
When hooks modify behavior, show:
- What triggered the hook
- What the hook recommends
- Why (brief reasoning)
- How to proceed with original if desired

---

## Five Extension Types

| type | purpose | what it extends |
|------|---------|-----------------|
| **skill** | knowledge + decision frameworks | what Claude knows |
| **hook** | event-triggered actions | session behavior |
| **agent** | specialized subagent | reasoning delegation |
| **command** | workflow shortcuts | repeatable procedures |
| **mcp** | external system integration | reach beyond Claude |

---

## Building a Skill

Skills are the most common extension. Follow Anthropic's patterns.

### Structure

```
skill-name/
├── SKILL.md           (required - < 500 lines)
├── references/        (detailed docs, load as needed)
├── scripts/           (executable code)
└── assets/            (templates, files for output)
```

### SKILL.md Anatomy

**Frontmatter** (required):
```yaml
---
name: skill-name
description: "What it does. Use when: specific triggers."
---
```

The description is the trigger. Claude reads this to decide when to load. Be specific about "Use when:".

**Body** (required):
1. Brief intro (1-2 sentences)
2. Why this approach (practical motivation, not academic)
3. Core content (decision tables, workflows, gotchas)
4. References section (what to load when)

### What Goes in SKILL.md vs References

| SKILL.md | references/ |
|----------|-------------|
| High-level workflow | Detailed patterns |
| Decision frameworks | Full examples |
| "Load X when Y" navigation | Academic/industry citations |
| Practical motivation | Research foundations |
| < 500 lines | No limit |

**Key insight:** SKILL.md is pragmatic and motivating. References are where depth lives.

### The Filter

```
Claude already knows this? → YES → Cut it
Non-obvious insight? → NO → Cut it
```

| include | cut |
|---------|-----|
| Production gotchas | Basic syntax |
| Decision frameworks | Textbook examples |
| Corrects assumptions | Generic explanations |
| What Claude gets wrong | Complete tutorials |

### Progressive Disclosure

Skills share context with everything else. Treat tokens as a public good.

1. **Metadata** (~100 words) - Always loaded, triggers activation
2. **SKILL.md body** (< 500 lines) - Loaded when skill activates
3. **References** (unlimited) - Loaded when Claude needs them

Reference each file clearly:
```markdown
## References

| need | load |
|------|------|
| Python patterns | [python.md](references/python.md) |
| Error handling | [errors.md](references/errors.md) |
```

---

## Building Other Extension Types

Each type has its own reference with templates and best practices.

| building... | load |
|-------------|------|
| skill | [skills.md](references/skills.md) |
| hook | [hooks.md](references/hooks.md) |
| agent | [agents.md](references/agents.md) |
| command | [commands.md](references/commands.md) |
| mcp server | [mcp.md](references/mcp.md) |
| sdk app | [sdk-apps.md](references/sdk-apps.md) |

---

## Validation Checklist

Before shipping:

### Content Quality
- [ ] Fills gaps (what Claude doesn't know)
- [ ] Decisions, not tutorials
- [ ] Each claim has source (in references)
- [ ] Tested in real session

### Transparency Built-In
- [ ] Reasoning visible for recommendations
- [ ] Sources cited or source types named
- [ ] Uncertainty acknowledged where relevant
- [ ] Alternatives considered and shown

### Control Built-In
- [ ] Decision frameworks, not mandates
- [ ] Tradeoffs presented for significant choices
- [ ] User can shape direction
- [ ] Approval gates for irreversible actions (if applicable)

### Observability Built-In
- [ ] OTel spans defined (agents/MCP/SDK: required; skills/hooks/commands: recommended)
- [ ] Key attributes captured (success, duration_ms, error)
- [ ] Traces route to local collector (Phoenix or OTLP)
- [ ] Hooks suggest, don't block (user retains choice)
- [ ] Opt-out mechanism documented (for hooks)
- [ ] No silent enforcement

### Activation
- [ ] Description has "Use when:"
- [ ] Triggers on right prompts
- [ ] Doesn't over-activate

### Quality
- [ ] Expert finds this useful
- [ ] User MORE capable after using
- [ ] Passes the pit of success test

---

## Publishing

For 1337 marketplace:

1. Create plugin in `plugins/<name>-1337/`
2. Add to `.claude-plugin/marketplace.json`
3. Add display metadata to `.claude-plugin/metadata.json`

See [marketplace-schema.md](references/marketplace-schema.md) for schema details.

---

## Quality Assurance

After building an extension, validate it through the eval→optimize cycle.

### Quick Evaluation

```
"Evaluate plugins/my-extension-1337"
```

The evaluator agent checks all 6 quality gates and returns a verdict:
- **1337**: ≥15/18, no gate below 2, no critical issues → ready to ship
- **NEEDS WORK**: ≥10/18, fixable issues → run optimizer
- **NOT READY**: <10/18 or fundamental problems → rethink approach

### Optimization

If evaluator returns NEEDS WORK:

```
"Optimize plugins/my-extension-1337 based on the evaluation"
```

The optimizer agent:
- Fixes issues in priority order (critical → major → minor)
- Applies minimal changes (surgical, not sweeping)
- Escalates domain decisions to you
- Reports what was fixed and what needs human input

### Full Quality Loop

For hands-off tuning:

```
"Run quality loop on plugins/my-extension-1337 until it passes"
```

This runs eval→optimize→re-eval cycles (max 3 iterations) until the extension reaches 1337 status or escalates issues that need human decisions.

### When to Run

| Situation | Action |
|-----------|--------|
| Just built new extension | Run evaluator |
| Evaluator says NEEDS WORK | Run optimizer |
| After optimizer fixes | Re-run evaluator |
| Want full automated tuning | Run quality loop |
| Auditing existing plugins | Run evaluator on each |

See [plugin-tuning-runbook.md](../../scratch/plugin-tuning-runbook.md) for detailed step-by-step execution guide.

---

## References

### Extension Type Guides

| type | reference | contains |
|------|-----------|----------|
| skill | [skills.md](references/skills.md) | Templates, best practices, examples |
| hook | [hooks.md](references/hooks.md) | Event types, script patterns |
| agent | [agents.md](references/agents.md) | Frontmatter, delegation patterns |
| command | [commands.md](references/commands.md) | Argument parsing, workflows |
| mcp | [mcp.md](references/mcp.md) | Server patterns, tool design |
| sdk app | [sdk-apps.md](references/sdk-apps.md) | Agent SDK patterns |

### Observability

| need | load |
|------|------|
| Building observable extensions | [observability.md](references/observability.md) |

### Methodology

| need | load |
|------|------|
| Evidence workflow | [evidence-templates.md](references/evidence-templates.md) |
| Evaluation | [evals.md](references/evals.md) |
| Plugin manifest | [plugin-schema.md](references/plugin-schema.md) |
| Marketplace schema | [marketplace-schema.md](references/marketplace-schema.md) |

Research foundations live in core-1337. Load that skill for methodology depth.
