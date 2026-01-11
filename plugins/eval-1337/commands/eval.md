---
description: Load skill evaluation methodology from eval-1337
allowed-tools: Read(*), Grep(*), Glob(*)
---

## Context

- Plugin root: ${CLAUDE_PLUGIN_ROOT}

## Your task

Load the eval-1337 skill for testing and evaluation:

1. Read `${CLAUDE_PLUGIN_ROOT}/SKILL.md` completely
2. Read relevant references from `${CLAUDE_PLUGIN_ROOT}/references/`
3. Apply evaluation methodology to the user's current task

This skill provides:
- Skill activation testing patterns
- Prompt injection testing
- Activation measurement methodology
- Evidence-based skill improvement

Use these patterns for evaluating skills in this session.
