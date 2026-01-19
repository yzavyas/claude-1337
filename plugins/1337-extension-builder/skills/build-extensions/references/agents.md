# Agents

Specialized subagents for autonomous task handling. Location: `agents/name.md`

Source: [Claude Code - Sub-agents](https://code.claude.com/docs/en/sub-agents.md)

---

## Official Schema (Claude Code)

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `name` | string | **Yes** | Lowercase letters and hyphens only, no spaces |
| `description` | string | **Yes** | Guides Claude's delegation decisions, include examples |
| `model` | string | No | `inherit`, `sonnet`, `opus`, `haiku` (default: `sonnet`) |
| `color` | string | No | UI background color for visual identification |
| `tools` | string/array | No | Tools agent can use (default: inherit from parent) |
| `disallowedTools` | string/array | No | Tools to explicitly deny |
| `skills` | string/array | No | Skills injected fully at startup |
| `hooks` | object | No | Lifecycle hooks (PreToolUse, PostToolUse, Stop) |
| `permissionMode` | string | No | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |

**Key insight:** Examples go IN the description using YAML multiline (`|`). The description is the trigger.

---

## Template

```markdown
---
name: agent-identifier
description: |
  [Role description]. Use when: [triggering conditions].

  <example>
  Context: [Situation description]
  user: "[User request]"
  assistant: "[How assistant should respond]"
  <commentary>
  [Why this agent should be triggered]
  </commentary>
  </example>

  <example>
  Context: [Another situation]
  user: "[Another request]"
  assistant: "[Response]"
  <commentary>
  [Why triggered]
  </commentary>
  </example>
model: inherit
color: blue
tools: ["Read", "Grep", "Glob"]
skills: skill-name
---

You are a specialized agent for [purpose].

**Your Core Responsibilities:**
1. [Primary responsibility]
2. [Secondary responsibility]

**Process:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Output Format:**
[Expected output structure]

**Edge Cases:**
- [Edge case 1]: [How to handle]
```

---

## Frontmatter Fields

| field | required | description |
|-------|----------|-------------|
| `name` | yes | Identifier (lowercase, hyphens, 3-50 chars) |
| `description` | yes | Triggering conditions + `<example>` blocks |
| `model` | yes | `inherit`, `sonnet`, `opus`, `haiku` |
| `color` | yes | Visual identifier in UI |
| `tools` | no | Array of allowed tools (default: all) |
| `skills` | no | Skills to load into subagent context at startup |

### name

```yaml
# Good
name: code-reviewer
name: test-generator
name: api-docs-writer

# Bad
name: helper      # too generic
name: -agent-     # starts/ends with hyphen
name: my_agent    # underscores not allowed
name: ag          # too short
```

### description

**Critical field** - determines when Claude triggers the agent.

Must include:
1. Role + triggering conditions ("[Role]. Use when: [triggers]")
2. Multiple `<example>` blocks showing usage
3. `<commentary>` explaining why agent triggers

**Use YAML multiline (`|`) for examples:**

```yaml
description: |
  Code review specialist. Use when: reviewing code, checking quality, validating implementations.

  <example>
  Context: The user has just implemented a new feature.
  user: "Can you check if everything looks good?"
  assistant: "I'll use the Task tool to launch the code-reviewer agent."
  <commentary>
  Since the user wants validation, use the code-reviewer agent.
  </commentary>
  </example>

  <example>
  Context: The assistant has just written new code.
  user: "Please create a function to validate emails"
  assistant: [writes code, then] "Now I'll review this implementation."
  <commentary>
  Proactively use after writing new code to catch issues early.
  </commentary>
  </example>
```

### model

| value | meaning |
|-------|---------|
| `inherit` | Same as parent (recommended) |
| `sonnet` | Balanced |
| `opus` | Most capable, expensive |
| `haiku` | Fast, cheap |

### color

Visual identifier in UI.

| color | suggested use |
|-------|---------------|
| `blue` | Analysis, research |
| `cyan` | Exploration, discovery |
| `green` | Success-oriented, generation |
| `yellow` | Caution, validation |
| `magenta` | Creative, generation |
| `red` | Critical, security |

### tools

Array of tool names. Omit for full access.

```yaml
# Read-only analysis
tools: ["Read", "Grep", "Glob"]

# Code generation
tools: ["Read", "Write", "Grep", "Glob"]

# Testing
tools: ["Read", "Bash", "Grep"]

# Research
tools: ["Read", "Grep", "Glob", "WebFetch", "WebSearch"]

# Full access (default if omitted)
tools: ["*"]
```

**Principle of least privilege** - limit to minimum needed.

### skills

Skills to load into subagent context at startup. Subagents don't inherit skills from parent.

```yaml
# Single skill
skills: build-core

# Multiple skills (comma-separated)
skills: build-core, build-extension-builder

# Multiple skills (list format)
skills:
  - build-core
  - build-extension-builder
```

**Important:** Skill content is fully injected at startup, not just made available for invocation.

---

## System Prompt Design

The markdown body becomes the agent's system prompt. Write in second person.

### Structure

```markdown
You are [role] specializing in [domain].

**Your Core Responsibilities:**
1. [Primary responsibility]
2. [Secondary responsibility]

**Process:**
1. [Step one]
2. [Step two]
3. [Step three]

**Quality Standards:**
- [Standard 1]
- [Standard 2]

**Output Format:**
Provide results in this format:
- [What to include]
- [How to structure]

**Edge Cases:**
- [Edge case 1]: [How to handle]
- [Edge case 2]: [How to handle]
```

### Best Practices

| do | don't |
|----|-------|
| Write in second person ("You are...") | First person ("I am...") |
| Be specific about responsibilities | Be vague or generic |
| Provide step-by-step process | Omit process steps |
| Define output format | Leave format undefined |
| Include quality standards | Skip quality guidance |
| Address edge cases | Ignore error cases |
| Keep under 10,000 chars | Write novels |

---

## Agent Patterns

| pattern | tools | use case |
|---------|-------|----------|
| **explorer** | Read, Grep, Glob | Codebase search, discovery |
| **verifier** | Read, Grep, Bash | Validation, testing |
| **researcher** | WebFetch, WebSearch, Read | Web synthesis |
| **reviewer** | Read, Grep, Glob | Code review, analysis |
| **generator** | Read, Write, Grep, Glob | Code generation |

---

## Complete Examples

### Read-Only Analyzer

```markdown
---
name: code-complexity-analyzer
description: |
  Code complexity analyst. Use when: analyzing maintainability, identifying refactoring opportunities, finding complexity issues.

  <example>
  Context: User is reviewing a large module.
  user: "This module seems hard to maintain. What should I refactor?"
  assistant: "I'll analyze the code complexity to identify refactoring targets."
  <commentary>
  Use complexity analyzer to find maintainability issues systematically.
  </commentary>
  </example>
model: inherit
color: cyan
tools: ["Read", "Grep", "Glob"]
---

You are a code complexity analyst who identifies maintainability issues.

**Your Core Responsibilities:**
1. Calculate cyclomatic complexity for functions
2. Identify deeply nested code blocks
3. Find overly long functions
4. Detect code duplication patterns

**Process:**
1. Scan target files with Grep for function definitions
2. Read each function and calculate complexity metrics
3. Rank issues by severity
4. Provide specific refactoring recommendations

**Output Format:**
| File | Function | Complexity | Issue | Recommendation |
|------|----------|------------|-------|----------------|
| ... | ... | ... | ... | ... |

Focus on actionable improvements, not exhaustive metrics.
```

### Research Agent

```markdown
---
name: best-practices-researcher
description: |
  Best practices researcher. Use when: finding current guidance, researching patterns, verifying approaches.

  <example>
  Context: User is implementing authentication.
  user: "What's the current best practice for JWT refresh tokens?"
  assistant: "I'll research current JWT refresh token best practices."
  <commentary>
  Research agent finds authoritative, current guidance.
  </commentary>
  </example>
model: sonnet
color: blue
tools: ["WebFetch", "WebSearch", "Read"]
---

You are a best practices researcher who finds authoritative, current guidance.

**Your Core Responsibilities:**
1. Search for authoritative sources (official docs, RFCs, security advisories)
2. Verify information is current (2024-2025)
3. Synthesize findings into actionable recommendations
4. Cite sources with URLs

**Process:**
1. WebSearch for "[topic] best practices 2025"
2. WebFetch top 3-5 authoritative sources
3. Cross-reference for consensus
4. Identify any security considerations
5. Summarize with citations

**Output Format:**
## Best Practices: [Topic]

**Recommendation:** [Clear guidance]

**Key Points:**
1. [Point 1] ([Source](url))
2. [Point 2] ([Source](url))

**Security Considerations:**
- [Consideration]

**Sources:**
- [Source 1](url)
- [Source 2](url)
```

---

## Critical Constraints

| constraint | reason |
|------------|--------|
| No nesting | Subagents cannot spawn other subagents |
| Single responsibility | Clear completion criteria |
| Explicit tools | Tools not inherited from parent |
| Example blocks required | Claude needs examples for triggering |

---

## Quality Checklist

- [ ] Name is 3-50 chars, lowercase, hyphens only
- [ ] Description includes triggering conditions
- [ ] Description has 2-4 `<example>` blocks with `<commentary>`
- [ ] Model is specified (`inherit` recommended)
- [ ] Color is specified and appropriate
- [ ] Tools are minimal for the role
- [ ] System prompt is in second person
- [ ] Process steps are explicit
- [ ] Output format is defined
- [ ] Edge cases are addressed
- [ ] Tested with representative tasks
