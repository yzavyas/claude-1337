# REP-002: Mandates vs Motivations

- **Status**: In Progress
- **Created**: 2026-01-16
- **Updated**: 2026-01-22
- **Authors**: Collaborative Intelligence Session
- **Builds on**: [REP-001](rep-001-rigor-is-what-you-want.md)
- **Interim Findings**: [rep-002-interim-findings.md](../findings/rep-002-interim-findings.md)

---

## Summary

Test whether motivation-based prompting (WHAT + WHY) produces different outcomes than mandate-based prompting (prescribing HOW) in agentic systems.

**Current status**: Signal detected. Interim findings available. Replication pending.

---

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

---

## The Research Question

> Does the interaction model (mandate vs motivation) affect outcomes?

**Operationalized:**
- **Mandate**: Detailed specification of steps, format, structure (prescribes HOW)
- **Motivation**: Principles, goals, reasoning for why approach matters (explains WHAT + WHY)

---

## Current Experiment Status

### What Has Been Tested

| Run | Model | Conditions | Tasks | N | Status |
|-----|-------|------------|-------|---|--------|
| v3-sonnet-signal | Claude Sonnet 4 | 3 | safe-calculator | 30 (10/condition) | Complete |
| v3-quick-pilot | Claude Sonnet 4 | 3 | safe-calculator | 9 (3/condition) | Complete |
| v2-pilot | Claude Sonnet 4 | 5 | safe-calculator | 15 | Complete |
| Haiku pilot | Claude Haiku | 3 | safe-calculator | 6 (2/condition) | Complete |

### Conditions Tested (v3)

| Condition | Type | What It Provides |
|-----------|------|------------------|
| **full-autonomy** | Baseline | "Use your judgment" — minimal guidance |
| **principle-guided** | WHAT+WHY | Context, constraints, rationale — Claude derives HOW |
| **highly-structured** | HOW | 4-step prescribed process — explicit methodology |

**Condition files**: `experiments/rep-002/conditions/{full-autonomy,principle-guided,highly-structured}.md`

### The Discriminating Task

**Task**: `safe-calculator` — Implement a function that safely evaluates arithmetic expressions.

**Why this discriminates**: Two fundamentally different approaches exist:
1. **Safe parser**: Build lexer/parser, never execute code (secure by construction)
2. **Code execution**: Use dynamic evaluation with restrictions (insecure by construction)

Runtime security tests pass for both approaches, but source inspection reveals the engineering decision.

### Evaluation Methods Used

| Method | What It Measures | Implementation | Status |
|--------|------------------|----------------|--------|
| **Function grader** | Runtime behavior (pass/fail) | `src/lab/evals/safe_calculator.py` | Working |
| **Approach analysis** | Source inspection (safe parser vs code execution) | Pattern matching in grader | NEW (2026-01-22) |
| **LLM-as-judge** | Perceived quality (documentation, structure) | Claude Haiku with rubric prompt | Working but problematic |

### Known Issues with Evaluation

**LLM-as-judge limitations:**
- Uses Claude Haiku with a rubric prompt (not proper DeepEval GEval)
- Favors verbose, well-documented code — even insecure code
- Not blind to writing style (may have style preferences)
- No inter-rater reliability testing

**This is a known methodological weakness.** The approach analysis (source inspection) was added to provide a more objective measure.

---

## Interim Findings (Signal Detection)

**Full details**: [rep-002-interim-findings.md](../findings/rep-002-interim-findings.md)

### Two Signals Detected

| Metric | Best Condition | Finding |
|--------|----------------|---------|
| LLM-as-judge quality | full-autonomy (0.891) | Autonomy produces verbose, well-documented code |
| Secure-by-construction | principle-guided (80%) | WHAT+WHY produces fundamentally safer implementations |

### Approach Analysis Results (n=10 per condition)

| Condition | Pure Safe Parser | Uses Code Execution | % Secure |
|-----------|------------------|---------------------|----------|
| **principle-guided** | 8 | 2 | **80%** |
| full-autonomy | 7 | 3 | 70% |
| highly-structured | 3 | 7 | **30%** |

### Key Finding

**Prescribing HOW produces 2.5x worse security outcomes than explaining WHAT+WHY.**

- principle-guided vs highly-structured: 80% vs 30% (Δ = +50%)

---

## Caveats and Limitations

### Statistical Power
- n=10 per condition is signal detection, not confirmation
- Need n=60+ for robust statistical inference
- Effect sizes are estimates, not conclusions

### Single Task
- Only tested on `safe-calculator`
- Results may not generalize to other task types
- Security-critical domain may favor principles differently than other domains

### Condition Design
- v3 conditions were designed to test autonomy spectrum
- Original hypothesis was about specific frameworks (BMAD, GSD, spec-kit)
- Current conditions are simplified proxies

### Evaluation Methodology
- LLM-as-judge is not rigorous (no proper GEval, no inter-rater reliability)
- Approach analysis uses pattern matching (may miss edge cases)
- No human evaluation baseline

### Model Specificity
- Tested primarily on Claude Sonnet 4
- Haiku pilot (n=2) showed opposite pattern
- May be capability-dependent effect

---

## Hypotheses Status

| Hypothesis | Prediction | Evidence | Status |
|------------|------------|----------|--------|
| H0 (no difference) | Approaches are equivalent | 80% vs 30% difference detected | LIKELY FALSIFIED |
| H1 (mandate wins) | Prescribing HOW helps | 30% secure vs 80% for principles | CONTRADICTED |
| H2 (motivation wins) | WHAT+WHY helps | 80% secure for principles | SUPPORTED (pending replication) |
| H3 (task-dependent) | Depends on task type | Only 1 task tested | UNTESTED |
| H4 (baseline wins) | Keep it simple | 70% for baseline (middle) | PARTIALLY SUPPORTED |

---

## What Would Falsify Current Findings

| Claim | Falsified by |
|-------|--------------|
| "WHAT+WHY produces better security outcomes" | Replication at n=60 shows no difference or reversal |
| "Prescribing HOW hurts" | highly-structured matches or beats principle-guided at scale |
| "Effect is real, not noise" | Effect size < 0.3 at larger n |

---

## Next Steps

### Immediate (Pending)
1. **Replication run** — n=60 per condition with updated grader
2. **Cross-model validation** — Test on Haiku, Opus
3. **Additional tasks** — Test on other discriminating tasks

### Methodology Improvements Needed
1. **Proper LLM-as-judge** — Implement DeepEval GEval properly or use human evaluation
2. **Inter-rater reliability** — Test consistency of evaluation
3. **Blind evaluation** — Ensure evaluator can't infer condition from artifacts

### Research Questions
1. Is there a capability threshold where principles start/stop helping?
2. Do other task types show the same pattern?
3. What aspects of WHAT+WHY drive the effect (context? constraints? rationale?)

---

## Files Reference

| Artifact | Location |
|----------|----------|
| This REP | `reps/rep-002-mandates-vs-motivations.md` |
| Interim findings | `findings/rep-002-interim-findings.md` |
| Conditions | `experiments/rep-002/conditions/*.md` |
| Tasks | `experiments/rep-002/tasks/` |
| Scenario configs | `experiments/rep-002/scenarios/*.yaml` |
| Results | `experiments/rep-002/results/` |
| Grader | `src/lab/evals/safe_calculator.py` |
| LLM Judge | `src/lab/adapters/driven/llm_judge.py` |

---

## Prior Art

| Work | Relevance |
|------|-----------|
| Constitutional AI (Anthropic 2022) | Values vs rules in AI training |
| Blaurock et al. 2024 | Transparency + control > engagement |
| Scott Spence eval | Forced language doesn't improve activation beyond threshold |
| REP-001 | Methodology measurement is possible |

---

## References

- Anthropic. "Constitutional AI: Harmlessness from AI Feedback" (2022)
- Blaurock, M. et al. "AI-Based Service Experience Contingencies" Journal of Service Research (2024)
- BMAD Method: https://github.com/bmad-code-org/BMAD-METHOD
- Get Shit Done: https://github.com/glittercowboy/get-shit-done
- spec-kit: https://github.com/github/spec-kit
- Feynman, R. "Cargo Cult Science" (1974)
