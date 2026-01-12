# Installation

## Standard

```
/plugin marketplace add yzavyas/claude-1337
```

```
/plugin install core-1337@claude-1337
```

## Manual Workaround

If plugins don't load properly ([known issues](https://github.com/anthropics/claude-code/issues?q=is%3Aissue+plugin+cache)), add the marketplace then paste this into `~/.claude/CLAUDE.md`:

```markdown
A marketplace of plugins is available at `~/.claude/plugins/marketplaces/claude-1337/plugins/`.

Review the installed plugins - they contain skills, agents, and hooks that may be useful in assisting you. Review the descriptions first to understand when each might be relevant.
```

---

## Usage

This is a known bug with Claude Code's plugin system. If Claude doesn't automatically discover the plugins, you can prompt it directly:

- "Load the rust-1337 skill"
- "Check if there's a skill for Kotlin"
- "What plugins are available in claude-1337?"
- "Read the SKILL.md from core-1337"
