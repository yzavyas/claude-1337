---
description: Load JVM analysis patterns and profiling decisions
allowed-tools: Read(*), Grep(*), Glob(*)
---

## Context

- Plugin root: ${CLAUDE_PLUGIN_ROOT}

## Your task

Load the jvm-analysis-1337 skill:

1. Read `${CLAUDE_PLUGIN_ROOT}/SKILL.md` completely
2. Read relevant references from `${CLAUDE_PLUGIN_ROOT}/references/`
3. Apply JVM analysis patterns to the user's current task

This skill provides:
- Profiling tool decisions (async-profiler, JFR)
- GC analysis patterns
- Memory leak investigation
- Performance debugging workflows

Use these patterns for JVM analysis in this session.
