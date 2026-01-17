# REP-002: Mandates vs Motivations

- **Status**: Draft
- **Created**: 2026-01-16
- **Authors**: Collaborative Intelligence Session
- **Builds on**: [REP-001](rep-001-rigor-is-what-you-want.md)

## Summary

Test whether motivation-based prompting produces different outcomes than mandate-based prompting in agentic systems. The hypothesis: the mental model we use for AI (algorithm runner vs reasoning agent) may affect results.

## Motivation

REP-001 established that methodology effectiveness is measurable. This REP applies that capability to a foundational question about how we interact with AI.

### The Algorithm Runner Mental Model

We're conditioned to treat "thinking machines" as algorithm runners:
- Input → deterministic process → output
- Specify exactly what to do
- More detail = more control = better outcomes

This mental model shaped spec-driven frameworks:
- BMAD: 21 specialized agents with detailed role specifications
- GSD: Rigid file structure (PROJECT/ROADMAP/STATE/PLAN)
- spec-kit: 7-step process (Constitution → Implement)

The assumption: Claude is a sophisticated algorithm. Tell it exactly what to do.

### The Constitutional AI Model

Claude is trained differently. Constitutional AI uses values, not rules.

Research on Constitutional AI (Anthropic 2022) shows:
- Values-based training produces understanding and judgment
- Rule-based constraints produce compliance and brittleness

This suggests a different interaction model might be effective:
- Explain WHY, not just WHAT
- Principles that generalize, not specs that enumerate
- Agency retained, not removed

### The Uncertainty

We don't know which model produces better outcomes. Both have plausible arguments:

**For mandate-based (spec-driven):**
- Removes ambiguity
- Consistent structure
- Explicit expectations
- Works for traditional software

**For motivation-based (principles-driven):**
- Enables judgment
- Handles edge cases
- Adapts to context
- Aligns with Constitutional AI design

The discourse is tribal. This is testable.

## The Question

> Does the interaction model (mandate vs motivation) affect outcomes?

**Operationalized:**
- **Mandate**: Detailed specification of steps, format, structure
- **Motivation**: Principles, goals, reasoning for why approach matters

## Proposed Experiment

### Conditions

| Condition | Type | Description |
|-----------|------|-------------|
| **baseline** | Control | Pure Claude, no methodology |
| **spec-kit** | Mandate | GitHub's 7-step process |
| **gsd** | Mandate | Rigid file structure, explicit state |
| **bmad** | Mandate | 21 specialized agents |
| **principles** | Motivation | core-1337 style (why over what) |
| **hybrid** | Mixed | Principles + minimal structure |

### Task Stratification

Different task types may favor different approaches:

| Category | Example | Notes |
|----------|---------|-------|
| Algorithmic | Implement merge sort | Clear spec, deterministic |
| Multi-step | Add authentication flow | Multiple components, integration |
| Ambiguous | "Make it faster" | Requires interpretation |
| Recovery | Fix failing tests | Diagnosis + correction |
| Edge cases | Handle malformed input | Unspecified scenarios |

### Metrics

| Metric | What it measures |
|--------|------------------|
| `pass@k` | Task completion in k attempts |
| `recovery_rate` | Ability to fix own mistakes |
| `edge_case_handling` | Handles unspecified situations |
| `tokens_used` | Efficiency |
| `code_quality` | LLM-as-judge (blind to condition) |

### Key Measurement: Ambiguity Response

When tasks are underspecified:
- Does mandate approach fail or ask for clarification?
- Does motivation approach infer reasonable behavior?

Design tasks with intentional ambiguity to test this.

## Hypotheses

**H0** (null): No difference between approaches.

**H1**: Mandate outperforms motivation.
- Explicit specs reduce errors
- Structure helps task completion
- Algorithms benefit from algorithms

**H2**: Motivation outperforms mandate.
- Agency enables judgment
- Principles handle edge cases
- Constitutional AI responds to reasoning

**H3**: Effect is task-dependent.
- Mandate wins on algorithmic tasks
- Motivation wins on judgment tasks
- Hybrid optimal overall

**H4**: No approach beats baseline.
- Framework overhead exceeds benefit
- Keep it simple

All outcomes are valuable findings.

## What Would Falsify Each Hypothesis

| Hypothesis | Falsified by |
|------------|--------------|
| H0 (no difference) | Statistically significant difference on any metric |
| H1 (mandate wins) | Motivation outperforms on pass@k or recovery_rate |
| H2 (motivation wins) | Mandate outperforms on pass@k or recovery_rate |
| H3 (task-dependent) | One approach wins across all task types |
| H4 (baseline wins) | Any methodology beats baseline significantly |

## Prior Art

| Work | Relevance |
|------|-----------|
| Constitutional AI (Anthropic 2022) | Values vs rules in AI training |
| Blaurock et al. 2024 | Transparency + control > engagement |
| Scott Spence eval | Forced language doesn't improve activation beyond threshold |
| REP-001 | Methodology measurement is possible |

### Gap This Fills

No controlled experiments compare:
- Spec-driven frameworks vs principles-based approaches
- Mandate vs motivation prompting styles
- Algorithm runner vs reasoning agent mental models

The discourse is tribal. We can measure.

## Open Questions

1. **Fair representation**: How to crystallize each framework as a prompt without strawmanning?

2. **Principles prompt**: What does an effective motivation-based prompt look like? (core-1337 as starting point, but may need iteration)

3. **Ambiguity calibration**: How underspecified is underspecified enough to differentiate?

4. **Model dependency**: Results may vary by model. Test Haiku, Sonnet, Opus?

5. **Task selection**: Use existing benchmarks (SWE-bench, HumanEval) or custom tasks?

## Why This Matters

Whichever finding emerges is valuable:

**If mandate-based approaches produce better outcomes:**
- Validates spec-driven frameworks
- Suggests structure > agency for current AI
- Informs how to write effective prompts

**If motivation-based approaches produce better outcomes:**
- Validates Constitutional AI interaction model
- Suggests principles > specs
- Changes how we design AI collaboration

**If task-dependent:**
- Provides decision framework for when to use which
- Both approaches have valid use cases
- Context determines choice

**If baseline wins:**
- Framework overhead hurts outcomes
- Simplicity > methodology
- Keep interaction minimal

The agentic era is scaling fast. Teams adopt frameworks based on GitHub stars and Twitter threads. Evidence would help.

## References

- Anthropic. "Constitutional AI: Harmlessness from AI Feedback" (2022)
- Blaurock, M. et al. "AI-Based Service Experience Contingencies" Journal of Service Research (2024)
- BMAD Method: https://github.com/bmad-code-org/BMAD-METHOD
- Get Shit Done: https://github.com/glittercowboy/get-shit-done
- spec-kit: https://github.com/github/spec-kit
- Feynman, R. "Cargo Cult Science" (1974)
