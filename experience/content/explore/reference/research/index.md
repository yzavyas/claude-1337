# Research

Validated findings supporting the ethos.

The research tells a story: AI tools promise productivity gains, but early evidence shows mixed results. More concerning are the cognitive effects — reduced critical thinking, memory formation, and skill retention. These aren't one-time effects; they compound over time. The final section shows what protects against these risks: transparency, control, and human agency in the collaboration.

---

## Deep Dives

- [Anti-Hollowing Framework](/explore/reference/research/anti-hollowing-framework) — How transparency and control protect capability

---

## Productivity

<details>
<summary><strong>METR 2025</strong> — AI tools slowed experienced developers by 19% on real coding tasks</summary>

Randomized controlled trial with 16 experienced open-source developers completing 246 real-world coding tasks. Screen recordings analyzed. Primary tools: Cursor Pro + Claude 3.5/3.7 Sonnet.

Developers predicted AI would make them 24% faster. They were actually 19% slower — a 43-point perception gap.

> "Surprisingly, we find that allowing AI actually increases completion time by 19% — AI tooling slowed developers down."

</details>

<details>
<summary><strong>Stack Overflow 2024-2025</strong> — Developers use tools they don't trust (trust fell, adoption rose)</summary>

Annual developer survey. Trust in AI coding accuracy dropped from 43% to 33%. Adoption rose from 76% to 84% over the same period.

People use tools they don't trust, perceiving benefits they don't actually get. Suggests a gap between expectation and reality.

</details>

<details>
<summary><strong>Fastly 2025</strong> — Senior developers question AI output more, ship more of it</summary>

Survey of 791 developers. 30% of seniors edit AI output enough to offset time savings (vs 17% of juniors). Despite lower trust, seniors ship 2.5x more AI-generated code to production.

Experience enables judgment about when AI output is trustworthy and when it needs work.

</details>

---

## Cognitive Effects

<details>
<summary><strong>Lee CHI 2025</strong> — Users more confident in AI show less critical thinking</summary>

Survey of 319 knowledge workers sharing 936 examples of GenAI use. Strong negative correlation between confidence in AI capabilities and critical thinking behavior.

The more people trust AI to handle tasks, the less they question its output.

</details>

<details>
<summary><strong>Kosmyna MIT 2025</strong> — 83% couldn't recall content written with AI assistance</summary>

Experimental study using EEG to measure brain activity during memory formation. Participants showed significantly reduced memory encoding for content created with AI assistance versus content written themselves.

The AI assistance prevented memory formation at a neurological level — they never learned the content in the first place.

</details>

<details>
<summary><strong>Bastani PNAS 2025</strong> — Unrestricted AI access hurt learning; scaffolded use showed no harm</summary>

Large-scale RCT with nearly 1,000 Turkish high school students across four 90-minute sessions. Students with unrestricted ChatGPT access scored 17% worse on unassisted final exams compared to control group.

Students with scaffolded AI (guardrails and structure) showed no significant difference from control. How you use it determines whether it helps or hurts.

</details>

<details>
<summary><strong>Bansal CHI 2021</strong> — AI explanations increase blind trust, not understanding</summary>

User studies testing whether explanations help humans evaluate AI recommendations. Explanations increased acceptance of AI suggestions regardless of whether they were correct.

When AI was right, performance improved slightly. When AI was wrong, performance degraded. Explanations created trust without calibration.

</details>

---

## Skill Degradation

<details>
<summary><strong>Budzyń Lancet 2025</strong> — 20% skill degradation after 3 months with AI</summary>

Crossover randomized controlled trial with endoscopists. After 3 months of AI-assisted colonoscopy, physicians' adenoma detection rate dropped from 28.4% to 22.4% when the AI was removed.

The skill atrophied measurably. You don't maintain skills you stop exercising.

</details>

<details>
<summary><strong>GitClear 2024</strong> — Code duplication increased 8x since AI coding tools adoption</summary>

Analysis of 211 million lines of code committed between 2020-2024. Copy-paste duplication within codebases increased 8-fold. Refactoring work dropped from 25% to 10% of changes.

Suggests developers accepting AI output without understanding or adapting it to existing patterns.

</details>

---

## Collaboration Design

<details>
<summary><strong>Blaurock JSR 2024</strong> — Transparency and control matter more than engagement features</summary>

Literature review + 14 interviews + two experiments with 654 professionals (financial services and HR).

**Key findings:**
- **Transparency** (show reasoning) — strong positive effect on outcomes
- **Process control** (let user steer how) — strongest positive effect
- **Outcome control** (let user steer what) — strong positive effect
- **Engagement features** (system prompts for feedback) — significant negative effect for experienced users

> "Engagement, for example, through asking for user feedback, is perceived by employees as effortful rather than empowering."

The insight: Show your reasoning, give them control, don't interrupt with engagement theater.

</details>

---

Full citations in [bibliography](/explore/reference/bibliography).
