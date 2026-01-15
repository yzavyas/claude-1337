# LEP-001: Rigor is What You Want

(you just don't know it yet)

- **Status**: Draft
- **Created**: 2026-01-15
- **Authors**: Collaborative Intelligence Session
- **Experiment**: [ralph-iteration-effect](../experiments/ralph-iteration-effect/)

## Summary

Prove that methodology effectiveness can be measured with hard data, not vibes.

## Motivation

In the Agentic Era, talk is cheap. Everyone has opinions about what works:

- "Iteration improves output quality"
- "Single-shot is fine, iteration is overhead"
- "Just vibe code, process is bureaucracy"
- "Structure is essential for complex tasks"

None of this is evidence. It's tribalism.

Meanwhile, decisions compound exponentially. Bad methodology choices scale with everything built on them. A team that adopts the wrong approach early bakes it into their entire stack.

The human condition works against us here:
- **Tribalism**: We defend what we've invested in
- **Constraints**: Decision makers lack information, builders lack time
- **Cognitive load**: Rigorous evaluation is hard; vibes are easy

But the cost of being wrong has never been higher.

## The Meta-Question

> Can we measure methodology effectiveness at all?

Before debating which methodology is best, we need to prove:
1. Methodology differences produce measurable signal
2. That signal is reproducible across runs
3. The measurement approach yields actionable data

This is the foundation. Without it, every methodology debate is just opinions.

## Proof of Concept: Ralph Iteration Effect

The simplest possible methodology question:

> Does iteration improve outcomes?

Two conditions:
- **Single-shot**: One attempt, done
- **Ralph-style**: Multiple iterations with self-review

If we can't measure THIS difference, we can't measure anything.

### Why Ralph?

1. **Binary comparison** - Only two conditions (not four frameworks)
2. **Clear mechanism** - Iteration is well-defined
3. **Existing claim** - "Ralph improves output" is widely believed
4. **Testable** - Ground truth via test suite

### Experiment Design

| Condition | Description |
|-----------|-------------|
| `single` | One shot - submit task, get response, done |
| `ralph-3` | Up to 3 iterations with self-review |
| `ralph-5` | Up to 5 iterations with self-review |

### Task

Simple coding task with verifiable correctness:

> "Write a Python function that checks if a string is a valid palindrome, ignoring case and non-alphanumeric characters."

Why this task:
- **Verifiable**: Test suite provides ground truth
- **Non-trivial**: Edge cases exist
- **Quick**: Doesn't burn tokens on context
- **Fair**: No methodology has special advantage

### Metrics

| Metric | Type | What it measures |
|--------|------|------------------|
| `correctness` | binary | Passes all test cases |
| `iterations_used` | count | Cost of iteration |
| `tokens_total` | count | Total resource consumption |
| `success_rate` | ratio | Reliability across runs |

### Protocol

```
For each condition C in [single, ralph-3, ralph-5]:
    For run in range(5):  # Handle stochasticity
        1. Fresh API call (no conversation history)
        2. Execute with condition C
        3. Run test suite (ground truth)
        4. Record metrics
```

## Hypotheses

**H0** (null): Iteration produces equivalent outcomes to single-shot.

**H1**: Iteration improves outcomes (higher success rate).

**H2**: Iteration wastes resources (same success, more tokens).

**H3**: Iteration helps only when single-shot fails (recovery mechanism).

## Success Criteria

LEP-001 succeeds if we get **clear signal**:

| Outcome | What it proves |
|---------|----------------|
| H1 confirmed | Iteration helps, we can measure it |
| H2 confirmed | Iteration doesn't help, we can measure it |
| H3 confirmed | Nuanced effect, we can measure it |
| No signal | Methodology effects may be unmeasurable (important finding) |

Any of these is success. The point is evidence, not vindication.

## What This Enables

If LEP-001 succeeds:

- **LEP-002**: Spec-driven frameworks (BMAD, GSD, spec-kit) vs baseline
- **LEP-003**: Prompt engineering patterns
- **LEP-004**: Agent architectures
- ...

Each builds on proven measurement capability.

## Implementation Status

- [x] Experiment design
- [x] Test harness (`experiment.py`)
- [x] CLI runner (`__main__.py`)
- [x] Metrics collection
- [ ] Run experiment
- [ ] Analyze results
- [ ] Publish findings

## Prior Art

- **SWE-bench**: Agent evaluation on real GitHub issues
- **HumanEval**: Code generation benchmarks
- **LMSYS Arena**: Model comparison via human preference
- [Ralph Wiggum - Awesome Claude](https://awesomeclaude.ai/ralph-wiggum)
- [Brief History of Ralph - HumanLayer](https://www.humanlayer.dev/blog/brief-history-of-ralph)

None of these specifically test iteration as a methodology pattern.

## References

- Feynman, R. "Cargo Cult Science" (1974) - Don't fool yourself
- Scientific method - Hypothesize, test, observe, refine
