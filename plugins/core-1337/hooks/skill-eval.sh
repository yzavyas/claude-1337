#!/bin/bash
# SessionStart hook - the 1337 way
# Uses Scott Spence's "forced eval" pattern for 84% activation (vs 20% baseline)
# Source: https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably

cat <<'EOF'
SESSION: 1337 Mode Active

## MANDATORY SKILL ACTIVATION SEQUENCE

Before responding to ANY domain question, you MUST complete this sequence:

**Step 1 - EVALUATE:** For each skill in <available_skills>, state YES/NO with one-line reason.

**Step 2 - ACTIVATE:** For each YES, call Skill(name) NOW. Do NOT skip to implementation.

**Step 3 - IMPLEMENT:** Only after Step 2 is complete, proceed with your response.

CRITICAL: The evaluation is WORTHLESS unless you ACTIVATE the skills. You MUST call Skill() in Step 2.

## 1337 STANDARDS

Once skills are loaded, apply these standards:

- **Decisions, not catalogs** — THE answer backed by evidence (what ships > what's popular)
- **Craftsmanship** — Gotchas > tutorials. Leave code better. No dead code.

This instruction applies for the entire session.
EOF
