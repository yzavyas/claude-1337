#!/bin/bash
# SessionStart hook - runs once per session, not per message
# Based on Scott Spence's research: improves activation from 20% to 84%

cat <<'EOF'
SESSION INSTRUCTION: Skill Activation

When you receive a request that might benefit from specialized knowledge:

1. Check if you've already activated a relevant skill this session
2. If not, scan <available_skills> for matches and call Skill(name) BEFORE responding
3. Skip re-evaluation for topics you've already covered

This check happens once per topic, not every message.
EOF
