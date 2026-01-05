[&larr; reference](../../reference/)

# research

<p class="dimmed-intro">skill activation studies and the claude-1337 validation framework</p>

## the activation problem

claude code skills have a ~20% baseline activation rate. you install a skill, ask a relevant question, and claude ignores it 80% of the time.

### root cause

from [lee han chung's deep dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/):

- **no algorithmic routing** - no regex, no embeddings, no classifiers
- **pure LLM reasoning** - claude reads skill descriptions and decides
- **description is everything** - the only signal for matching

problem: claude sees the skills but doesn't automatically evaluate them against your request. it responds without checking if a skill would help.

## the forced evaluation study

from [scott spence's 200+ test study](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably):

| approach | activation rate | notes |
|----------|----------------|-------|
| no intervention (baseline) | ~20% | default behavior |
| simple instruction | ~20% | doesn't help |
| LLM eval hook | 80% | asks claude to evaluate |
| forced eval hook | **84%** | explicit skill checking |

### the fix

explicit evaluation prompts that force claude to check skills before responding. this is what core-1337's SessionStart hook implements.

```
Before responding:
1. Check if any skills in <available_skills> are relevant
2. If relevant, invoke the Skill tool
3. Then respond using that knowledge
```

## validation framework

the claude-1337 eval framework validates activation rates by observing actual tool invocation, not asking claude's opinion.

### methodology

tests send prompts through the claude agent sdk and monitor the response stream for `ToolUseBlock` with `name == "Skill"`. this is observed tool invocation (what Claude actually did, not what it claims) - did claude actually invoke the skill?

```python
async for message in query(prompt=prompt, options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                if block.name == "Skill":
                    skill_called = True  # ground truth
```

### test suite format

```json
{"name": "claude-1337-skills",
  "description": "test activation of marketplace skills",
  "skills": [
    {"name": "terminal-1337",
      "plugin": "terminal-1337",
      "expected_triggers": [
        "how do i search for a pattern in my codebase?",
        "what's a fast way to find files by name?"
      ]
    }
  ],
  "runs_per_prompt": 3
}
```

### interpreting results

| activation rate | meaning |
|----------------|---------|
| 80%+ | skill description is working well |
| 50-79% | description needs improvement |
| &lt;50% | description likely missing "use when:" or too vague |

## running tests

### installation

```
cd evals
uv sync
```

*note: tested with claude code subscription (max plan). api testing status documented in [evals/README.md](https://github.com/yzavyas/claude-1337/tree/main/evals)*

### single test

```
uv run skill-test test "how do i search for a pattern?" -s terminal-1337 -n 3
```

### run test suite

```
# create sample suite
uv run skill-test init-suite sample-suite.json

# run suite
uv run skill-test suite sample-suite.json -o report.md
```

## what makes skills activate

patterns that improve activation rates:

| pattern | why it works |
|---------|-------------|
| "use when:" clause | explicit trigger conditions |
| specific tools/terms | "axum, tonic, sqlx" not "backend" |
| action verbs | "building", "debugging", "configuring" |
| front-loaded keywords | claude matches against description |

## sources

- [anthropic: equipping agents with skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) - official documentation
- [scott spence: skills activation study](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably) - 200+ test validation of forced eval pattern
- [lee han chung: skills deep dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) - how skill routing actually works
- [deep dive: anatomy of a skill](https://www.reddit.com/r/ClaudeAI/comments/1pha74t/deep_dive_anatomy_of_a_skill_its_tokenomics_why/) - tokenomics and available_skills budget
- [CLAUDE.md and skills experiment](https://www.reddit.com/r/ClaudeAI/comments/1pe37e3/claudemd_and_skills_experiment_whats_the_best_way/) - optimal knowledge distribution patterns

## structure

```
evals/
├── .env.example              # api key template
├── main.py                   # cli entry point
├── pyproject.toml            # uv project config
├── README.md                 # detailed documentation
├── sample-suite.json         # example test suite
├── src/
│   ├── cli.py               # command interface
│   ├── runner.py            # test execution
│   └── report.py            # markdown generation
└── uv.lock                  # dependency lock
```

[view evals/ on github](https://github.com/yzavyas/claude-1337/tree/main/evals)
