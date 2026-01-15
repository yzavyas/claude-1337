# LEP-001: Rigor is What You Want

(you just don't know it yet)

- **Status**: Draft
- **Created**: 2026-01-15
- **Authors**: Collaborative Intelligence Session

## Summary

Measure the effectiveness of spec-driven development frameworks (BMAD, GSD, spec-kit) compared to baseline Claude on coding tasks.

## Motivation

In the Agentic Era, talk is cheap. Everyone has opinions about what works:

- "BMAD is the best because it has 21 specialized agents"
- "GSD solves context rot"
- "spec-kit is from GitHub so it must be good"
- "Just vibe code, frameworks are overhead"

None of this is evidence. It's tribalism.

Meanwhile, decisions compound exponentially. Bad methodology choices scale with everything built on them. A team that adopts the wrong approach early bakes it into their entire stack.

The human condition works against us here:
- **Tribalism**: We defend what we've invested in
- **Constraints**: Decision makers lack information, builders lack time
- **Cognitive load**: Rigorous evaluation is hard; vibes are easy

But the cost of being wrong has never been higher.

## The Question

> Do spec-driven development frameworks improve outcomes over baseline Claude?

The spec-driven discourse assumes more structure = better outcomes. But there's reason to doubt:

1. Detailed specs may trigger compliance mode, not reasoning mode
2. Over-specification removes AI agency - mandate without motivation
3. The coordination cost of maintaining specs may exceed their benefit

This is testable. We should test it.

## Proposed Experiment

### Conditions

| Condition | Description |
|-----------|-------------|
| **baseline** | Pure Claude, no methodology |
| **spec-kit** | GitHub's 7-step process (Constitution→Implement) |
| **gsd** | Get Shit Done (PROJECT/ROADMAP/STATE/PLAN) |
| **bmad** | BMAD Method (21 agents, scale-adaptive) |

### Tasks

Stratified by complexity:

| Category | Example | Hypothesis |
|----------|---------|------------|
| Trivial | Fix typo | Methodology overhead hurts |
| Simple | Add endpoint | Minimal difference |
| Multi-step | Add auth flow | Methodologies may help |
| Architecture | Refactor service | Methodologies should help |
| Ambiguous | "Make it faster" | Clarification value |

### Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `pass@k` | completion | Task succeeds in k attempts |
| `pass^k` | reliability | Task succeeds in ALL k attempts |
| `code_quality` | LLM-judge | Maintainability, structure |
| `tokens_used` | efficiency | Cost |
| `recovery_rate` | robustness | Can it fix its mistakes? |

### Protocol

```
For each task T:
    For each methodology M in [baseline, speckit, gsd, bmad]:
        For run in range(5):  # Handle stochasticity
            1. Fresh environment (no leakage)
            2. Load methodology M as system prompt
            3. Execute task T
            4. Run test suite (ground truth)
            5. LLM-judge quality (blind to methodology)
            6. Record metrics
```

## Hypotheses

**H0** (null): Spec-driven frameworks produce equivalent outcomes to baseline.

**H1**: Spec-driven frameworks improve outcomes (higher pass@k, better quality).

**H2**: Spec-driven frameworks hurt outcomes (overhead costs exceed benefits).

**H3**: Effect is task-dependent (helps on complex, hurts on simple).

## Unresolved Questions

1. **Task selection**: Source from existing benchmarks (SWE-bench) or create custom?

2. **Methodology crystallization**: How to fairly represent each framework as a prompt?

3. **Generalizability**: Results may be model-specific. Run on multiple models?

4. **Cost**: Full experiment could be expensive. Start with pilot?

## Prior Art

- **SWE-bench**: Agent evaluation on real GitHub issues
- **HumanEval**: Code generation benchmarks
- **LMSYS Arena**: Model comparison via human preference

None of these specifically test development methodologies.

## Expected Outcome

One of:

1. **Spec-driven wins**: Structure helps, we learn which framework helps most
2. **Baseline wins**: Overhead hurts, keep it simple
3. **Context-dependent**: Different approaches for different task types

Any of these is valuable. The point is evidence, not vindication.

## References

- [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD)
- [Get Shit Done](https://github.com/glittercowboy/get-shit-done)
- [spec-kit](https://github.com/github/spec-kit)
- Feynman, R. "Cargo Cult Science" (1974)
