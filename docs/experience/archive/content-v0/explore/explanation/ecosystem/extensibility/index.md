[&larr; ecosystem](../)

# extensibility

<p class="dimmed-intro">five ways to extend claude code</p>

## the five extension types

| type | what it is | use for |
|------|------------|---------|
| **skill** | knowledge that loads when needed | SOPs, runbooks, decision frameworks, domain expertise |
| **hook** | code that runs at specific moments | guardrails, enforcement, auto-formatting, logging |
| **agent** | Claude with specific job + tools | research, validation, code review, exploration |
| **command** | shortcut that expands to prompt | workflows, deployments, repetitive tasks |
| **mcp** | connection to external systems | databases, APIs, file systems, third-party services |

## skills

**What**: Folders with SKILL.md files. Claude reads descriptions, loads matching skills.

**Critical**: The description determines activation. Bad description = never loads.

**Metrics**: activation rate, false positive rate

| docs | link |
|------|------|
| reference | [SDK Overview](https://docs.anthropic.com/en/docs/claude-code/sdk) |
| deep dive | [Agent Skills Engineering](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) |

## hooks

**What**: Shell commands that run at lifecycle events (PreToolUse, PostToolUse, SessionStart, etc.)

**Critical**: Exit code 2 blocks the action. Use for enforcement, not suggestions.

**Metrics**: execution time, block rate, error rate

| docs | link |
|------|------|
| reference | [SDK Overview](https://docs.anthropic.com/en/docs/claude-code/sdk) |
| guide | [Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) |

## agents

**What**: Claude instances with specific tools and a task. Run autonomously, return results.

**Critical**: Agents can't spawn agents. Keep scope narrow.

**Metrics**: steps per task, tool call distribution, success rate

| docs | link |
|------|------|
| reference | [Subagents](https://docs.anthropic.com/en/docs/claude-code/sub-agents) |
| deep dive | [Building Agents](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) |

## commands

**What**: Markdown files that expand to prompts when you type `/commandname`.

**Critical**: They're just prompts. Put the work in the prompt, not magic.

**Metrics**: usage frequency, execution time

| docs | link |
|------|------|
| reference | [CLI Reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference) |

## mcp

**What**: Model Context Protocol servers that expose tools to Claude.

**Critical**: 25k token limit on responses. Design for pagination.

**Metrics**: call latency, error rate per tool

| docs | link |
|------|------|
| reference | [MCP Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/mcp) |
| engineering | [Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) |

## plugins

Bundle of extensions. Install with `/plugin install <name>`.

| docs | link |
|------|------|
| announcement | [Claude Code Plugins](https://www.anthropic.com/news/claude-code-plugins) |

## building extensions

| what | where |
|------|-------|
| methodology | [1337-extension-builder](/plugins/1337-extension-builder/) skill |
| observability | [observability.md](references/observability.md) in extension-builder |
