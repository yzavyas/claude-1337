# REP-002: Mandates vs Motivations

- **Status**: Draft
- **Created**: 2026-01-16
- **Authors**: Collaborative Intelligence Session
- **Builds on**: [REP-001](rep-001-rigor-is-what-you-want.md)

## Summary

Test whether explaining WHY (motivation) produces different outcomes than prescribing HOW (mandate) when working with Claude. The hypothesis: Claude is Constitutional AI — trained with values, not rigid rules — and may respond better to motivation than mandate.

## Motivation

REP-001 established that methodology effectiveness is measurable. This REP applies that capability to a foundational question: **how should we interact with AI?**

### The Mental Model Gap

Two competing mental models for AI interaction:

| Model | Assumption | Interaction Style |
|-------|------------|-------------------|
| **Algorithm runner** | AI executes instructions | Prescribe HOW in detail |
| **Reasoning agent** | AI exercises judgment | Explain WHY, let it decide HOW |

The algorithm runner model shaped early prompt engineering: more detail = more control = better outcomes. This led to frameworks prescribing exact artifacts, file structures, and personas.

### The Constitutional AI Insight

Claude is trained differently. Constitutional AI (Anthropic 2022) uses values-based training:

> "Values-based training produces understanding and judgment. Rule-based constraints produce compliance and brittleness."

This suggests a different interaction model might be effective:
- Explain WHY, not just WHAT
- Principles that generalize, not specs that enumerate
- Agency retained, not removed

### The Uncertainty

We don't know which produces better outcomes. Both have plausible arguments:

**For mandate (prescribe HOW):**
- Removes ambiguity
- Consistent structure
- Explicit expectations

**For motivation (explain WHY):**
- Enables judgment
- Handles edge cases
- Adapts to context
- Aligns with Constitutional AI design

The discourse is tribal. This is testable.

## The Question

> Does prescribing HOW help or hurt, compared to explaining WHY?

## Experiment Design

### Isolating the Variable

The key insight: **all conditions share the same WHAT + WHY + CONSTRAINTS**. The only difference is whether/how HOW is prescribed.

This isolates the variable being tested.

### Conditions

| Condition | Type | What Claude Receives |
|-----------|------|---------------------|
| `baseline` | Control | WHAT only — pure Claude, no methodology |
| `motivation` | Principles | WHAT + WHY + CONSTRAINTS (Claude decides HOW) |
| `mandate-template` | Mandate | Above + HOW via required template artifacts |
| `mandate-structure` | Mandate | Above + HOW via required file structure |
| `mandate-role` | Mandate | Above + HOW via prescribed expert persona |

### Why These Specific Mandates?

Each tests a different flavor of "prescribing HOW":

| Mandate Type | Example Pattern | Tests Whether... |
|--------------|-----------------|------------------|
| **Template** | "Produce these artifacts: spec.md, plan.md, impl.md" | Required outputs help or constrain |
| **Structure** | "Use this file layout: PROJECT/, PLAN/, STATE/" | Imposed organization helps or constrains |
| **Role** | "You are a senior architect who always..." | Prescribed persona helps or constrains |

### Metrics

| Metric | What it Measures |
|--------|------------------|
| `pass@k` | Task completion in k attempts |
| `recovery_rate` | Ability to fix own mistakes |
| `tokens_used` | Efficiency (cost) |

### Benchmark

SWE-bench lite subset — real-world software engineering tasks with ground truth via test suites.

## Hypotheses

**H0** (null): No difference between approaches.

**H1**: Mandate outperforms motivation.
- Explicit structure reduces errors
- Prescribed process helps task completion

**H2**: Motivation outperforms mandate.
- Agency enables judgment
- Principles handle varied contexts
- Constitutional AI responds to reasoning

**H3**: Effect is task-dependent.
- Mandate wins on structured tasks
- Motivation wins on judgment tasks

**H4**: Baseline wins.
- Any methodology overhead hurts outcomes
- Keep it simple

All outcomes are valuable findings.

## What Would Falsify Each Hypothesis

| Hypothesis | Falsified By |
|------------|--------------|
| H0 (no difference) | Statistically significant difference on any metric |
| H1 (mandate wins) | Motivation outperforms on pass@k or recovery_rate |
| H2 (motivation wins) | Any mandate outperforms on pass@k or recovery_rate |
| H3 (task-dependent) | One approach wins across all task types |
| H4 (baseline wins) | Any methodology beats baseline significantly |

## Interim Findings

*Status: Pre-experiment — design phase*

No quantitative results yet. However, observations during skill development and collaborative sessions suggest:

**Directional signals (not evidence):**
- Forceful language ("MUST", "MANDATORY") doesn't improve activation beyond threshold (Scott Spence eval, 200+ tests)
- Claude exercises judgment about relevance regardless of instruction style
- Over-specified instructions sometimes produce worse outcomes (anecdotal)

**What we don't know:**
- Whether these observations generalize to controlled conditions
- The magnitude of any effect
- Whether task type moderates the effect

**Next steps:**
1. Finalize condition prompts (ensure fair representation)
2. Pilot batch: 2 tasks × 5 conditions × 3 runs
3. Signal batch if pilot validates harness
4. Full batch for statistical significance

## Prior Art

| Work | Relevance |
|------|-----------|
| Constitutional AI (Anthropic 2022) | Values vs rules in AI training |
| Blaurock et al. 2024 | Transparency + control produce complementary outcomes (β = 0.415, 0.507) |
| Scott Spence eval | Forced language doesn't improve activation beyond threshold |
| REP-001 | Methodology measurement is possible |

### Gap This Fills

No controlled experiments compare:
- Motivation-based vs mandate-based prompting
- The effect of prescribing HOW vs explaining WHY
- Whether Constitutional AI training affects optimal interaction style

## Open Questions

1. **Fair representation**: How to crystallize each condition as a prompt without strawmanning?

2. **Shared context**: What WHAT + WHY + CONSTRAINTS should all conditions share?

3. **Task selection**: Which SWE-bench tasks best differentiate the approaches?

4. **Model dependency**: Results may vary by model. Start with Sonnet, extend if findings warrant.

## Why This Matters

The agentic era is scaling fast. Teams adopt interaction patterns based on intuition and tribal preference. Evidence would help.

**If motivation wins:** Validates the Constitutional AI interaction model. Stop prescribing HOW; explain WHY.

**If mandate wins:** Structure helps even reasoning agents. Invest in process specification.

**If task-dependent:** Provides decision framework for when to use which.

**If baseline wins:** Framework overhead hurts. Keep interaction minimal.

## References

- Anthropic. "Constitutional AI: Harmlessness from AI Feedback" (2022)
- Blaurock, M. et al. "AI-Based Service Experience Contingencies" Journal of Service Research (2024)
- Feynman, R. "Cargo Cult Science" (1974)
