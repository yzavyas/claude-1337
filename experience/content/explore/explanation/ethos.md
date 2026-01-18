# Why This Approach

METR ran a randomized controlled trial with 16 experienced developers on mature codebases. AI tools made them 19% slower. They predicted being 24% faster.

That 43-point perception gap isn't an anomaly. It's the starting point for understanding how AI collaboration goes wrong - and what makes it go right.

---

## The productivity illusion

Developers believe AI helps. Measurements say otherwise.

Trust in AI coding accuracy dropped from 43% to 33% in one year (Stack Overflow 2024-2025). Adoption rose to 84% over the same period. People use tools they don't trust, perceive benefits they don't get.

The illusion has a mechanism. AI shifts work from generation to verification. Coding feels easier because the hard part - writing from scratch - is gone. But the new hard part - catching subtle errors in mostly-correct code - takes longer and demands more sustained attention.

30% of seniors edit AI output enough to offset time savings vs 17% of juniors. Seniors ship 2.5x more AI code to production despite lower trust. They can verify; juniors can't (Fastly 2025).

---

## The hollowing problem

Beyond productivity, there's capability.

| Study | Finding | Timeframe |
|-------|---------|-----------|
| Lee CHI 2025 | Higher AI confidence → less critical thinking (strong negative correlation) | Cross-sectional |
| Budzyń Lancet 2025 | 20% skill degradation in endoscopists after AI removal | 3 months |
| Kosmyna MIT 2025 | 83% couldn't recall content from AI-assisted writing | Immediate |
| Bastani PNAS 2025 | Unrestricted AI access → 17% worse exam performance | Single course |

The Budzyń study is the clearest. Endoscopists used AI-assisted polyp detection for 3 months. When the AI was removed, their detection rate had dropped from 28.4% to 22.4%. The skill atrophied measurably.

No equivalent study exists for developers - the technology is too new. But the cognitive mechanisms are the same. You don't maintain skills you stop exercising.

GitClear analyzed 211 million lines of code (2020-2024). Since AI adoption: 8x increase in code duplication. Refactoring dropped from 25% to 10% of changes. These are proxies, not proof of skill loss. But they point the same direction.

---

## What makes collaboration work

Blaurock et al. (Journal of Service Research, 2024) studied collaborative intelligence through interviews and two experiments with 654 professionals. What predicted good outcomes:

| Factor | Effect | What it means |
|--------|--------|---------------|
| Transparency | Strong positive | User sees AI reasoning → better outcomes |
| Process control | Strongest positive | User shapes how AI works → better outcomes |
| Outcome control | Strong positive | User shapes what AI produces → better outcomes |
| Reciprocity | Strong positive | User grows through collaboration → better outcomes |
| Engagement features | Significant negative | AI asks questions → worse for frequent users |

The engagement finding surprised people. Making AI conversational was supposed to build trust. Instead, for frequent AI users, engagement features significantly hurt perceived service quality.

The pattern: showing reasoning and giving control work. Prompting for interaction doesn't.

---

## Cognitive extensions

Clark and Chalmers (1998) proposed the extended mind thesis: cognitive processes don't stop at the skull. Otto uses a notebook to remember addresses. Inga uses biological memory. If we'd call Inga's process "remembering," we should call Otto's the same. The notebook is part of Otto's mind.

The parity principle: if a process were done in the head, we'd call it cognition. When external but functionally equivalent, it's cognitive extension.

This is why we call them cognitive extensions, not tools. They become part of how you think. The question isn't "is AI helpful?" but "what kind of mind are you building?"

---

## Complementary vs. substitutive

AI can extend capability three ways:

| Type | Human role | Outcome |
|------|------------|---------|
| **Complementary** | Learns, guides, improves through collaboration | Better with and without AI |
| **Constitutive** | Enables capability impossible alone | New capability emerges |
| **Substitutive** | Passively consumes output | Skills atrophy |

The distinction isn't what task you're doing. It's how you're doing it.

Code generation at scale is constitutive - no human types that volume. That's fine. The human maintains capability through transparency (seeing patterns in the output), control (architectural decisions), and reciprocity (growing more capable through the collaboration).

What makes something substitutive: accepting output without understanding. Treating AI as oracle rather than tool.

Bastani's PNAS study makes this concrete. Same AI, same students, different design:
- Unrestricted access: -17% exam performance
- Scaffolded access with guardrails: no significant harm

The tool didn't change. The interaction pattern did.

---

## The trust paradox

84% of developers use or plan to use AI coding tools. 33% trust their accuracy. 46% actively distrust. Only 60% view AI favorably, down from 77% in 2023 (Stack Overflow).

Seniors trust AI least (20% "high distrust") but ship the most AI code. They treat it as rough draft material - fast generation, heavy revision. The productivity comes from rapid correction, not AI correctness.

Juniors treat AI differently. 17% rely on AI code without significant editing. They view AI as teacher or oracle. This is the population most at risk of skill gaps - building habits without building the underlying capability to catch AI errors.

Explanations don't fix this. Bansal et al. (CHI 2021) found that detailed AI explanations increase overreliance. Making AI reasoning visible builds trust, which can mean appropriate calibration or inappropriate overtrust depending on the user.

What works: cognitive forcing functions. Requiring engagement before accepting output. It improves calibration but hurts user satisfaction. The interventions that work aren't the ones people like.

---

## Foundations compound

Why this matters: patterns established now get scaled up.

If the foundation is complementary - engineers learning, guiding, growing through collaboration - capability compounds. Each cycle builds on the last.

If the foundation is substitutive - engineers checking out, consuming, offloading without understanding - atrophy compounds. The strong negative correlation between AI confidence and critical thinking isn't a one-time effect. It's a trajectory.

AI capability is increasing faster than our frameworks for using it well. The METR finding (experienced developers slower with AI on mature codebases) suggests even sophisticated users struggle to integrate AI effectively. The tools are ahead of the practices.

Extensions designed now shape whether engineers in five years are more capable than ever or can't function without their tools.

---

## Design principles

From the research, four principles for extension design:

**Collaborative agency**: Both human and AI retain agency. Transparency requires AI that shows its work. Control requires AI that can be directed. Both showed strong positive effects in the research.

**Bidirectional learning**: The human learns, not just consumes. Reciprocity predicts good outcomes. Passive consumption predicts atrophy.

**Transparent abstractions**: Extensions should be readable, forkable, verifiable. Transparency works. Black boxes don't.

**Compounding engineering**: Each solution makes the next one faster. Write it down, build on it. (Every.to)

The goal: make the user more capable, not more dependent.

---

## Sources

**Productivity**
- METR (2025). Randomized controlled trial, 16 experienced developers. 19% actual slowdown, 24% predicted speedup.
- Stack Overflow Developer Survey (2024-2025). Trust accuracy: 43% → 33%. Adoption: 76% → 84%.
- Fastly (2025). Survey of 791 developers. 30% seniors offset time savings with edits vs 17% juniors; seniors ship 2.5x more AI code.

**Cognitive effects**
- Lee, H.P. et al. (2025). AI Confidence and Critical Thinking. CHI. Strong negative correlation.
- Kosmyna, N. et al. (2025). AI-Assisted Writing and Memory. MIT. 83% recall failure.
- Bastani, H. et al. (2025). Scaffolded vs Unrestricted AI in Education. PNAS. 17% performance drop.
- Bansal, G. et al. (2021). Explanations and Overreliance. CHI. Explanations increase reliance on incorrect AI.

**Skill degradation**
- Budzyń, B. et al. (2025). Endoscopic Skill After AI Exposure. Lancet. Detection rate dropped 28.4% → 22.4% after 3 months with AI.
- GitClear (2024). 211M lines analyzed. 8x code duplication, refactoring 25% → 10%.

**Collaboration design**
- Blaurock, M. et al. (2024). Designing Collaborative Intelligence Systems. Journal of Service Research. Two experiments with 654 professionals.

**Trust and verification**
- DORA Report (2024). 7.2% delivery stability decrease per 25% AI adoption.
- Veracode GenAI Security Report (2025). 40-50% vulnerability rate in AI-generated code.
