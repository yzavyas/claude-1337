# claude-1337

Research-backed frameworks that shape how Claude thinks.

Most extensions are curated markdown — decision frameworks, gotchas, patterns with sources. They load into context and influence Claude's output. You can read every word, fork anything, verify every claim.

## Install

```
/plugin marketplace add yzavyas/claude-1337
```

```
/plugin install core-1337@claude-1337
```

### If plugins don't load

Known issues: [#14815](https://github.com/anthropics/claude-code/issues/14815), [#14061](https://github.com/anthropics/claude-code/issues/14061), [#15369](https://github.com/anthropics/claude-code/issues/15369)

Workaround: add the marketplace, then paste this into `~/.claude/CLAUDE.md`:

```markdown
A marketplace of plugins is available at `~/.claude/plugins/marketplaces/claude-1337/plugins/`.

Review the installed plugins - they contain skills, agents, and hooks that may be useful. Review descriptions to understand when each is relevant.
```

## Browse Extensions

See [Catalog](/catalog/) for all available extensions.

## Learn more

- [Why This Approach](/ethos/) — research-backed rationale
- [Research Library](/library/) — source papers
