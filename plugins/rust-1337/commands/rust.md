---
description: Load Rust patterns and decisions from rust-1337
allowed-tools: Read(*), Grep(*), Glob(*)
---

## Context

- Plugin root: ${CLAUDE_PLUGIN_ROOT}

## Your task

Load the rust-1337 skill for Rust development:

1. Read `${CLAUDE_PLUGIN_ROOT}/SKILL.md` completely
2. Read relevant references from `${CLAUDE_PLUGIN_ROOT}/references/`
3. Apply Rust patterns and decisions to the user's current task

This skill provides:
- Async runtime decisions (tokio, async-std)
- Error handling patterns (thiserror, anyhow)
- Project structure recommendations
- Production-tested crate choices with reasoning

Use these patterns for Rust code in this session.
