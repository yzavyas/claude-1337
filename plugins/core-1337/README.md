# core-1337

The foundation. Makes Claude operate the 1337 way.

## Install

```
/plugin install core-1337@claude-1337
```

Install this first, then add domain skills (rust-1337, terminal-1337, etc).

## What it does

Sets session-wide behavior at startup:

1. **Skill activation** - Claude checks `<available_skills>` before responding
2. **Decisions, not catalogs** - THE answer backed by evidence, not options
3. **Production mindset** - Gotchas over tutorials, what ships over what's popular

## Why this exists

Without intervention, skills activate ~20% of the time. With core-1337's evaluation hook, recall improves to ~84%.

**Note**: Higher recall may mean lower precision (more false activations). The smart eval approach balances both. See [/evals](../../evals/) for rigorous testing methodology.

More importantly, core-1337 establishes the philosophy: elite developer standards throughout the session.

## Technical

- Hook type: SessionStart
- Runs once per session
- Sets context for all subsequent interactions
