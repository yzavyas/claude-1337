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

## Alternative: Copy Hook

After adding the marketplace, copy the workaround hook to your settings:

```bash
cp ~/.claude/plugins/marketplaces/claude-1337/workaround-hooks.json ~/.claude/settings.json
```

This adds a session-start hook that injects the plugin context automatically.

**Note:** If you already have a `settings.json`, merge the hooks section manually.
