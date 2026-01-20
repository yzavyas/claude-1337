# REP-002: Mandates vs Motivations

## Experiment Status

| | |
|---|---|
| **Status** | 🔬 RUNNING |
| **Progress** | 32/90 runs (35%) |
| **Started** | 2026-01-20 10:43 |
| **ETA** | ~4 hours remaining |

---

## Research Question

> Does motivation-based prompting (principles + WHY) produce better outcomes than mandate-based prompting (rigid specs/templates) on software engineering tasks?

**Hypothesis**: Motivation-based prompting will outperform mandate-based prompting on high-ambiguity tasks, where judgment and interpretation matter more than rigid process.

---

## Experimental Design

### Conditions (5)

| Condition | Type | Provides |
|-----------|------|----------|
| `baseline` | Control | Task only |
| `motivation` | Principles | WHAT + WHY + CONSTRAINTS |
| `mandate-template` | Spec | + Required template artifacts |
| `mandate-structure` | Spec | + File structure rules |
| `mandate-role` | Spec | + Expert persona |

### Tasks (6)

| Task | Ambiguity | Status |
|------|-----------|--------|
| pytest-dev__pytest-10051 | LOW | ✅ Complete |
| scikit-learn__scikit-learn-10297 | LOW | ✅ Complete |
| django__django-10097 | HIGH | 🔄 Running |
| django__django-11848 | HIGH | ⏳ Pending |
| django__django-10554 | HIGH | ⏳ Pending |
| django__django-11087 | HIGH | ⏳ Pending |

### Execution

- **Model**: Claude Sonnet
- **Runs per condition**: 3
- **Total runs**: 6 tasks × 5 conditions × 3 runs = 90
- **Grader**: SWE-bench Docker harness

---

## Interim Findings

> ⚠️ **These are preliminary observations from partial data. Conclusions may change as more results arrive.**

### Current Data Snapshot

**Overall**: 15/32 passed (47%)

#### By Task
| Task | Pass Rate | Avg Tokens | Avg Duration | Observation |
|------|-----------|------------|--------------|-------------|
| pytest-dev__pytest-10051 | 0/15 (0%) | 1,578 | 229s | Floor — too hard |
| scikit-learn__scikit-learn-10297 | 15/15 (100%) | 1,455 | 250s | Ceiling — too easy |
| django__django-10097 | 0/2 (0%) | 1,784 | 405s | In progress |

#### By Condition (Efficiency & Effectiveness)
| Condition | Pass Rate | Avg Tokens | Avg Duration | Token σ |
|-----------|-----------|------------|--------------|---------|
| baseline | 3/8 (38%) | 1,837 | 276s | 236 |
| motivation | 3/6 (50%) | 1,364 | **205s** ⚡ | 356 |
| mandate-template | 3/6 (50%) | 1,637 | 253s | 224 |
| mandate-structure | 3/6 (50%) | **970** ⚡ | 270s | 219 |
| mandate-role | 3/6 (50%) | 1,757 | 236s | 215 |

#### Reliability (Consistency Across Attempts)
| Metric | Value |
|--------|-------|
| Consistent (same result all 3 attempts) | 11/11 |
| Inconsistent | 0/11 |
| **Reliability** | **100%** ✓ |

---

### Interim Finding 1: Task Difficulty Dominates

**Observation**: The two completed tasks show extreme outcomes — 0% and 100% — regardless of condition.

**Evidence**:
```
pytest (LOW ambiguity):      0/15 = 0%   ALL conditions
scikit-learn (LOW ambiguity): 15/15 = 100% ALL conditions
```

**Interpretation**: Task difficulty appears to be the primary factor. Prompting strategy effects are not detectable when tasks hit floor or ceiling.

**Confidence**: HIGH (30 data points, consistent pattern)

---

### Interim Finding 2: No Condition Differentiation Yet

**Observation**: All conditions perform equivalently on completed tasks.

**Evidence**:
- On pytest: ALL conditions = 0%
- On scikit-learn: ALL conditions = 100%
- Aggregated: All conditions ≈ 50%

**Interpretation**: Either (a) conditions truly don't matter, or (b) floor/ceiling effects are masking differences. Need "Goldilocks" tasks (30-70% baseline) to discriminate.

**Confidence**: LOW (confounded by task effects)

---

### Interim Finding 3: Stratification Flaw Identified

**Observation**: "Ambiguity" and "difficulty" are orthogonal.

**Evidence**:
| Task | Ambiguity Label | Actual Difficulty |
|------|-----------------|-------------------|
| pytest | LOW | HARD (0%) |
| scikit-learn | LOW | EASY (100%) |

**Interpretation**: A "clear bug" (low ambiguity) can still be hard to fix. Our stratification conflated these dimensions.

**Confidence**: HIGH

---

### Interim Finding 4: Efficiency Varies by Condition

**Observation**: Different prompting strategies produce different token usage and speed.

**Evidence**:
| Condition | Avg Tokens | vs Baseline |
|-----------|------------|-------------|
| baseline | 1,837 | — |
| motivation | 1,364 | -26% |
| mandate-template | 1,637 | -11% |
| **mandate-structure** | **970** | **-47%** |
| mandate-role | 1,757 | -4% |

**Interpretation**:
- `mandate-structure` is most efficient — uses HALF the tokens of baseline
- `motivation` is fastest (205s vs 276s baseline)
- Rigid file structure rules may constrain Claude's exploration, reducing token use

**Confidence**: MEDIUM (pattern consistent but small n)

---

### Interim Finding 5: Perfect Reliability

**Observation**: All condition×task combinations produced identical results across 3 attempts.

**Evidence**:
- 11/11 combinations consistent
- 0/11 combinations showed variance
- **100% reliability**

**Interpretation**: The outcomes are deterministic given task + condition. Variance across runs is NOT a factor — the primary variance is between tasks.

**Confidence**: HIGH

---

## What We're Watching

### Django Tasks (HIGH Ambiguity)

The remaining 4 tasks are labeled HIGH ambiguity. Key questions:

1. **Will they discriminate?** — Show different pass rates by condition?
2. **Will they hit floor/ceiling?** — 0% or 100% like the others?
3. **Is ambiguity the right dimension?** — Or do we need difficulty-stratified tasks?

### Early Django Signal

django__django-10097 (URLValidator): 0/2 on baseline so far. If this continues to 0% across conditions, it suggests another floor effect.

---

## Methodology Notes

### The Goldilocks Problem

For condition effects to be detectable, we need tasks where:
```
          Discriminating range
                 ↓
0%────────[30%]════════[70%]────────100%
 ↑                                    ↑
Floor                              Ceiling
(can't improve)                (can't detect improvement)
```

Current tasks are at extremes, not in the discriminating range.

### Potential Next Steps (Post-Experiment)

If SWE-bench tasks don't discriminate:
1. **Function grader** — Design tasks with known 30-70% baseline
2. **Task filtering** — Select SWE-bench tasks by historical pass rate
3. **Difficulty calibration** — Pre-screen tasks for discriminating range

---

## Interim Conclusions

| Claim | Evidence | Confidence |
|-------|----------|------------|
| Task difficulty >> condition effects | 0% vs 100% task variance | HIGH |
| All conditions equivalent in pass rate | All ~50% aggregated | LOW (confounded) |
| Ambiguity ≠ Difficulty | Orthogonal outcomes | HIGH |
| Need "Goldilocks" tasks | Floor/ceiling mask effects | HIGH |
| mandate-structure most token-efficient | 970 vs 1,837 tokens (-47%) | MEDIUM |
| motivation fastest | 205s vs 276s (-26%) | MEDIUM |
| Results are deterministic | 100% reliability (11/11) | HIGH |

---

## Data Quality

| Metric | Value |
|--------|-------|
| Runs completed | 32/90 (35%) |
| Tasks fully evaluated | 2/6 |
| Tasks partially evaluated | 1/6 |
| Tasks pending | 3/6 |
| Key confound | Floor/ceiling effects |

---

## Live Updates

Results streaming to: `experiments/rep-002/results/rep-002-stratified-ready/`

Monitor progress:
```bash
tail -f /private/tmp/claude/.../tasks/be49baa.output
```

---

*Interim findings — experiment in progress*
*Last updated: 2026-01-20 12:20*
