# how-to

task-oriented guides for common goals

## install the marketplace

```
/plugin marketplace add yzavyas/claude-1337
```

then install specific plugins:

```
/plugin install terminal-1337@claude-1337
```

## improve skill activation

skills activate ~20% by default. add this system prompt:

```
When you receive a request that might benefit from specialized knowledge:

1. Check if you've already activated a relevant skill this session
2. If not, scan <available_skills> for matches and activate before responding
3. Skip re-evaluation for topics you've already covered
```

**note:** this is per-topic, not per-message. the "MUST evaluate every request" version works for testing but wastes tokens in production.

for hooks-based approach, create `.claude/hooks/skill-eval.sh`:

```bash
#!/bin/bash
cat <<'EOF'
INSTRUCTION: If you haven't already for this topic, scan <available_skills>
and activate relevant skills before responding.
EOF
```

## use with agent sdk

load plugins directly in python:

```python
from claude_agent_sdk import ClaudeAgentOptions, query

options = ClaudeAgentOptions(
    plugins=[
        {"type": "local", "path": "./plugins/terminal-1337"},
    ],
    system_prompt=FORCED_EVAL_PROMPT,
)
```

note: each plugin needs its own path, not the marketplace root.

## check skill budget

skills truncate at ~20-22k chars. to check:

```
"how many skills in your <available_skills> block?"
```

truncated skills don't trigger - claude can't see them.

## write a 1337 skill

install the skill creator:

```
/plugin install 1337-extension-builder@claude-1337
```

**don't read process docs. run prompts.**

1. test claude's knowledge, find gaps
2. research 3 production codebases
3. verify with maintainer quotes
4. collect production gotchas
5. fill in SKILL.md template
6. run validation checks

key rules:

- fill gaps (what Claude doesn't already know)
- cite evidence (production codebases > stars)
- decisions, not tutorials
- use tables, not prose

see [1337-extension-builder reference](../reference/1337-extension-builder/) for executable prompts.

## test skill activation

validate that your skills actually activate when they should.

### setup

```
cd evals
uv sync
```

### run a single test

```
uv run skill-test test "how do i search files?" -s terminal-1337 -n 3
```

this sends the prompt 3 times and checks if terminal-1337 skill gets invoked.

### run a test suite

```bash
# create test suite
uv run skill-test init-suite my-tests.json

# edit my-tests.json to add prompts for your skills

# run suite
uv run skill-test suite my-tests.json -o report.md
```

### interpret results

| activation rate | action |
|-----------------|--------|
| 80%+ | skill description is good |
| 50-79% | improve description, add "use when:" clause |
| <50% | description too vague, front-load keywords |

see [research reference](../reference/research.md) for validation methodology and detailed docs.
