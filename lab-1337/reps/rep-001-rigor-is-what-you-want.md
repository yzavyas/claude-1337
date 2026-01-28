---
tags: [evidence-based, hype-cycle, methodology, iteration]
---

# REP-001: Rigor is What You Want

*You just don't know it yet*

- **Status**: Implemented
- **Created**: 2026-01-15
- **Published**: 2026-01-16
- **Authors**: Collaborative Intelligence Session

## Summary

The AI boom has created a rush to adopt tools and methodologies without measuring actual impact. **63% of IT leaders cite FOMO as their primary driver for AI investment** (ABBYY 2024), yet **74% of companies can't demonstrate tangible value** (BCG 2024). Rigorous evaluation breaks this cycle by measuring actual impact and enabling data-driven decisions.

## The Question

> In the rush to adopt AI-powered tools and methodologies, are we measuring actual impact — or just following the hype?

## Motivation

### The Hype-Driven Adoption Problem

The current AI boom shows a consistent pattern: organizations adopt tools based on hype, not evidence.

**The perception-reality gap**: A 2025 randomized controlled trial by METR found that experienced open-source developers using AI tools (Cursor Pro, Claude 3.5/3.7) were actually **19% slower** at completing tasks — despite predicting a 24% speedup beforehand (Becker et al., 2025). Developers spent more time reviewing AI outputs, prompting, and waiting than they saved on coding.

**The aggregate evidence**: A California Management Review meta-analysis pooling 371 estimates (2019-2024) found **no robust relationship between AI adoption and productivity** once publication bias and methodological issues were controlled (CMR, 2025).

**The FOMO effect**: Despite this evidence gap, adoption continues. ABBYY's 2024 survey found 63% of IT leaders cite fear of being "left behind" as a driver of AI investment. Organizations invested an average of $879,000 in AI tools while only 4% reported meaningful innovation outcomes.

### The Homogenization Risk

When everyone adopts the same tools without measuring actual outcomes, the field converges on whatever the current hype promotes — regardless of whether it works.

Zhang et al. (2025) found that LLM-generated content is systematically **more homogeneous** than human-generated content, masking underlying variation. The same pattern applies to methodology: when teams follow popular advice instead of measuring impact in their own context, the entire industry homogenizes around unverified practices.

Rigorous evaluation breaks this cycle. Different teams measuring actual outcomes will discover different optimal approaches based on their context — not what a vendor claimed or what a thought leader tweeted.

### Why This Matters

Decisions compound. Bad methodology choices bake into everything built on them. When an industry collectively adopts based on hype rather than evidence:
- Suboptimal practices become "best practices"
- Contrary evidence gets dismissed as anecdotal
- The cost of being wrong scales with adoption

### The Hypothesis

**If we replace hype-driven adoption with rigorous evaluation, we can make methodology decisions based on measured impact rather than market pressure.**

We need a way to produce hard data about what actually works — not what's popular.

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

---

## Findings

**Primary finding**: Iteration improved success from 87% to 99% at 10x the token cost.

**The insight**: Iteration is insurance, not optimization. It only helps the 13% of tasks at the edge of capability — recovering 91% of those failures. For the 87% that succeed anyway, it just burns tokens.

### The Core Pattern

```
Total problems:          164
Single-shot solved:      142 (87%)
Single-shot failed:       22 (13%)

Of those 22 failures:
  Iteration recovered:    20 (91%)
  Still failed:            2 (9%)
```

### The Decision Framework

```python
if (cost_of_failure > 10x_token_cost):
    use_iteration()
else:
    use_single_shot()
```

### When to Use Each

**Single-shot (87% success)** — Use when:
- Speed matters more than perfection
- Token budget is constrained
- Task is well within model capability
- Occasional failure is acceptable

**Iteration (99% success)** — Use when:
- Correctness is non-negotiable
- Task has known edge cases or complexity
- Cost of failure exceeds 10x token cost
- Critical path or production code

### What Iteration Can't Fix

Two problems (HumanEval/80, HumanEval/130) failed both strategies. This tells us:
- Iteration is **recovery**, not capability expansion
- There's a ceiling (98.8%, not 100%)
- Some problems require reasoning the model can't perform
- More iterations won't help beyond capability limits

### Limitations

- **Single model**: Haiku only (pattern may differ for Sonnet, Opus)
- **Single benchmark**: HumanEval (coding tasks only)
- **Functional correctness**: Didn't measure security, maintainability, or quality
- **Single run**: No statistical variance analysis

---

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

### Research on AI Hype and Adoption

| Work | Finding |
|------|---------|
| **METR RCT** (Becker et al., 2025) | Experienced developers 19% slower with AI tools despite expecting 24% speedup. [arXiv:2507.09089](https://arxiv.org/abs/2507.09089) |
| **CMR Meta-Analysis** (2025) | No robust AI-productivity relationship in 371 pooled estimates once publication bias controlled. [CMR](https://cmr.berkeley.edu/2025/10/seven-myths-about-ai-and-productivity-what-the-evidence-really-says/) |
| **ABBYY AI Trust Barometer** (2024) | 63% of IT leaders cite FOMO as adoption driver; avg $879K invested despite uncertain ROI. [ABBYY](https://www.abbyy.com/company/news/fomo-ai-adoption-abbyy-survey-results/) |
| **BCG AI Survey** (2024) | 74% of companies unable to demonstrate tangible value from AI investments. [BCG](https://www.bcg.com/press/24october2024-ai-adoption-in-2024-74-of-companies-struggle-to-achieve-and-scale-value) |
| **Zhang et al.** (2025) | LLM outputs systematically more homogeneous than human outputs, masking variation. [SAGE](https://journals.sagepub.com/doi/10.1177/00491241251327130) |

### Benchmarks and Methodology

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
