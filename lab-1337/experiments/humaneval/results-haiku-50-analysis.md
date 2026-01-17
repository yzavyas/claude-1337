# Experiment Analysis: results-haiku-50

**Generated:** 2026-01-15T22:29:53.186035
**Verification Model:** qwen2.5:7b-instruct

## Executive Summary

Ralph-style achieved 100% pass rate vs 94% for single-shot, recovering 3 failures at 8.9x token cost.

## Verified Claims

### 1. [VERIFIED] Single-shot achieved 94% pass rate (47/50 problems)

**Evidence:** S1
**Budget Gap:** -1.4 bits

### 2. [VERIFIED] Ralph-style achieved 100% pass rate (50/50 problems)

**Evidence:** S2
**Budget Gap:** -1.3 bits

### 3. [VERIFIED] Ralph-style recovered 3 problems that single-shot failed: HumanEval/24, HumanEval/32, HumanEval/41

**Evidence:** S3, S4
**Budget Gap:** -20.5 bits

## What Remains Uncertain

These claims have high budget gaps (>2 bits), meaning the evidence doesn't directly support them.
They may require calculation or inference beyond what's explicitly stated in the evidence.

### 1. [UNCERTAIN] Ralph-style uses 8.9x more tokens than single-shot

**Evidence:** S1, S2
**Budget Gap:** 12.0 bits

### 2. [UNCERTAIN] 2 of 3 recovered problems passed on first ralph-style attempt (iterations=1)

**Evidence:** S4
**Budget Gap:** 11.5 bits

### 3. [UNCERTAIN] 1 problem(s) required multiple iterations to pass: ['HumanEval/32']

**Evidence:** S4
**Budget Gap:** 9.3 bits

## Evidence Spans

<details>
<summary>Raw evidence (click to expand)</summary>

- **S0:** Benchmark metadata: model=haiku, num_problems=50, max_iterations=3
- **S1:** Single-shot summary: total=50, passed=47, pass_rate=0.94, avg_tokens=189.92
- **S2:** Ralph-style summary: total=50, passed=50, pass_rate=1.0, avg_tokens=1698.76, avg_iterations=1.26
- **S3:** Single-shot failures: ['HumanEval/24', 'HumanEval/32', 'HumanEval/41']
- **S4:** Ralph recoveries: [{'task_id': 'HumanEval/24', 'iterations': 1, 'tokens': 1144}, {'task_id': 'HumanEval/32', 'iterations': 2, 'tokens': 5512}, {'task_id': 'HumanEval/41', 'iterations': 1, 'tokens': 1836}]

</details>

## Verification Notes

- Strawberry audit: 3 claims verified, 3 uncertain

## Limitations

- Sample size: 50 problems
- Single model: haiku
- Single run per strategy (no confidence intervals)
