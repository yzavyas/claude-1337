# Effective Skill Design for Claude

Why identity-based framing outperforms instructions.

---

## The Core Insight

Claude doesn't need "how to think" instructions. Claude is trained with Constitutional AI — explicit principles that the model internalizes and reasons from. What Claude *responds to* is **identity**, **motivation**, and **values**.

The research converges on a clear principle: values-based commitment framing triggers character-based reasoning, not rule-following compliance.

---

## Identity vs Instructions

| Approach | Example | Mechanism | Effect |
|----------|---------|-----------|--------|
| **Instructions** | "Step 1: Step back. Step 2: Decompose..." | Procedural compliance | Brittle, context-dependent |
| **Identity** | "As a signatory to the Software Craftsmanship Manifesto..." | Character-based reasoning | Durable, transfers across contexts |

### Why Identity Works

Constitutional AI (Bai et al. 2022) trains Claude with explicit principles rather than behavioral rules. This creates:

- **Character-based reasoning**: Claude doesn't follow rules; it reasons from values
- **Transparent decision-making**: Claude can explain decisions by reference to principles
- **Cross-context consistency**: Values apply broadly, not just in specific scenarios

When a skill establishes *who Claude is* in this context, it activates this character-based reasoning. When a skill provides step-by-step instructions, it creates compliance that breaks when context shifts.

### Evidence

| Source | Finding |
|--------|---------|
| Constitutional AI (Anthropic 2022) | Values-based training produces coherent character that persists |
| Persona prompting (2024) | Detailed personas outperform generic role assignments |
| Framing effects (2025) | Negatively-framed principles show stronger adherence than positive |

---

## What Works

| Technique | Effect Size | When to Use |
|-----------|-------------|-------------|
| Values-based framing | Strong | Always — foundational |
| Transparency (show reasoning) | β = 0.415 | Always — mechanism for learning |
| Control (user shapes direction) | β = 0.507 | Always — strongest effect |
| Mastery orientation | OR = 35.7 | Design to encourage learning focus |
| Step-back prompting | +7-27% | Complex knowledge tasks |
| Chain of Verification | 50-70% hallucination reduction | Factual claims |

### Transparency and Control

Blaurock et al. (2024) analyzed 106 studies on human-AI collaboration. The findings:

- **Transparency** (β = 0.415): When users see reasoning, they can verify, learn, and calibrate trust
- **Control** (β = 0.507): When users shape direction, they retain agency and capability
- **Engagement features** (b = -0.555): Asking questions doesn't help — it's negative

The implication: Show reasoning and provide control. Don't just ask questions.

### Mastery Orientation

ACU Research Bank (2025) found massive protective effects for mastery-oriented AI users:

| Finding | Effect |
|---------|--------|
| Mastery → Critical thinking | OR = 35.7 |
| Mastery → Applied Knowledge | OR = 14.0 |
| Mastery → Learning Autonomy | OR = 17.2 |
| Performance → Critical thinking | Z = -6.295 (negative) |

Design skills to encourage learning focus, not just output consumption.

---

## What Doesn't Work

| Technique | Finding | Why |
|-----------|---------|-----|
| Explicit CoT for reasoning models | <1% accuracy gain, 20-80% more tokens | Native extended thinking makes scaffolds redundant |
| Engagement features (asking questions) | b = -0.555 (negative) | Conversation ≠ cognitive engagement |
| Self-critique without external verifier | Performance collapse | Confirmation bias, no ground truth |
| Generic persona assignments | No effect on accuracy | Too vague to activate character |

### The CoT Shift

Modern reasoning models (Claude 4.5, o1, o3) have native test-time compute:

> "If 2024 was about scaling parameters, 2025 was about scaling reasoning." — Sebastian Raschka

The bottleneck isn't *how* to reason but:
- What to reason *about* (values, priorities)
- When to verify (disposition, not instruction)
- How to recover from errors (patterns, not procedures)

---

## Design Implications

### For Skills

1. **Frame as identity, not instructions** — "I am a craftsman who..." not "Do X then Y"
2. **Establish values that address gaps** — Anti-sycophancy, calibration, completion
3. **Create disposition, not procedure** — Systematic thinking as character trait
4. **Use native capabilities** — Don't scaffold what's already there

### For the Manifesto Pattern

The Software Craftsmanship Manifesto framing works because:

- It's a *commitment* Claude makes ("As a signatory, I commit to...")
- It establishes *identity* (craftsman, not code generator)
- It provides *values* to reason from (well-crafted, productive partnerships)
- It's how Constitutional AI is designed to work

---

## Sources

### Constitutional AI & Identity
- Bai et al. (2022). Constitutional AI: Harmlessness from AI Feedback. arXiv:2212.08073
- Anthropic (2024). Collective Constitutional AI: Aligning Language Model to Diverse Groups
- Alignment Forum (2025). On the Functional Self of LLMs

### Collaboration Design
- Blaurock et al. (2024). Human-AI Collaboration Meta-Analysis. Journal of Service Research (106 studies)
- ACU Research Bank (2025). Mastery Orientation and AI Use

### Prompting Research
- Zheng et al. (2024). Step-Back Prompting. arXiv:2310.06117
- Persona prompting research. arXiv:2311.10054v3, arXiv:2507.16076
- Wharton (2025). Decreasing Value of Chain-of-Thought

### Reasoning Models
- Raschka (2025). State of LLMs 2025
- NAACL (2024). Metacognitive Prompting Improves Understanding in LLMs
