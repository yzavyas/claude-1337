# Research Foundations

Validated findings that inform extension design principles. All HIGH confidence (triangulated across independent sources).

## Why Extensions Must Be Complementary

### The Performance-Capability Dissociation

AI improves task performance while degrading underlying capability.

| Study | Finding | Statistic | Source |
|-------|---------|-----------|--------|
| Fernandes et al. CHI 2025 | LSAT performance gain | d = 1.23 | HCI research |
| Lee H.P. et al. CHI 2025 | Higher AI confidence → less critical thinking | β = -0.69, p<0.001 | CHI 2025 |
| Gerlich 2025 | AI use vs critical thinking correlation | r = -0.75 | Societies journal |
| Budzyń et al. Lancet 2025 | Endoscopist skill degradation after AI removal | 28.4% → 22.4% ADR (20% decline), p=0.0089 | Lancet |
| Kosmyna et al. MIT 2025 | Recall failure for AI-assisted content | 83% couldn't recall | MIT Media Lab |

**Note**: β = -0.69 (Lee) and r = -0.75 (Gerlich) are DIFFERENT statistics from DIFFERENT studies. Both independently confirm the negative relationship.

**Design implication**: Extensions must preserve capability, not just boost performance.

---

## Why Transparency and Control Matter

### The Blaurock Meta-Analysis

| Feature | Effect | Source |
|---------|--------|--------|
| Transparency | β = 0.415 (significant positive) | Blaurock et al. JSR 2024 |
| Process Control | β = 0.507 (significant positive) | Blaurock et al. JSR 2024 |
| Outcome Control | Significant positive | Blaurock et al. JSR 2024 |
| Engagement features | b = -0.555, p<.05 (negative for frequent users) | Blaurock et al. JSR 2024 |

**Source**: Blaurock, M. et al. (2024). AI-Based Service Experience Contingencies. Journal of Service Research. Meta-analysis of 106 studies.

**Design principle**: Show reasoning (β=0.415) and provide control (β=0.507). Don't ask questions (engagement b=-0.555 negative).

---

## Why Expertise Doesn't Buffer

| Study | Finding | Statistic |
|-------|---------|-----------|
| Fernandes et al. CHI 2025 | Higher AI literacy → worse metacognitive accuracy | r = 0.21, p<.01 |
| Demirer et al. 2024 | Junior developers gain more | 27-39% productivity |
| Demirer et al. 2024 | Senior developers gain less | 7-16% (non-significant) |

**Implication**: Calibration matters more than knowledge. Experts are not protected.

---

## Why Security Is Non-Negotiable

| Study | Finding | Statistic |
|-------|---------|-----------|
| Tihanyi et al. EMSE 2024 | AI-generated code vulnerabilities | 62.07% contain vulnerabilities |
| Fu et al. ACM TOSEM 2024 | Python snippets with CWE weaknesses | 29.5% |
| Fu et al. ACM TOSEM 2024 | JavaScript snippets with CWE weaknesses | 24.2% |

**Language-specific** (Perry et al. 2025):
- Python: 16-18% vulnerabilities (highest)
- TypeScript: 2.5% (lowest)

**Iteration effect**: Security degrades through iteration (3x increase from iteration 1-3 to 8-10).

---

## Why Mastery Orientation Protects

| Study | Finding | Statistic |
|-------|---------|-----------|
| ACU Research Bank 2025 | Mastery orientation → Critical thinking | OR = 35.7 |
| ACU Research Bank 2025 | Mastery orientation → Applied Knowledge | OR = 14.0 |
| ACU Research Bank 2025 | Mastery orientation → Learning Autonomy | OR = 17.2 |
| ACU Research Bank 2025 | Performance orientation → Critical thinking | Z = -6.295 (negative) |

**What OR = 35.7 means**: Mastery-oriented users are 35.7x more likely to demonstrate critical thinking. This is an extremely large effect.

| Orientation | Behavior | Outcome |
|-------------|----------|---------|
| **Mastery** | Learning focus, questions output | Protected—OR=35.7 |
| **Performance** | Output focus, accepts output | At risk—hollowing |

**Design implication**: Extensions should support mastery orientation (learning, questioning) not performance orientation (output, acceptance).

---

## The Core Paradox

**Short-term**: AI improves performance (d = 1.23)
**Long-term**: AI degrades capability (β = -0.69, r = -0.75, 20% skill decline)

This is the mechanism: improved performance removes the cognitive load that maintains skill.

---

## The Mitigation Path

| Factor | Effect | Mechanism |
|--------|--------|-----------|
| Mastery orientation | Protective (OR = 35.7) | User engages cognitively, questions output |
| Transparency | Protective (β = 0.415) | User sees reasoning, can learn patterns |
| Control | Protective (β = 0.507) | User guides process, retains agency |
| Engagement features | Null/negative (b = -0.555) | Conversation ≠ cognitive engagement |

---

## Statistical Glossary

| Statistic | What It Means | Scale |
|-----------|---------------|-------|
| **d** (Cohen's d) | Effect size: how many SDs apart | 0.2 small, 0.5 medium, 0.8 large |
| **β** (beta) | Regression coefficient | Standardized: -1 to +1 typical |
| **r** (correlation) | Strength of linear relationship | -1 to +1: 0.3 moderate, 0.5 strong |
| **OR** (odds ratio) | How much more likely | OR=35.7 means 35.7x more likely |

---

## Full Bibliography

- Blaurock, M. et al. (2024). AI-Based Service Experience Contingencies. Journal of Service Research. Meta-analysis of 106 studies.
- Budzyń, B. et al. (2025). Effect of AI-Assisted Colonoscopy on Adenoma Detection. Lancet Gastroenterology & Hepatology.
- Demirer et al. (2024). Three RCTs on developer productivity with AI.
- Fernandes et al. (2025). CHI 2025 paper on LSAT performance.
- Fu et al. (2024). Security vulnerabilities in AI code. ACM TOSEM.
- Gerlich (2025). AI and critical thinking. Societies journal.
- Kosmyna et al. (2025). AI-assisted writing and memory. MIT Media Lab.
- Lee H.P. et al. (2025). Impact of generative AI on critical thinking. CHI 2025.
- Perry et al. (2025). 7,703 AI-generated files security analysis.
- Tihanyi et al. (2024). AI code vulnerabilities. EMSE.

**Validation**: Triangulated across Claude Desktop + Gemini 3 Pro deep research (14+ agents, 4 phases). See `scratch/final-validated-synthesis.md`.

---

## Caveats

### Why Few Software Developer Studies?

| reality | implication |
|---------|-------------|
| AI coding tools are new (2021+) | Longitudinal studies don't exist yet |
| Developer productivity is hard to measure | Most studies use proxies (lines, completion time) |
| Companies don't publish internal data | RCTs are rare (Demirer exception) |
| Academic CS focuses on the AI, not the human | HCI studies lag behind |

**What we have**: Medical studies (colonoscopy, radiology), education studies, general population studies. These transfer imperfectly but the mechanisms (skill degradation, cognitive offloading) are domain-general.

**What we don't have**: 5-year longitudinal studies of developers using Copilot/Claude. These will come.

### Study Limitations

| study | limitation |
|-------|------------|
| **Budzyń (colonoscopy)** | Medical domain, may not transfer to cognitive work |
| **Gerlich (r=-0.75)** | Cross-sectional, can't prove causation |
| **Lee (β=-0.69)** | Self-reported critical thinking |
| **Blaurock (meta)** | Service contexts, not dev-specific |
| **Mastery (OR=35.7)** | Single study, needs replication |

### What This Means

The research provides **direction**, not **precision**. We know:
- Transparency and control help (strong evidence)
- Passive use risks capability (convergent evidence across domains)
- The exact effect sizes for developers are unknown

**Our approach**: Use the research to inform design principles, but don't over-claim precision we don't have. The methodology (transparency, control, learning) is robust even if exact numbers aren't.
