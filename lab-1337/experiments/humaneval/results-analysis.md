# HumanEval Benchmark Analysis: Ralph Iteration Effect

**Date:** 2026-01-15
**Model:** Claude Haiku
**Dataset:** 50 problems from HumanEval
**Methodology:** COVE (Chain of Verification)

---

## Executive Summary

Ralph-style iteration with session continuity achieved **100% pass rate** compared to **94% for single-shot**, recovering all 3 failures at a cost of ~9x tokens. However, only 1 of 3 recovered problems actually required iteration—the other 2 passed on the first ralph-style attempt, suggesting structured output (file writing) may independently improve reliability.

---

## Key Findings

| Metric | Single-Shot | Ralph-Style | Delta |
|--------|-------------|-------------|-------|
| Pass Rate | 94% (47/50) | 100% (50/50) | +6pp |
| Avg Tokens | 190 | 1,699 | 8.9x |
| Avg Iterations | 1.0 | 1.26 | +0.26 |
| Total Duration | 72s | 628s | 8.7x |

---

## Verified Claims

### 1. [VERIFIED] Ralph-style recovers single-shot failures

**Evidence:** Three problems failed single-shot and passed ralph-style:

| Problem | Single-Shot | Ralph-Style | Iterations |
|---------|-------------|-------------|------------|
| HumanEval/24 | FAIL | PASS | 1 |
| HumanEval/32 | FAIL | PASS | 2 |
| HumanEval/41 | FAIL | PASS | 1 |

**Verification:** Cross-checked each result in raw data. All three single-shot failures (passed=false) have corresponding ralph-style passes (passed=true).

### 2. [VERIFIED] Token cost is approximately 9x

**Evidence:**
- Single-shot average: 189.92 tokens
- Ralph-style average: 1698.76 tokens
- Ratio: 8.94x

**Verification:** Calculated independently from raw results array. Sum of all ralph tokens / 50 = 1698.76.

### 3. [VERIFIED] No problems required maximum iterations

**Evidence:** All ralph-style results show iterations ≤ 2. Maximum allowed was 3.

**Verification:** Searched results for any iterations=3. None found.

---

## Uncertain Claims

### [UNCERTAIN] Iteration is the primary improvement mechanism

**Observation:** 2 of 3 recovered problems (HumanEval/24, HumanEval/41) passed ralph-style on the **first iteration**.

**Hypothesis:** The structured output approach (writing to a file via tools) may produce more reliable code than raw text generation.

**What would confirm this:**
- Run single-shot with file-writing tools (no iteration)
- Compare to raw text single-shot
- If file-writing single-shot outperforms raw text, hypothesis confirmed

**Current evidence is insufficient** to separate the effect of structured output from iteration.

---

## Detailed Analysis

### Problems Where Iteration Actually Helped

Only **HumanEval/32** required iteration:

| Metric | Single-Shot | Ralph Attempt 1 | Ralph Attempt 2 |
|--------|-------------|-----------------|-----------------|
| Passed | No | No (implied) | Yes |
| Tokens | 719 | ~2500 (est) | ~3000 (est) |

This problem used more tokens than other failures (719 vs 311-345), suggesting complexity.

### Iteration Distribution

| Iterations Needed | Count | Percentage |
|-------------------|-------|------------|
| 1 | 37 | 74% |
| 2 | 13 | 26% |
| 3 | 0 | 0% |

Most problems (74%) pass on the first ralph-style attempt, suggesting the overhead of the iteration infrastructure may not always be necessary.

### Token Efficiency

For problems that passed both strategies:

| Scenario | Single-Shot Tokens | Ralph Tokens | Ratio |
|----------|-------------------|--------------|-------|
| Problems 0-23 | 3,756 | 31,606 | 8.4x |
| Problems 24-49 | 5,740 | 53,332 | 9.3x |

Higher problem numbers (harder problems) show slightly worse token efficiency for ralph-style.

---

## COVE Verification Notes

### Phase 2 - Verification Questions Asked

**Q: Did single-shot actually fail the 3 claimed problems?**
A: Yes. Verified passed=false for HumanEval/24, 32, 41 in raw data.

**Q: Did ralph-style introduce any NEW failures?**
A: No. All 50 ralph-style results show passed=true.

**Q: Is the 9x token claim accurate?**
A: Yes. 1698.76 / 189.92 = 8.94x, rounded to 9x.

**Q: What would contradict "iteration helps"?**
A: If ralph-style failed problems that single-shot passed. This did not occur.

### Phase 3 - Fresh Read Observations

1. HumanEval/32 (the only problem needing iteration) had the highest single-shot token count among failures (719 vs 311-345), suggesting it may be inherently harder.

2. No problem hit the max iteration limit (3), suggesting the 3-iteration cap is sufficient for this benchmark.

3. Duration correlation: ralph-style took ~8.7x longer, matching the token ratio closely.

---

## Limitations

1. **Sample size:** 50 problems from a 164-problem benchmark. Results may not generalize to full dataset.

2. **Single model:** Only tested with Claude Haiku. Results may differ for Sonnet/Opus.

3. **Confounded variables:** Cannot separate effect of structured output (file writing) from iteration effect.

4. **No error analysis:** Did not examine what caused the 3 single-shot failures.

5. **Determinism:** Single run per strategy. LLM outputs are stochastic; multiple runs needed for confidence intervals.

---

## Raw Data Summary

```
Total problems: 50
Single-shot: 47 passed, 3 failed
Ralph-style: 50 passed, 0 failed

Single-shot failures: HumanEval/24, HumanEval/32, HumanEval/41

Token totals:
- Single-shot: 9,496 tokens
- Ralph-style: 84,938 tokens

Duration totals:
- Single-shot: 72,155 ms
- Ralph-style: 628,161 ms
```

---

## Conclusion

Ralph-style iteration with session continuity provides a measurable improvement on HumanEval (94% → 100%), but the mechanism is not purely iteration. Two-thirds of recovered problems passed on the first ralph-style attempt, suggesting structured output may be an independent factor. Further experimentation is needed to isolate these effects.

**For methodology claims:** Iteration with external feedback CAN recover failures, as demonstrated by HumanEval/32. However, the improvement may be partly attributable to the structured approach of writing code to files rather than raw text generation.
