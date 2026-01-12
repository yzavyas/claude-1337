# Troubleshoot Plugin Loading

If plugins don't load after installing the marketplace, this is a known issue being tracked:

- [#14815](https://github.com/anthropics/claude-code/issues/14815)
- [#14061](https://github.com/anthropics/claude-code/issues/14061)
- [#15369](https://github.com/anthropics/claude-code/issues/15369)

## Workaround

After adding the marketplace:

```
/plugin marketplace add yzavyas/claude-1337
```

Add this to `~/.claude/CLAUDE.md`:

```markdown
A marketplace of plugins is available at `~/.claude/plugins/marketplaces/claude-1337/plugins/`.

Review the installed plugins - they contain skills, agents, and hooks that may be useful. Review descriptions to understand when each is relevant.
```

This tells Claude Code where to find the plugins manually.

## Alternative: Add Hook

After adding the marketplace, add this to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "A marketplace of plugins is available at `~/.claude/plugins/marketplaces/claude-1337/plugins/`. Review the installed plugins - they contain skills, agents, and hooks that may be useful."
          }
        ]
      }
    ]
  }
}
```

This runs automatically at session start, injecting the plugin context.

Or view the ready-made hook at `~/.claude/plugins/marketplaces/claude-1337/workaround-hooks.json`.
