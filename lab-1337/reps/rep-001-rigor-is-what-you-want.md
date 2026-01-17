# REP-001: Rigor is What You Want

- **Status**: Implemented
- **Created**: 2026-01-15
- **Authors**: Collaborative Intelligence Session
- **Tracking**: [Findings](../findings/rep-001-findings.md)

## Summary

Establish rigorous evaluation as the standard practice for methodology decisions in AI work. Apply the scientific method — hypothesis, experiment, evidence, decision — instead of vibes and tribal preferences.

## Motivation

Everyone has opinions about what works:
- "Iteration improves output quality"
- "Single-shot is fine, process is overhead"
- "Just vibe code, structure is bureaucracy"

None of this is evidence. Decisions compound exponentially — bad methodology choices bake into everything built on them. The cost of being wrong has never been higher, yet most methodology debates are tribal, not empirical.

We need a way to produce hard data about what actually works.

## Guide-level explanation

When facing a methodology question ("Does X improve outcomes?"), follow this process:

1. **Hypothesis** — State a clear, falsifiable claim
2. **Experiment** — Design controlled conditions with ground truth
3. **Metrics** — Define what we measure and how
4. **Analysis** — Let the data speak
5. **Decision** — Act on evidence, not preference

This LEP validates the approach by testing a simple question: *Does iteration improve outcomes?*

## Reference-level explanation

### Experiment Design

**Question**: Does iteration (Ralph-style self-review) improve code generation outcomes?

**Benchmark**: HumanEval (164 Python coding problems)
- Ground truth via test suites
- Varied difficulty
- Standard, comparable benchmark

**Conditions**:
| Strategy | Description |
|----------|-------------|
| Single-shot | One attempt, submit result |
| Ralph-style | Up to 3 iterations with test feedback |

**Metrics**:
- Pass rate (binary correctness)
- Token consumption
- Iterations used

### Results (Full HumanEval, 164 problems, Haiku)

| Strategy | Pass Rate | Avg Tokens | Multiplier |
|----------|-----------|------------|------------|
| Single-shot | 86.6% (142/164) | 232 | 1x |
| Ralph-style | 98.8% (162/164) | 2,264 | ~10x |

Iteration recovered 20 of 22 failures. Two problems remained unsolved — the model's capability ceiling. Pattern consistent across problem difficulty ranges.

## Drawbacks

- **Cost**: Running experiments costs API tokens and time
- **Scope**: Results may not generalize beyond the tested benchmark
- **Complexity**: Requires infrastructure for reproducible experiments

## Rationale and alternatives

**Why this approach?**
- Scientific method is proven over centuries
- Falsifiable hypotheses prevent self-deception
- Quantitative data enables objective comparison

**Alternatives considered**:
- *Expert opinion* — Subject to bias, not reproducible
- *Case studies* — Anecdotal, not systematic
- *A/B testing in production* — Expensive, slow feedback

**Impact of not doing this**: Methodology debates remain tribal. Decisions made on vibes compound into scaled mistakes.

## Prior art

| Work | Relevance |
|------|-----------|
| **HumanEval** (OpenAI) | Code generation benchmark we build on |
| **SWE-bench** (Princeton) | Real-world agent evaluation |
| **LMSYS Arena** | Model comparison methodology |
| **Rust RFCs** | Proposal process we adapt |

## Unresolved questions

- Does the pattern hold for other models (Sonnet, Opus)?
- Does it hold for non-coding tasks?
- What's the optimal iteration limit before diminishing returns?

## Future possibilities

With validated measurement infrastructure:
- **REP-002**: Spec-driven frameworks vs baseline
- **REP-003**: Prompt engineering patterns
- **REP-004**: Agent architectures (ReAct, CoT, etc.)
- **REP-005**: Multi-agent coordination patterns

Each builds on proven methodology.
