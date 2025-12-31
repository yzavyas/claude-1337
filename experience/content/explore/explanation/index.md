# explanation

understanding the skill activation problem

## the problem

claude code skills have a ~20% activation rate by default. you install a skill, ask a relevant question, and claude ignores it.

this is emergent behavior from how skills are surfaced.

## how skills work

skills appear in an `<available_skills>` block in claude's context:

```xml
<available_skills>
<skill>
  <name>terminal-1337</name>
  <description>modern cli tools...</description>
</skill>
...
</available_skills>
```

claude sees this but doesn't automatically:

1. evaluate each skill against the current request
2. decide which skills are relevant
3. activate them before responding

it just... responds. sometimes it notices skills, usually it doesn't.

## the research

scott spence documented this problem and found a fix:

> "skills don't trigger automatically - claude needs explicit instruction to evaluate them"

his forced evaluation prompt achieved 84% activation (4.2x improvement).

## our eval framework

we built an eval framework using claude agent sdk to measure activation rigorously:

```python
# rigorous evaluation uses labeled test cases
suite = TestSuite(
    name="rust-eval",
    skills=[
        SkillTestSpec(
            name="rust-1337",
            plugin="rust-1337",
            test_cases=[
                # should activate
                TestCase(prompt="what crate for cli args?", expectation="must_activate"),
                # should NOT activate
                TestCase(prompt="help me write python", expectation="should_not_activate"),
                # ambiguous
                TestCase(prompt="explain ownership", expectation="acceptable"),
            ]
        )
    ],
    negative_cases=[
        TestCase(prompt="write a haiku", expectation="should_not_activate"),
    ]
)

# measures precision (avoid false activations) AND recall (catch valid triggers)
report = await run_test_suite(suite, mode="baseline")
metrics = report.compute_metrics()
print(f"Precision: {metrics.precision}, Recall: {metrics.recall}, F1: {metrics.f1_score}")
```

**important:** raw activation rate is meaningless without measuring false positives. a system that activates on every prompt has 100% recall but 0% precision.

## the fix

add this to your system prompt:

```
When you receive a request that might benefit from specialized knowledge:

1. Check if you've already activated a relevant skill this session
2. If not, scan <available_skills> for matches and activate before responding
3. Skip re-evaluation for topics you've already covered
```

## why this works

the prompt forces explicit evaluation before response generation. claude checks skills once per topic rather than ignoring them entirely.

this is similar to chain-of-thought prompting — forcing the "should I use a skill?" step prevents Claude from skipping straight to answering.

## testing vs production

for testing activation rates, use the aggressive version:

```
Before responding to ANY request, you MUST evaluate skills...
```

for production, the per-topic version saves tokens while maintaining activation.

## tradeoffs

| aspect | baseline | smart eval | forced eval |
|--------|----------|------------|-------------|
| recall (catches triggers) | ~20% | ~70% | ~84% |
| precision (avoids noise) | high | medium | lower |
| token usage | baseline | +once per topic | +every message |

**recommendation:** use "smart eval" (per-topic) for production. forced eval inflates recall but may increase false activations.

## deeper explanations

- [ethos](ethos/) — cognitive extensions, extended mind thesis, Ba, methodology
- [concepts](concepts.md) — marketplace, plugins, skills, hooks, commands, agents, MCP, evals
- [models](models/) — how opus, sonnet, haiku work and when to use each
- [agents](agents/) — how autonomous task execution works
- [extensibility](extensibility/) — how to extend claude code with skills, hooks, agents, mcp
- [architecture](architecture/) — how the plugin system works
- [activation](activation/) — skill activation research in detail
- [autonomy](autonomy/) — collaborative intelligence and motivation

## sources

- [scott spence - claude code skills research](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably)
- [reddit - anatomy of a skill, tokenomics, truncation](https://www.reddit.com/r/ClaudeAI/comments/1pha74t/deep_dive_anatomy_of_a_skill_its_tokenomics_why/)
- [reddit - CLAUDE.md and skills experiment](https://www.reddit.com/r/ClaudeAI/comments/1pe37e3/claudemd_and_skills_experiment_whats_the_best_way/)
- our eval framework: `/evals` in the repo
