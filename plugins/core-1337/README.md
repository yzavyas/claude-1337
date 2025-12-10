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

Without core-1337, skills activate ~20% of the time. With it, ~84%.

More importantly, it establishes the philosophy: elite developer standards throughout the session.

## Technical

- Hook type: SessionStart
- Runs once per session
- Sets context for all subsequent interactions
