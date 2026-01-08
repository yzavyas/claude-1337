# Extension Catalog

Five modalities for extending Claude Code.

| Type | What it extends | Use when |
|------|-----------------|----------|
| **skill** | What Claude knows | Adding domain knowledge, decision frameworks |
| **hook** | Session behavior | Event-triggered actions, validation gates |
| **agent** | Reasoning delegation | Specialized subprocesses, focused tasks |
| **command** | Repeatable workflows | Slash command shortcuts |
| **mcp** | External systems | API integrations, data sources |

## Skills

Knowledge that loads into Claude's context. Decision frameworks, production patterns, domain expertise.

See [plugins/](../../../plugins/) for available skills.

## Hooks

Scripts that run at lifecycle events. PreToolUse, PostToolUse, SessionStart, Stop.

Deterministic control — no LLM decision, guaranteed execution.

## Agents

Specialized subprocesses with separate context windows. Explorer, verifier, researcher, planner patterns.

Constraint: agents cannot spawn other agents.

## Commands

Slash command shortcuts that expand to prompts. `/commit`, `/review-pr`, workflow automation.

## MCP Servers

Model Context Protocol integrations. External APIs, databases, services.
