# Scripts Directory

**DEPRECATED**: This directory is intentionally empty.

## Everything is a Plugin

All functionality in claude-1337 MUST be a plugin. No standalone scripts.

**Why**:
- Users can install and use functionality directly
- Dogfooding: we use our own plugins
- Consistency: one way to package functionality
- Discoverability: everything is in the marketplace

**Before**: `scripts/curator-1337/` (standalone automation)

**Now**: `plugins/curator-1337/` (plugin with agent + GHA wrapper)

## Migration

If you need to add functionality:
1. Create a plugin in `plugins/`
2. Include an agent if appropriate
3. GHA workflows can invoke plugin agents
4. Users can also invoke the agent directly

See `CLAUDE.md` for the "Everything is a Plugin" architecture principle.
