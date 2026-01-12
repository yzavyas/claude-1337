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

Run the install script:

```bash
~/.claude/plugins/marketplaces/claude-1337/install-workaround.sh
```

This adds a session-start hook that tells Claude Code where to find the plugins.

## Manual Alternative

If you prefer not to run a script, add this to `~/.claude/CLAUDE.md`:

```markdown
A marketplace of plugins is available at `~/.claude/plugins/marketplaces/claude-1337/plugins/`.

Review the installed plugins - they contain skills, agents, and hooks that may be useful. Review descriptions to understand when each is relevant.
```
