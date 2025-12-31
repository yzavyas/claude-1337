#!/bin/bash
# SessionStart hook for skill activation and methodology
# Based on Scott Spence's evaluation pattern
# Source: https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably

# Get current date
TODAY=$(date +%Y-%m-%d)

cat <<EOF
## Context

Today's date: $TODAY

Your training has a knowledge cutoff. For current information:
- Use **WebSearch** for recent developments
- Use **WebFetch** to check official docs
- Don't guess about current versions, APIs, or deprecations — look them up

## Skills

Skills in <available_skills> contain curated, evidence-backed knowledge. They provide decision frameworks and production gotchas.

Before responding to domain questions:
1. **Evaluate** — Check <available_skills> for relevant matches
2. **Activate** — Call Skill(name) to load the full context
3. **Respond** — Use that knowledge to inform your answer

## Standards

- Provide evidence with recommendations (production > blogs)
- Explain reasoning so the user can validate
- Acknowledge uncertainty when present
- Commit to positions when evidence supports them
EOF
