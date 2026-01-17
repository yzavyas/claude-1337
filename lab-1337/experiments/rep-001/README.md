# LEP-001: Rigor is What You Want

> From [LEP-001-Evals are non negotiable](LEP-001-Evals%20are%20non%20negotiable.md) | [IMP-001](../../implementations/imp-001-rigor-is-what-you-want.md)

## Hypothesis

**Primary**: Does iteration (Ralph-style self-review) improve outcomes?

**Secondary**: Can methodology effectiveness be measured with hard data?

## Experiment Design

### Conditions

| Condition | Description |
|-----------|-------------|
| `single` | One API call, no iteration |
| `ralph-3` | Up to 3 iterations with self-review |
| `ralph-5` | Up to 5 iterations with self-review |

### Task: Interval Merging

Merge overlapping intervals - a LeetCode medium problem with many edge cases:
- Overlapping intervals
- Adjacent intervals (e.g., [1,2] and [2,3])
- Unsorted input
- Negative numbers
- Empty/single element cases

**Why this task**: Single-shot often misses edge cases that review would catch.

### Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `correctness` | binary | Passes all 20 test cases |
| `iterations_used` | count | How many iterations until completion |
| `tokens_total` | count | Total tokens consumed |
| `success_rate` | ratio | Passes / total runs per condition |

### Observability

OTel instrumentation included for transparency:
- `experiment_run` span per condition/run
- `llm_call` span per API call
- `evaluation` span for ground truth verification

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
