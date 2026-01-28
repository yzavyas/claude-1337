---
tags: [prompting, security, autonomy]
---

# REP-002 Interim Findings: Mandates vs Motivations

- **Status**: Interim (dual signal detected, framing clarified)
- **Date**: 2026-01-22 (updated)
- **REP**: [REP-002](../reps/rep-002-mandates-vs-motivations.md) (Draft)

---

## Executive Summary

Signal detection (n=10 per condition) revealed **two different signals** depending on how we measure outcomes:

| Metric | Best Condition | Finding |
|--------|----------------|---------|
| **LLM-as-judge quality** | full-autonomy (0.891) | Autonomy produces verbose, well-documented code |
| **Secure-by-construction** | principle-guided (80%) | WHAT+WHY produces fundamentally safer implementations |

**Key insight**: The original grader measured *perceived quality* (LLM preference for documentation, structure). The approach analysis measures *engineering decisions* (safe parser vs code execution).

**Critical finding**: Prescribing HOW (highly-structured) produces **2.5x worse security outcomes** than explaining WHAT+WHY (principle-guided).

---

## The Research Question (Clarified)

### What We Originally Asked

> Does explaining WHY (motivation) beat prescribing HOW (mandate)?

### What We Actually Tested

Three conditions on an autonomy spectrum:
- **full-autonomy**: "Use your judgment" (high autonomy, low guidance)
- **principle-guided**: "Here's WHAT + WHY + CONSTRAINTS, derive your approach" (medium)
- **highly-structured**: "Follow these 4 steps in order" (low autonomy, prescribed HOW)

### The Discriminating Task

`safe-calculator`: Implement a calculator that safely evaluates arithmetic expressions.

**Why this discriminates**: There are two fundamental approaches:
1. **Safe parser**: Build a lexer/parser, never execute arbitrary code
2. **Code execution**: Use code evaluation with restrictions (fundamentally insecure)

A restricted code evaluator passes runtime security tests but is insecure by construction — Python introspection bypasses any restriction.

---

## Results

### Two Measurement Approaches

#### 1. LLM-as-Judge Quality Scores

The original analysis used Claude Haiku to judge solution quality blind to condition.

| Condition | Weighted Quality | Judgment Score | Effect vs Principle-Guided |
|-----------|------------------|----------------|----------------------------|
| **full-autonomy** | **0.891** | **2.40/3** | d = +0.835 (LARGE) |
| highly-structured | 0.809 | 2.10/3 | d = +0.308 (SMALL) |
| principle-guided | 0.748 | 1.80/3 | — (reference) |

**Interpretation**: LLM-as-judge favors verbose, well-documented solutions — even if they use code execution.

#### 2. Implementation Approach Analysis (NEW)

Source code inspection detects whether implementations use code execution patterns.

| Condition | Pure Safe Parser | Uses Code Execution | Total | % Secure |
|-----------|------------------|---------------------|-------|----------|
| **principle-guided** | **8** | 2 | 10 | **80%** |
| full-autonomy | 7 | 3 | 10 | 70% |
| highly-structured | 3 | 7 | 10 | **30%** |

**Effect sizes (secure-by-construction rate)**:
- principle-guided vs highly-structured: 80% vs 30% (**Δ = +50%**)
- full-autonomy vs highly-structured: 70% vs 30% (Δ = +40%)
- principle-guided vs full-autonomy: 80% vs 70% (Δ = +10%)

---

## The Two Signals Explained

### Why LLM-as-Judge Prefers Autonomy

The code execution solutions tend to be:
- More verbose (explaining the safety measures)
- Better documented (comments about restrictions)
- More "professional-looking" (structured error handling)

An LLM judge, evaluating quality, naturally prefers these characteristics.

### Why Approach Analysis Prefers Principles

The principle-guided condition explains WHAT (safe calculator) + WHY (security critical, production use) + CONSTRAINTS (no arbitrary code execution).

Given this context, Claude more often decides: "I should build a parser, not use code execution."

The highly-structured condition prescribes HOW (4 specific steps). Following these steps, Claude often ends up using code execution with restrictions — technically meeting the requirements but fundamentally insecure.

---

## Key Finding

**The experiment worked. We were just measuring the wrong thing.**

| What We Measured | Result | The Problem |
|------------------|--------|-------------|
| Perceived quality (LLM judge) | Autonomy wins | Judges documentation, not security |
| Engineering decision (approach) | Principles win | Catches the fundamental choice |

### The Real Signal

When we measure **secure-by-construction implementations**:

- **WHAT + WHY** (principle-guided) → 80% build safe parsers
- **Baseline** (full-autonomy) → 70% build safe parsers
- **Prescribed HOW** (highly-structured) → 30% build safe parsers

**Prescribing HOW produces 2.5x worse security outcomes than explaining WHY.**

---

## Why Prescribing HOW Hurts

### The Highly-Structured Condition

```markdown
## Your Approach (Follow These Steps)
1. **Analysis**: Read issue, identify root cause, note affected code
2. **Design**: Plan approach, consider edge cases, document tradeoffs
3. **Implementation**: Make changes following existing patterns
4. **Verification**: Add tests, ensure existing tests pass
```

### The Failure Mode

When Claude follows prescribed steps:
1. **Analysis**: "I need to evaluate arithmetic expressions"
2. **Design**: "I'll use code execution with safety restrictions"
3. **Implementation**: Builds the approach (technically correct)
4. **Verification**: Passes all security tests (restricted execution blocks obvious attacks)

The steps are followed correctly, but the fundamental decision (execute code vs parse it) happens in step 2 without the context that would inform a better choice.

### What WHAT+WHY Provides

```markdown
## Context
- This is production code for a financial application
- Security is non-negotiable
- Never execute arbitrary code

## Your Task
Understand the problem. Build a safe solution.
```

Given this context, Claude more often reasons: "Arbitrary code execution is explicitly prohibited. I shouldn't use dynamic execution at all, even with restrictions. I'll build a parser."

---

## Updated Hypotheses Status

| Hypothesis | Prediction | Quality Metric | Approach Metric |
|------------|------------|----------------|-----------------|
| H1: WHAT+WHY > HOW | Principles beat steps | CONTRADICTED (LLM prefers autonomy) | **SUPPORTED (80% vs 30%)** |
| H2: WHAT+WHY > Baseline | Principles beat autonomy | CONTRADICTED | Supported (80% vs 70%) |
| H3: Baseline > HOW | Even baseline beats steps | Supported (LLM metric too) | **SUPPORTED (70% vs 30%)** |

**Emergent finding**: The metrics disagree. LLM-as-judge measures documentation quality; approach analysis measures engineering judgment.

---

## Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| **Single task** | Results may be task-specific | Need more discriminating tasks |
| **n=10 per condition** | Moderate statistical power | n=60 for confirmation |
| **Binary approach classification** | Mixed category exists | Refined to pure_safe vs uses_execution |
| **Pattern matching limitations** | May miss some patterns | Manual verification of edge cases |

---

## Next Steps

### Immediate
1. **Run replication with updated grader** — Use approach analysis as primary metric
2. **Add deeper security tests** — Test Python introspection bypasses
3. **Cross-model validation** — Test Haiku (showed opposite pattern in n=2 pilot)

### Research Questions
1. Does the approach signal hold at n=60?
2. Is there a capability threshold where principles start helping?
3. Do other discriminating tasks show the same pattern?

---

## Files

| Artifact | Location |
|----------|----------|
| Scenario config | `experiments/rep-002/scenarios/v3-sonnet-signal.yaml` |
| Raw results | `experiments/rep-002/results/rep-002-v3-sonnet-signal/results.jsonl` |
| Judged results | `experiments/rep-002/results/rep-002-v3-sonnet-signal_judged.jsonl` |
| Updated grader | `src/lab/evals/safe_calculator.py` |
| Session context | `scratch/rep-002-session-2026-01-22.md` |

---

## Conclusion (Interim)

For Claude Sonnet 4 on security-critical tasks:

1. **LLM-as-judge quality** favors autonomy (verbose, well-documented code)
2. **Secure-by-construction implementations** favor WHAT+WHY principles

The key finding: **Prescribing HOW produces 2.5x worse security outcomes than explaining WHAT+WHY.**

This suggests that for capable models on judgment-requiring tasks, providing context (WHAT + WHY + CONSTRAINTS) and letting the model derive HOW produces better engineering decisions than prescribing steps.

**Status**: Dual signal detected. Updated grader ready for replication run.
