# LEP-001: Rigor is What You Want

(you just don't know it yet)

- **Status**: Draft
- **Created**: 2026-01-15
- **Authors**: Collaborative Intelligence Session

## Summary

Establish a rigorous experimental framework for comparing development methodologies in the agentic era. First experiment: spec-driven development frameworks (BMAD, GSD, spec-kit) vs collaborative intelligence vs baseline Claude.

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

## The Hypothesis

The spec-driven development discourse assumes more structure = better outcomes. But there's a counter-hypothesis:

**H1**: Collaborative intelligence (understand → discourse → agency) outperforms spec-driven approaches because:

1. Detailed specs trigger compliance mode, not reasoning mode
2. Over-specification removes AI agency - mandate without motivation
3. The coordination cost of maintaining specs exceeds their benefit

This is testable. We should test it.

## Proposed Experiment: Methodology Comparison

### Conditions

| Condition | Description |
|-----------|-------------|
| **baseline** | Pure Claude, no methodology |
| **spec-kit** | GitHub's 7-step process |
| **gsd** | Get Shit Done context engineering |
| **bmad** | 21 agents, scale-adaptive workflows |
| **collaborative** | Understand → discourse → agency pattern |

### Tasks

Stratified by complexity and type:

| Category | Example | Why It Matters |
|----------|---------|----------------|
| Trivial fix | Fix typo | Methodology overhead should hurt |
| Simple feature | Add endpoint | Baseline competence |
| Complex feature | Add auth flow | Planning depth |
| Refactoring | Extract service | Architectural thinking |
| Ambiguous | "Make it faster" | Clarification value |

### Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `pass@k` | completion | Does it work? (test suite) |
| `pass^k` | reliability | Does it work every time? |
| `code_quality` | LLM-judge | Maintainability, structure |
| `tokens_used` | efficiency | Cost |
| `recovery_rate` | robustness | Can it fix its mistakes? |

### Protocol

```
For each task T:
    For each methodology M:
        For run in range(5):  # Handle stochasticity
            1. Fresh environment (no leakage)
            2. Load methodology M
            3. Execute task T
            4. Run test suite (ground truth)
            5. LLM-judge quality (blind to methodology)
            6. Record metrics
```

## Unresolved Questions

1. **How to load "collaborative intelligence" as a methodology?** It's a process, not a prompt. May need different experimental design.

2. **Task selection**: Which specific tasks? Need to avoid cherry-picking. Possibly source from SWE-bench or similar.

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
3. **Collaborative wins**: Agency matters, structure beyond a point hurts
4. **Context-dependent**: Different approaches for different task types

Any of these is valuable. The point is evidence, not vindication.

## References

- [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD)
- [Get Shit Done](https://github.com/glittercowboy/get-shit-done)
- [spec-kit](https://github.com/github/spec-kit)
- [Ralph Wiggum Technique](https://awesomeclaude.ai/ralph-wiggum)
- Feynman, R. "Cargo Cult Science" (1974)
