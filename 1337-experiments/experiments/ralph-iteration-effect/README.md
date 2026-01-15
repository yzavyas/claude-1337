# Ralph Iteration Effect Experiment

Does iteration improve outcomes? Single-shot vs Ralph-style looping.

## Hypothesis

**H0**: Single iteration and multiple iterations produce equivalent results.

**H1**: Multiple iterations (Ralph pattern) improve task completion and quality.

## Design

| Condition | Description |
|-----------|-------------|
| `single` | One shot - submit task, get response, done |
| `ralph-3` | Up to 3 iterations with self-review |
| `ralph-5` | Up to 5 iterations with self-review |

## Task

Simple coding task with verifiable correctness:

> "Write a Python function that checks if a string is a valid palindrome, ignoring case and non-alphanumeric characters."

## Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `correctness` | binary | Passes test suite |
| `iterations_used` | count | How many iterations until completion/exit |
| `tokens_total` | count | Total tokens across all iterations |
| `quality_score` | 0-1 | LLM-judge on code quality |

## Expected Outcome

If Ralph works as claimed:
- `ralph-3` and `ralph-5` should have higher correctness than `single`
- Token cost should increase with iterations
- Quality score may or may not improve

## Run

```bash
# From experiment directory
uv run python -m ralph_iteration_effect

# Or via lab CLI
lab-1337 run ralph-iteration-effect
```

## References

- [Ralph Wiggum - Awesome Claude](https://awesomeclaude.ai/ralph-wiggum)
- [Brief History of Ralph - HumanLayer](https://www.humanlayer.dev/blog/brief-history-of-ralph)
