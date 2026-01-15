# LEP-001: Rigor is What You Want

> From [LEP-001](../../proposals/lep-001-rigor-is-what-you-want.md) | [IMP-001](../../implementations/imp-001-rigor-is-what-you-want.md)

## Hypothesis

Can methodology effectiveness be measured with hard data?

Specifically: Does iteration improve outcomes?

## Experiment Design

### Conditions

| Condition | Description |
|-----------|-------------|
| `single` | One API call, no iteration |
| `ralph-3` | Up to 3 iterations with self-review |
| `ralph-5` | Up to 5 iterations with self-review |

### Task

Write a Python function that checks if a string is a valid palindrome, ignoring case and non-alphanumeric characters.

### Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `correctness` | binary | Passes all 10 test cases |
| `iterations_used` | count | How many iterations until completion |
| `tokens_total` | count | Total tokens consumed |
| `success_rate` | ratio | Passes / total runs per condition |

## Run

```bash
# From experiment directory
uv run python -m lep_001_rigor_is_what_you_want

# Options
uv run python -m lep_001_rigor_is_what_you_want --runs 3      # Pilot (3 runs per condition)
uv run python -m lep_001_rigor_is_what_you_want --runs 5      # Full experiment
uv run python -m lep_001_rigor_is_what_you_want --dry-run     # Show config only
uv run python -m lep_001_rigor_is_what_you_want --condition single  # Run single condition only

# Or via lab CLI (from lab-1337/)
lab-1337 run lep-001-rigor-is-what-you-want
```

## Results

Results are written to `results/` as JSON files with timestamps.

View with:
```bash
lab-1337 results lep-001-rigor-is-what-you-want
```
