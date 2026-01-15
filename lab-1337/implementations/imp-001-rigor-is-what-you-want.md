# IMP-001: Rigor is What You Want

- **Status**: Draft
- **LEP**: [LEP-001](../proposals/lep-001-rigor-is-what-you-want.md)
- **Created**: 2026-01-15
- **Authors**: Collaborative Intelligence Session

## Overview

Implementation plan for proving methodology effectiveness is measurable via the Ralph Iteration Effect experiment.

## Design

### Experimental Conditions

| Condition | Description |
|-----------|-------------|
| `single` | One API call, no iteration |
| `ralph-3` | Up to 3 iterations with self-review |
| `ralph-5` | Up to 5 iterations with self-review |

### Task

Palindrome checker - simple, verifiable, fair.

```python
def is_palindrome(s: str) -> bool:
    """Check if string is palindrome, ignoring case and non-alphanumeric."""
    ...
```

### Test Suite (Ground Truth)

```python
TEST_CASES = [
    ("A man, a plan, a canal: Panama", True),
    ("race a car", False),
    ("Was it a car or a cat I saw?", True),
    ("", True),
    ("a", True),
    ("ab", False),
    ("Madam", True),
    ("No 'x' in Nixon", True),
    ("hello", False),
    ("12321", True),
]
```

### Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `correctness` | binary | Passes all 10 test cases |
| `iterations_used` | count | How many iterations until completion/exit |
| `tokens_total` | count | Total tokens across all iterations |
| `success_rate` | ratio | Passes / total runs per condition |

### Architecture

```
experiments/ralph-iteration-effect/
├── src/ralph_iteration_effect/
│   ├── __init__.py
│   ├── __main__.py       # CLI entrypoint
│   └── experiment.py     # Core experiment logic
├── results/              # Output JSON files
├── pyproject.toml
└── README.md
```

## Implementation

### Phase 1: Infrastructure (Done)

- [x] Create experiment package structure
- [x] Implement single-shot runner
- [x] Implement ralph-style iteration runner
- [x] Add test suite for verification
- [x] CLI with progress display

### Phase 2: Execution

- [ ] Run pilot (3 runs per condition) - verify metrics collection
- [ ] Run full experiment (5+ runs per condition)
- [ ] Collect results JSON

### Phase 3: Analysis

- [ ] Calculate success rates per condition
- [ ] Compare token costs
- [ ] Statistical significance (if sample size allows)
- [ ] Generate summary report

### Phase 4: Publication

- [ ] Write findings document
- [ ] Update LEP-001 status to implemented
- [ ] Publish to results/

## Running the Experiment

```bash
# From lab-1337 directory
cd experiments/ralph-iteration-effect

# Dry run (show config)
uv run python -m ralph_iteration_effect --dry-run

# Pilot (3 runs)
uv run python -m ralph_iteration_effect --runs 3

# Full experiment (5 runs)
uv run python -m ralph_iteration_effect --runs 5 -o results/full-run.json
```

## Dependencies

- `anthropic` - Claude API
- `pydantic` - Data models
- `rich` - CLI output
- `click` - CLI framework

## Risks

| Risk | Mitigation |
|------|------------|
| API rate limits | Add retry logic, space requests |
| Cost overrun | Start with pilot, estimate full cost |
| Model stochasticity | Multiple runs (5+) per condition |
| Task too easy | If 100% pass rate, task doesn't discriminate |

## Success Criteria

The experiment succeeds if we observe **measurable difference** between conditions:
- Success rate varies by condition, OR
- Token cost varies meaningfully, OR
- Clear "no difference" finding (also valuable)

Failure = inconclusive data that doesn't inform methodology choices.

## Open Questions

1. **Sample size**: Is 5 runs enough for statistical confidence?
2. **Task difficulty**: If single-shot hits 100%, does iteration matter?
3. **Model choice**: Run on Sonnet only, or also Haiku to check generalization?
