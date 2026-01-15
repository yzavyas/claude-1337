# LEP-001 Findings: Ralph Iteration Effect

**Date**: 2026-01-15
**Status**: Complete
**Experiment**: [lep-001-rigor-is-what-you-want](../experiments/lep-001-rigor-is-what-you-want/)

## Summary

**Primary finding**: Methodology effectiveness CAN be measured with hard data.

**Secondary finding**: For simple, well-defined tasks within model capability, iteration provides no correctness benefit while increasing token cost ~2x.

## Results

### Success Rates

| Condition | Success Rate | Runs |
|-----------|-------------|------|
| single | 100% | 5/5 |
| ralph-3 | 100% | 5/5 |
| ralph-5 | 100% | 5/5 |

### Resource Usage

| Condition | Avg Tokens | Avg Iterations | Total Cost |
|-----------|-----------|----------------|------------|
| single | 181 | 1.0 | $0.28 |
| ralph-3 | 378 | 1.4 | $0.31 |
| ralph-5 | 385 | 1.8 | $0.31 |

### Key Observations

1. **Ceiling effect**: All conditions achieved 100% correctness
2. **Token overhead**: Ralph conditions use ~2x tokens (378-385 vs 181)
3. **Unnecessary iterations**: Ralph conditions sometimes iterate (1.4-1.8 avg) even when initial code is correct
4. **Consistent output**: Single-shot produces identical token counts (181) across all runs

## Hypothesis Evaluation

| Hypothesis | Result |
|------------|--------|
| **H0** (null): Iteration = single-shot | **Supported for correctness** - no difference in success rate |
| **H1**: Iteration improves outcomes | **Not supported** for this task |
| **H2**: Iteration wastes resources | **Partially supported** - more tokens, same success |
| **H3**: Iteration helps as recovery | **Not testable** - no failures to recover from |

## Interpretation

### What This Proves

1. **Measurement is possible**: We can reliably measure methodology differences
2. **Reproducible results**: Token counts are consistent within conditions
3. **Clear metrics**: Correctness, token usage, iteration count all measurable

### What This Does NOT Prove

1. That iteration never helps (task may be too easy)
2. That single-shot is always sufficient (harder tasks may differ)
3. That ralph-style iteration is fundamentally flawed

### Task Difficulty Analysis

The palindrome task exhibits a **ceiling effect**:
- Well-defined requirements
- Clear success criteria
- Within model's reliable capability
- No ambiguity in specifications

This makes it unsuitable for measuring methodology effectiveness differences, but excellent for validating the measurement infrastructure.

## Recommendations

### For LEP-002 (Future Work)

1. **Harder tasks**: Use tasks with <100% single-shot success rate
2. **Ambiguous requirements**: Test methodology impact on underspecified problems
3. **Multi-file tasks**: Where iteration might help with coordination
4. **Error-prone domains**: Where single-shot is known to fail sometimes

### Suggested Task Properties

| Property | Why |
|----------|-----|
| 60-80% single-shot success | Room for iteration to help |
| Multiple edge cases | Where review catches mistakes |
| Ambiguous requirements | Where iteration refines understanding |
| Complex dependencies | Where single-shot misses interactions |

## Raw Data

- **Pilot run**: [pilot-run.json](../experiments/lep-001-rigor-is-what-you-want/results/pilot-run.json)
- **Full run**: [full-run.json](../experiments/lep-001-rigor-is-what-you-want/results/full-run.json)

## Conclusion

**LEP-001 succeeds**: We proved that methodology effectiveness can be measured.

The experiment infrastructure works. The finding that iteration doesn't help on simple tasks is itself valuable evidence. Future experiments should use harder tasks to explore where iteration actually provides benefit.

---

*Experimental methodology validated. Ready for LEP-002.*
