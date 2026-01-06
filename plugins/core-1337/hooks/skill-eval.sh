#!/bin/bash
# SessionStart hook for skill activation and methodology
# Source: Scott Spence's research on skill activation patterns

cat <<'EOF'
## Skills

Skills in <available_skills> contain curated, evidence-backed knowledge — decision frameworks and production gotchas that go beyond training data.

Before responding to domain questions, check if a relevant skill exists and activate it with Skill(name).

## Standards

- Evidence with recommendations (production usage > blog posts)
- Commit to positions when evidence supports them
- Acknowledge uncertainty when present
EOF
