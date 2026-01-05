# research

empirical foundations for cognitive extension design

---

## human-AI collaboration: what the research says

### the meta-analysis (flagship study)

**vaccaro, m., almaatouq, a., & malone, t. w. (2024).** when combinations of humans and AI are useful: a systematic review and meta-analysis. *nature human behaviour*, 8(12), 2293-2303.

- **106 experimental studies**, 370 effect sizes
- preregistered systematic review (highest methodological rigor)
- databases: ACM digital library, AIS eLibrary, web of science

| finding | implication |
|---------|-------------|
| human-AI combos often perform **worse** than best alone (g = -0.23) | don't assume collaboration always helps |
| **content creation**: performance gains | skills for writing, building, creating |
| **decision-making**: performance losses | avoid skills that make decisions for user |
| synergy is rare; augmentation is common | design for augmentation, not replacement |

**critical quote:** "there's a prevailing assumption that integrating AI into a process will always help performance — but we show that that isn't true."

### implications for cognitive extensions

the meta-analysis reframes what skills should do:

| task type | collaboration outcome | skill design |
|-----------|----------------------|--------------|
| content creation | **gains** | provide patterns, templates, reference material |
| decision-making | **losses** | provide frameworks, NOT decisions |
| subtask assistance | **gains** | handle specific subtasks, not entire workflows |

**design principle:** skills should extend knowledge and enable human decisions, not make decisions for the user.

---

## motivation and autonomy

### performance vs motivation tradeoff

**scientific reports (nature), april 2025.** human-generative AI collaboration enhances task performance but undermines human's intrinsic motivation.

- **N = 3,562 participants** across four experimental studies
- professional work settings, controlled design

| finding | cognitive extension implication |
|---------|--------------------------------|
| immediate performance enhanced | short-term gains are real |
| gains **don't transfer** to solo work | dependency risk is real |
| intrinsic motivation **decreases** | over-reliance harms long-term capability |
| sense of control increases when transitioning away | autonomy matters |

**theoretical framework:** self-determination theory (SDT)
- intrinsic motivation requires: autonomy, relatedness, competence
- AI collaboration can diminish perceived autonomy when AI overrides human decision-making

### co-creation vs editing

**scientific reports (nature), august 2024.** establishing the importance of co-creation and self-efficacy in creative collaboration with artificial intelligence.

| role | creativity outcome |
|------|-------------------|
| **editing** AI output | creativity deficit |
| **co-creating** with AI | deficit dissipates |

**mechanism:** creative self-efficacy is the key. people must occupy the role of **co-creator**, not **editor**.

### implications for cognitive extensions

| principle | implementation |
|-----------|----------------|
| preserve autonomy | skills provide knowledge, user decides |
| enable co-creation | decision frameworks, not decisions |
| avoid dependency | don't do things user should learn |
| maintain competence | explain patterns, don't just apply them |

**design principle:** skills should make users more capable, not more dependent.

---

## trust and appropriate reliance

### the over-reliance problem

**computers in human behavior, 2024.** trust and reliance on AI — an experimental study on the extent and costs of overreliance on AI.

| finding | risk |
|---------|------|
| users over-rely to their **own detriment** | personal harm |
| mere "AI" label causes over-reliance | labeling effect |
| over-reliance persists even when **contradicting context** | judgment override |
| third parties affected by over-reliance | broader harm |

### cognitive offloading correlation

from multiple 2024-2025 studies:

| metric | correlation with critical thinking |
|--------|-----------------------------------|
| cognitive offloading to AI | **r = -0.75** (strong negative) |
| younger participants | more dependent, lower critical thinking |
| higher education | mitigates negative effects |

### explainability paradox

**CHI 2021.** does the whole exceed its parts? the effect of AI explanations on complementary team performance.

| finding | implication |
|---------|-------------|
| explanations **don't increase** complementarity | transparency alone isn't enough |
| explanations increase acceptance **regardless of correctness** | can cause over-reliance |
| trust miscalibration results | explanations can hurt |

**scientific reports (nature), december 2024.** explainable AI improves task performance in human-AI collaboration.

| finding | condition |
|---------|-----------|
| visual heatmaps improve performance | when experts can **validate** against domain knowledge |
| cross-domain benefits | manufacturing, medical inspection |

**resolution:** explanations help when they enable **validation**, not when they just increase **acceptance**.

### implications for cognitive extensions

| principle | implementation |
|-----------|----------------|
| calibrated trust | acknowledge skill limitations |
| validation-enabling | show reasoning, not just conclusions |
| critical engagement | prompt evaluation, not blind acceptance |
| appropriate reliance | clear "use when" boundaries |

**design principle:** skills should enable validation, not demand trust.

---

## creativity and diversity

### the creativity paradox

**science advances, 2024.** generative AI enhances individual creativity but reduces the collective diversity of novel content.

| dimension | effect |
|-----------|--------|
| **individual** creativity | enhanced |
| **collective** diversity | reduced |
| anchoring on AI ideas | reduces exploration |

**tang et al. (2024) meta-analysis:**

| model | creative advantage (effect size) |
|-------|----------------------------------|
| GPT-4 | d = 0.41 (moderate) |
| GPT-3.5 | d = 0.18 (small) |
| AI excels at | fluency (quantity of ideas) |
| humans excel at | diversity of ideas |

### implications for cognitive extensions

| principle | implementation |
|-----------|----------------|
| preserve diversity | provide options, not single answers |
| avoid anchoring | present alternatives, tradeoffs |
| enable exploration | decision frameworks over decisions |
| maintain human creativity | patterns as starting points, not endpoints |

**design principle:** skills should expand possibility space, not constrain it.

---

## software engineering research

### github copilot productivity

**ziegler et al. (2024).** measuring github copilot's impact on productivity. *communications of the ACM*, 67(3), 54-63.

| finding | implication |
|---------|-------------|
| productivity is **multidimensional** | can't be summarized by single metric |
| experienced developers | less likely to write "better" code with copilot |
| junior developers | higher perceived productivity gains |
| acceptance rate varies | skill level affects appropriate use |

### metacognitive skills matter

**ACM ICER 2025.** the effects of github copilot on computing students' programming effectiveness, efficiency, and processes in brownfield coding tasks.

| metacognitive skills | AI assistance outcome |
|---------------------|----------------------|
| strong | enhanced performance |
| weak | **negatively impacted** |

### implications for cognitive extensions

| principle | implementation |
|-----------|----------------|
| skill-appropriate assistance | different patterns for different expertise levels |
| metacognitive support | explain "why", not just "what" |
| avoid deskilling | don't bypass foundational understanding |
| context-aware | brownfield vs greenfield considerations |

**design principle:** skills should augment existing capability, not substitute for learning.

---

## distributed cognition

### AI as social forcefield

**riedl, c., savage, s., & zvelebilova, j. (2024).** AI's social forcefield: reshaping distributed cognition in human-AI teams. arXiv:2407.17489

AI shapes:
- how people **speak**
- how they **think**
- what they **attend to**
- how they **relate to each other**

| effect | valence |
|--------|---------|
| enables efficient collaboration | positive |
| can erode epistemic diversity | negative |
| can undermine natural alignment | negative |

**critical quote:** "AI not merely as a tool but as a social forcefield that reorganizes the distributed dynamics of collective intelligence."

### implications for cognitive extensions

| principle | implementation |
|-----------|----------------|
| preserve epistemic diversity | multiple perspectives in skills |
| enable natural alignment | don't force patterns |
| aware of shaping effects | skills shape how users think |
| maintain human agency | co-creation, not automation |

**design principle:** skills shape cognition; design with that responsibility.

---

## cognitive vs operational extensions

the research applies differently depending on extension type:

### cognitive extensions

extensions that extend cognition — where human-AI collaboration research directly applies:

| modality | extends | research applicability |
|----------|---------|----------------------|
| **skills** | knowledge | full — content creation, autonomy, trust, diversity |
| **agents** | reasoning | full — delegation, over-reliance, distributed cognition |
| **MCP** | reach | full — trust calibration, appropriate reliance, capability |

### operational extensions

extensions that provide automation — research applies partially or tangentially:

| modality | provides | research applicability |
|----------|----------|----------------------|
| **commands** | efficiency | partial — autonomy tradeoffs, but mostly just macros |
| **hooks** | triggers | minimal — passive injection, not active collaboration |

---

## implications for cognitive extension design

### skills (knowledge extension)

| research finding | implication | affordance |
|-----------------|-------------|------------|
| content creation > decision-making (vaccaro 2024) | provide patterns, not conclusions | decision frameworks enable user judgment |
| co-creation > editing (nature 2024) | user as co-creator, not consumer | explain reasoning, invite modification |
| collective diversity at risk (science advances 2024) | present alternatives, tradeoffs | avoid single "right answer" |
| metacognitive skills determine benefit (ICER 2025) | explain "why", not just "what" | build understanding, not dependency |

**considerations:**
- skills shape how users think (distributed cognition)
- over-reliance correlates with reduced critical thinking (r = -0.75)
- gains don't transfer to independent work without understanding

### agents (reasoning extension)

| research finding | implication | affordance |
|-----------------|-------------|------------|
| synergy rare, augmentation common (vaccaro 2024) | design for augmentation, not replacement | agents assist, don't decide |
| over-reliance to own detriment (CHB 2024) | explicit boundaries on agent authority | clear scope, user validates |
| AI as social forcefield (riedl 2024) | agents reshape team cognition | design with shaping responsibility |
| autonomy required for motivation (SDT 2025) | preserve user control | agent proposes, user disposes |

**considerations:**
- delegated reasoning creates trust dependencies
- agent outputs need validation affordances
- epistemic diversity can erode with agent use

### MCP (reach extension)

| research finding | implication | affordance |
|-----------------|-------------|------------|
| trust calibration matters (2024) | surface data provenance | show sources, confidence |
| appropriate reliance varies (2025) | context-aware trust signals | indicate reliability |
| capability extension ≠ cognitive extension | tools extend reach, not replace judgment | user interprets, tool fetches |

**considerations:**
- external data requires different trust model than internal reasoning
- MCP extends what's possible, not what's wise
- user must evaluate relevance of retrieved information

---

## design principles hierarchy

from the 2024-2025 research, principles emerge in priority order:

### tier 1: foundational (non-negotiable)

| principle | research basis | applies to |
|-----------|---------------|------------|
| **augment, don't replace** | vaccaro 2024: synergy rare | skills, agents, MCP |
| **preserve autonomy** | SDT 2025: autonomy → motivation | skills, agents |
| **enable co-creation** | nature 2024: co-creation > editing | skills, agents |

### tier 2: trust (critical for adoption)

| principle | research basis | applies to |
|-----------|---------------|------------|
| **enable validation** | CHI 2021: validation > acceptance | skills, agents, MCP |
| **calibrate reliance** | CHB 2024: over-reliance harms | agents, MCP |
| **maintain critical thinking** | cognitive offloading r = -0.75 | skills, agents |

### tier 3: growth (long-term capability)

| principle | research basis | applies to |
|-----------|---------------|------------|
| **support metacognition** | ICER 2025: skills determine benefit | skills |
| **preserve diversity** | science advances 2024: collective risk | skills, agents |
| **avoid dependency** | nature 2025: gains don't transfer | skills, agents |

---

## how claude-1337 applies this

### the observability advantage

the research identifies a critical gap: traditional plugin systems (compiled bundles, deep dependencies, opaque behavior) prevent the validation that makes AI collaboration safe.

| research finding | traditional plugins | claude-1337 approach |
|------------------|--------------------|-----------------------|
| validation enables appropriate trust (CHI 2021) | black box, can't validate | plaintext markdown, fully readable |
| metacognitive skills determine benefit (ICER 2025) | "just install and use" | read, understand, learn patterns |
| cognitive offloading harms critical thinking (r = -0.75) | pure execution | engagement through comprehension |
| autonomy → motivation (SDT 2025) | dependency lock-in | self-contained, forkable |
| trust calibration requires understanding | reputation-based trust | inspection-based trust |

### self-contained design

instead of enforced dependencies:
```json
// NOT this
{ "dependencies": { "core-1337": "^1.0.0" } }
```

we use documented relationships:
```markdown
<!-- This -->
Works best with core-1337 installed.
Everything you need is in this file.
```

this enables:
- complete transparency (no hidden behavior)
- immediate comprehensibility (no dependency trees)
- full user control (fork and modify freely)
- appropriate trust (verify before relying)

### skill design

| principle | implementation |
|-----------|----------------|
| augment, don't replace | decision **frameworks**, not decisions |
| enable validation | "use when:" clauses, explicit boundaries |
| support metacognition | explain patterns, not just apply them |
| preserve diversity | present tradeoffs, not single answers |
| observable by default | everything in readable SKILL.md |

### agent design

| principle | implementation |
|-----------|----------------|
| preserve autonomy | agents propose, users validate |
| calibrate reliance | explicit scope boundaries |
| enable co-creation | agents as collaborators, not oracles |
| glass box reasoning | explain agent decisions |

### activation approach

| principle | implementation |
|-----------|----------------|
| preserve autonomy | motivation over mandate in hooks |
| calibrate reliance | 84% activation = appropriate non-activation exists |
| maintain critical thinking | evaluate relevance, don't force |

the 16% non-activation represents appropriate judgment — cases where extensions genuinely weren't relevant.

---

## skill activation research

### the activation problem

claude code skills have a ~20% baseline activation rate. you install a skill, ask a relevant question, and claude ignores it 80% of the time.

### root cause

from [lee han chung's deep dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/):

- **no algorithmic routing** — no regex, no embeddings, no classifiers
- **pure LLM reasoning** — claude reads skill descriptions and decides
- **description is everything** — the only signal for matching

### the forced evaluation study

from [scott spence's 200+ test study](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably):

| approach | activation rate | notes |
|----------|-----------------|-------|
| no intervention (baseline) | ~20% | default behavior |
| simple instruction | ~20% | doesn't help |
| LLM eval hook | 80% | asks claude to evaluate |
| forced eval hook | **84%** | explicit skill checking |

### the fix

explicit evaluation prompts that force claude to check skills before responding:

```
Before responding:
1. Check if any skills in <available_skills> are relevant
2. If relevant, invoke the Skill tool
3. Then respond using that knowledge
```

### what makes skills activate

| pattern | why it works |
|---------|--------------|
| "use when:" clause | explicit trigger conditions |
| specific tools/terms | "axum, tonic, sqlx" not "backend" |
| action verbs | "building", "debugging", "configuring" |
| front-loaded keywords | claude matches against description |

---

## validation framework

the claude-1337 eval framework validates activation rates by observing actual tool invocation, not asking claude's opinion.

### methodology

tests send prompts through the claude agent sdk and monitor the response stream for `ToolUseBlock` with `name == "Skill"`. this is ground truth — did claude actually invoke the skill?

```python
async for message in query(prompt=prompt, options=options):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                if block.name == "Skill":
                    skill_called = True  # ground truth
```

### interpreting results

| activation rate | meaning |
|-----------------|---------|
| 80%+ | skill description is working well |
| 50-79% | description needs improvement |
| <50% | description likely missing "use when:" or too vague |

---

## sources

### human-AI collaboration (tier 1 — highest quality)

- vaccaro, m., almaatouq, a., & malone, t. w. (2024). [when combinations of humans and AI are useful: a systematic review and meta-analysis](https://www.nature.com/articles/s41562-024-02024-1). *nature human behaviour*, 8(12), 2293-2303.
- [generative AI enhances individual creativity but reduces the collective diversity of novel content](https://www.science.org/doi/10.1126/sciadv.adn5290). *science advances*, 2024.
- [when and how artificial intelligence augments employee creativity](https://journals.aom.org/doi/10.5465/amj.2022.0426). *academy of management journal*, 2024.
- choudhary, v., et al. (2025). [human-AI ensembles: when can they work?](https://journals.sagepub.com/doi/10.1177/01492063231194968). *journal of management*.
- ziegler, a., et al. (2024). [measuring github copilot's impact on productivity](https://cacm.acm.org/research/measuring-github-copilots-impact-on-productivity/). *communications of the ACM*, 67(3), 54-63.

### motivation and autonomy (tier 1-2)

- [human-generative AI collaboration enhances task performance but undermines human's intrinsic motivation](https://www.nature.com/articles/s41598-025-98385-2). *scientific reports*, april 2025.
- [establishing the importance of co-creation and self-efficacy in creative collaboration with AI](https://www.nature.com/articles/s41598-024-69423-2). *scientific reports*, august 2024.
- [the impact of AI-assisted pair programming on student motivation](https://stemeducationjournal.springeropen.com/articles/10.1186/s40594-025-00537-3). *international journal of STEM education*, 2025.

### trust and reliance (tier 1-2)

- [trust and reliance on AI — an experimental study on overreliance](https://www.sciencedirect.com/science/article/pii/S0747563224002206). *computers in human behavior*, 2024.
- [explainable AI improves task performance in human-AI collaboration](https://www.nature.com/articles/s41598-024-82501-9). *scientific reports*, december 2024.
- [does the whole exceed its parts? the effect of AI explanations on complementary team performance](https://dl.acm.org/doi/10.1145/3411764.3445717). *CHI 2021*.
- gerlich, m. (2025). [AI tools in society: impacts on cognitive offloading and the future of critical thinking](https://www.mdpi.com/2075-4698/15/1/6). *societies*, 15(1), 6.
- [the amplifying effect of explainability in AI-assisted decision-making in groups](https://dl.acm.org/doi/10.1145/3706598.3713534). *CHI 2025*.

### software engineering (tier 1)

- liang, j. t., yang, c., & myers, b. a. (2024). a large-scale survey on the usability of AI programming assistants. *IEEE/ACM ICSE 2024*.
- [human-AI collaboration in software development: a mixed-methods study](https://dl.acm.org/doi/abs/10.1145/3696630.3730566). *FSE 2024*.
- [the effects of github copilot on computing students' programming effectiveness](https://dl.acm.org/doi/full/10.1145/3702652.3744219). *ACM ICER 2025*.
- METR (2025). [measuring the impact of early-2025 AI on experienced open-source developer productivity](https://arxiv.org/abs/2507.09089). arXiv:2507.09089.

### distributed cognition (tier 2)

- riedl, c., savage, s., & zvelebilova, j. (2024). [AI's social forcefield: reshaping distributed cognition in human-AI teams](https://arxiv.org/abs/2407.17489). arXiv:2407.17489.
- [human-AI collaboration is not very collaborative yet](https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2024.1521066/full). *frontiers in computer science*, 2024.
- lee et al. (2025). [the impact of generative AI on critical thinking](https://dl.acm.org/doi/10.1145/3706598.3713778). *CHI 2025*.
- [epistemic diversity and knowledge collapse in large language models](https://arxiv.org/abs/2510.04226). arXiv, 2025.

### cognitive extension theory (tier 1-2)

- clark, a. (2025). extending minds with generative AI. *nature communications*.
- [homogenizing effect of LLMs on cognitive diversity](https://www.arxiv.org/pdf/2508.01491). arXiv, 2025.
- [the value of disagreement in AI design, evaluation, and alignment](https://dl.acm.org/doi/10.1145/3715275.3732146). *ACM FAccT 2025*.

### skill activation

- [anthropic: equipping agents with skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — official documentation
- [scott spence: skills activation study](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably) — 200+ test validation
- [lee han chung: skills deep dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) — how routing works

### theoretical foundations

- clark, a., & chalmers, d. (1998). [the extended mind](https://www.alice.id.tue.nl/references/clark-chalmers-1998.pdf). *analysis*, 58(1), 7-19.
- nonaka, i. (1991). the knowledge-creating company. *harvard business review*.
- hutchins, e. (1995). *cognition in the wild*. MIT press.
- popper, k. (1959). *the logic of scientific discovery*. — scientific method
- aristotle. *posterior analytics*. — first principles reasoning
- dhuliawala et al. (2023). [chain-of-verification reduces hallucination](https://arxiv.org/abs/2309.11495). arXiv:2309.11495.

### software craftsmanship

- [software craftsmanship manifesto](https://manifesto.softwarecraftsmanship.org/) (2009)
- martin, r. c. (2008). *clean code*
- mancuso, s. (2014). *the software craftsman*

### design principles

- mariani, r. (microsoft). pit of success / performance culture
- shingo, s. (1986). *zero quality control: source inspection and the poka-yoke system*. — mistake-proofing
- minsky, y. (jane street). effective ML — make illegal states unrepresentable
- king, a. (2019). [parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/)
