# Research Foundations

Academic backing for why these principles matter. Load when you want to understand the evidence, not for everyday use.

---

## Why Collaboration Design Matters

### The Blaurock Meta-Analysis

What makes AI collaboration complementary rather than substitutive?

| Feature | Effect | Implication |
|---------|--------|-------------|
| **Transparency** | β = 0.415 (strong positive) | Show reasoning, not just answers |
| **Process Control** | β = 0.507 (strong positive) | Human shapes HOW work is done |
| **Outcome Control** | Significant positive | Human shapes WHAT is produced |
| **Engagement features** | b = -0.555 (negative for frequent users) | Don't prompt curiosity — make reasoning unavoidable |

**Source:** Blaurock, M. et al. (2024). AI-Based Service Experience Contingencies. Journal of Service Research. Meta-analysis of 106 studies.

**Design principle:** Show reasoning and provide control. These are the mechanisms that preserve capability.

---

## The Capability Atrophy Risk

### Convergent Evidence

| Study | Finding | Statistic | Domain |
|-------|---------|-----------|--------|
| Gerlich 2025 | AI use correlates with critical thinking decline | r = -0.75 | General population |
| Lee et al. CHI 2025 | Higher AI confidence → less critical thinking | β = -0.69, p<0.001 | Users |
| Budzyń et al. Lancet 2025 | Skill degradation after AI removal | 28.4% → 22.4% ADR (20% decline) | Medical (colonoscopy) |
| Kosmyna et al. MIT 2025 | Recall failure for AI-assisted content | 83% couldn't recall | Writing |

**Note:** These are correlations and controlled studies, not proof of causation. But the convergent pattern across domains suggests real risk.

**What this means:** Passive consumption without transparency or engagement leads to capability decline. The mitigation is transparency and control (Blaurock findings above).

---

## Why Expertise Doesn't Protect

| Study | Finding | Statistic |
|-------|---------|-----------|
| Fernandes et al. CHI 2025 | Higher AI literacy → worse metacognitive accuracy | r = 0.21, p<.01 |
| Demirer et al. 2024 | Junior developers gain more from AI | 27-39% productivity |
| Demirer et al. 2024 | Senior developers gain less | 7-16% (non-significant) |

**Implication:** Knowing about AI doesn't protect against miscalibration. Experts are not immune.

---

## Mastery Orientation as Protection

| Study | Finding | Statistic |
|-------|---------|-----------|
| ACU Research Bank 2025 | Mastery orientation → Critical thinking | OR = 35.7 |
| ACU Research Bank 2025 | Mastery orientation → Applied Knowledge | OR = 14.0 |
| ACU Research Bank 2025 | Performance orientation → Critical thinking | Z = -6.295 (negative) |

**What OR = 35.7 means:** Mastery-oriented users are 35.7x more likely to demonstrate critical thinking.

| Orientation | Behavior | Outcome |
|-------------|----------|---------|
| **Mastery** | Learning focus, questions output | Protected |
| **Performance** | Output focus, accepts output | At risk |

**Design implication:** Collaboration should support learning and questioning, not just output delivery.

---

## The Reasoning Techniques Landscape (2025)

### What Actually Helps

| Technique | When it helps | Evidence |
|-----------|---------------|----------|
| **Chain of Verification** | Factual accuracy | 50-70% hallucination reduction (Dhuliawala 2023) |
| **Step-back prompting** | Abstract reasoning | +7-27% on knowledge tasks (Zheng 2023) |
| **Self-consistency** | Math/logic | +12-18% on reasoning benchmarks (Wang 2023) |

### What's Now Built-In

| Capability | Status in Modern Claude |
|------------|------------------------|
| Extended thinking | Native (triggered by "think") |
| Long-horizon reasoning | Native ("exceptional state tracking") |
| Subagent orchestration | Native (proactive delegation) |

### The Diminishing Returns Finding

> "For reasoning models, added benefits of explicit CoT are negligible and may not justify 20-80% increase in processing time."

**Source:** Wharton Generative AI Labs (Meincke et al. 2025)

**Implication:** Don't add reasoning scaffolds for their own sake. Modern Claude reasons well natively. Focus on transparency, verification, and collaboration design instead.

---

## Statistical Reference

| Statistic | What it means | Scale |
|-----------|---------------|-------|
| **β** (beta) | Regression coefficient — how much Y changes per unit X | Standardized: -1 to +1 typical |
| **r** (correlation) | Strength of linear relationship | -1 to +1: 0.3 moderate, 0.5 strong |
| **OR** (odds ratio) | How much more likely | OR=35.7 means 35.7x more likely |
| **d** (Cohen's d) | Effect size in standard deviations | 0.2 small, 0.5 medium, 0.8 large |

---

## Key Sources

### Collaboration Design
- Blaurock, M. et al. (2024). AI-Based Service Experience Contingencies. Journal of Service Research.

### Capability Effects
- Gerlich (2025). AI and critical thinking. Societies journal.
- Lee H.P. et al. (2025). Impact of generative AI on critical thinking. CHI 2025.
- Budzyń, B. et al. (2025). Effect of AI-Assisted Colonoscopy. Lancet Gastroenterology.
- Kosmyna et al. (2025). AI-assisted writing and memory. MIT Media Lab.

### Reasoning Techniques
- Dhuliawala et al. (2023). Chain-of-Verification. ACL 2024.
- Zheng et al. (2023). Step-Back Prompting. ICLR 2024.
- Meincke et al. (2025). Decreasing Value of CoT. Wharton.

### Compound Engineering
- Every.to (2025). Compound Engineering: How Every Codes With Agents.

---

## The Summary

**What the research says:**
1. Transparency and control make collaboration complementary (strong evidence)
2. Passive use risks capability decline (convergent evidence)
3. Mastery orientation protects (strong evidence)
4. Modern reasoning models need less explicit scaffolding (recent evidence)

**What this means for practice:**
- Show reasoning → human learns
- Provide control → human retains agency
- Support questioning → mastery orientation
- Don't over-scaffold → Claude 4.5 reasons natively
