# Sources

Academic references for verification and deeper learning. This is for humans who want to trace claims back to primary sources.

---

## Reasoning Architectures

### Chain-of-Thought Prompting

**Wei, J., Wang, X., Schuurmans, D., et al. (2022).** "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *NeurIPS 2022*.

The foundational paper showing that including intermediate reasoning steps in few-shot exemplars unlocks multi-step reasoning. Tested across LaMDA-137B, PaLM-540B, and GPT-3 on GSM8K math problems. Key finding: capability is latent in large models but requires structural scaffolding to emerge.

**Limitation noted:** ~2% of correct answers came from incorrect reasoning chains.

---

### Tree-of-Thoughts

**Yao, S., Yu, D., Zhao, J., et al. (2023).** "Tree of Thoughts: Deliberate Problem Solving with Large Language Models." *NeurIPS 2023 Oral*.

Generalizes chain-of-thought to search trees with LLM-based thought generation and evaluation. On the Game of 24, achieved 74% vs 4% for GPT-4 with standard CoT — an 18.5x improvement. The paper introduced breadth-first and depth-first search strategies with backtracking.

---

### Self-Consistency

**Wang, X., Wei, J., Schuurmans, D., et al. (2023).** "Self-Consistency Improves Chain of Thought Reasoning in Language Models." *ICLR 2023*.

Showed that sampling multiple reasoning paths and using majority voting improves accuracy by 12-18% on reasoning benchmarks. Key insight: different reasoning paths make different errors, so voting catches inconsistent mistakes. Limitation: cannot catch systematic biases where all paths err the same way.

---

### Graph-of-Thoughts

**Besta, M., Blach, N., Kubicek, A., et al. (2024).** "Graph of Thoughts: Solving Elaborate Problems with Large Language Models." *AAAI 2024*.

Extended tree search to arbitrary directed graphs, enabling thought aggregation and refinement loops. On sorting 128 elements, achieved 62% quality improvement over ToT with 31% cost reduction.

---

### Decomposition Strategies

**Zhou, D., Schärli, N., Hou, L., et al. (2023).** "Least-to-Most Prompting Enables Complex Reasoning in Large Language Models." *ICLR 2023*.

Addresses compositional generalization by explicitly decomposing problems and solving subproblems sequentially. Achieved 99.7% on SCAN versus near-random CoT performance.

**Yao, S., Zhao, J., Yu, D., et al. (2023).** "ReAct: Synergizing Reasoning and Acting in Language Models." *ICLR 2023 Notable Top 5%*.

Interleaves reasoning with external tool use. +34% absolute success rate on ALFWorld. Reduces hallucination through API grounding.

---

## Verification Techniques

### Chain-of-Verification

**Dhuliawala, S., Komeili, M., Xu, J., et al. (2024).** "Chain-of-Verification Reduces Hallucination in Large Language Models." *ACL 2024 Findings*. Meta AI.

Four-stage verification pipeline: generate → plan verification questions → answer independently → synthesize. The critical finding: factored execution (answering verification questions without access to the original response) dramatically outperforms joint verification. Achieved 50-70% hallucination reduction on Wikidata, MultiSpanQA, and biography generation tasks.

---

### SelfCheckGPT

**Manakul, P., Liusie, A., & Gales, M. (2023).** "SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models." *EMNLP 2023*. Cambridge.

Black-box hallucination detection through sampling consistency. Intuition: factual knowledge produces consistent samples; hallucinations diverge. Using 20 samples with LLM-based consistency prompting, achieved AUC-PR 93.42% on WikiBio. Cannot catch consistent hallucinations.

---

### FActScore

**Min, S., Krishna, K., Lyu, X., et al. (2023).** "FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation." *EMNLP 2023*. UW/Meta.

Decomposes generated text into atomic claims and verifies each against Wikipedia. Finding: ChatGPT achieves only 58% FActScore on biographies. Automated evaluation has <2% error rate vs human annotation.

---

### Semantic Entropy

**Farquhar, S., Kossen, J., Kuhn, L., & Gal, Y. (2024).** "Detecting Hallucinations in Large Language Models Using Semantic Entropy." *Nature, 630*, 625-630.

State-of-the-art uncertainty detection. Computes entropy in meaning space rather than token space using NLI models for semantic clustering. High semantic entropy indicates genuine uncertainty. Achieved state-of-the-art AUROC across GPT-4, LLaMA 2, and Falcon.

---

## Metacognition & Self-Correction

### Reflexion

**Shinn, N., Cassano, F., Gopinath, A., et al. (2023).** "Reflexion: Language Agents with Verbal Reinforcement Learning." *NeurIPS 2023*.

Verbal reinforcement learning through linguistic feedback stored in episodic memory. Architecture: actor generates outputs, evaluator provides feedback (often external), self-reflection converts sparse signals to insights. On HumanEval, achieved 91% pass@1 versus 80% GPT-4 baseline. Requires external feedback signals to work.

---

### Self-Correction Limitations

**Huang, J., Gu, S.S., Hou, L., et al. (2024).** "Large Language Models Cannot Self-Correct Reasoning Yet."

Critical finding: LLMs cannot reliably self-correct reasoning without external feedback. Intrinsic self-correction (without grounding) often degrades performance. "Try again" without new information doesn't work.

---

### Unfaithful Explanations

**Turpin, M., Michael, J., Perez, E., & Bowman, S. (2023).** "Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting." *NeurIPS 2023*.

Models sometimes reach correct answers through incorrect reasoning chains. The explanation isn't always faithful to how the model computed the answer. Implications for interpretability and trust.

---

### Confidence Calibration

**Tian, K., Mitchell, E., Yao, H., et al. (2023).** "Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models." *EMNLP 2023*.

Counterintuitive finding: for RLHF-tuned models, verbalized confidence is better calibrated than token probabilities. Prompting GPT-4 to state confidence achieved 50% reduction in Expected Calibration Error.

**Xiong, M., Hu, Z., Lu, X., et al. (2024).** "Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs." *ICLR 2024*.

LLMs are systematically overconfident when verbalizing — clustering at 80-100% confidence. All methods struggle with professional knowledge domains.

---

## Human-AI Collaboration

### Collaboration Design

**Blaurock, M., Čaić, M., Oertel, S., & Hollebeek, L.D. (2024).** "AI-Based Service Experience Contingencies: An Integrative Framework and Research Agenda." *Journal of Service Research*. Meta-analysis of 106 studies.

Key findings on what makes AI collaboration complementary rather than substitutive:
- Transparency: β = 0.415 (strong positive)
- Process control: β = 0.507 (strong positive)
- Outcome control: significant positive
- Engagement features: b = -0.555 (negative for frequent users)

Design principle: show reasoning and provide control.

---

### Interaction Patterns

**Gomez, G., Akhtar, F., Lee, A., et al. (2024).** "Taxonomy of Human-AI Interaction Patterns: A Systematic Review." *Frontiers in Computer Science*.

Systematic review of 105 articles. Finding: 67% of interaction sequences follow "AI-First Assistance" where AI generates and humans verify. True mixed-initiative collaboration remains rare.

---

### Capability Atrophy Risk

**Gerlich, M. (2025).** "AI and Critical Thinking." *Societies*.

Correlation between AI use and critical thinking: r = -0.75. Cross-sectional study.

**Lee, H.P., Sarkar, A., Tankelevitch, L., et al. (2025).** "Impact of Generative AI on Critical Thinking." *CHI 2025*.

Higher AI confidence correlates with less critical evaluation: β = -0.69, p < 0.001.

**Budzyń, B., et al. (2025).** "Effect of AI-Assisted Colonoscopy on Adenoma Detection." *Lancet Gastroenterology & Hepatology*.

Controlled study: endoscopists trained with AI assistance showed 20% skill degradation (28.4% → 22.4% ADR) when AI was removed.

**Kosmyna, N., et al. (2025).** "AI-Assisted Writing and Memory." *MIT Media Lab*.

83% of participants couldn't recall content they wrote with AI assistance.

---

### Mastery Orientation

**ACU Research Bank (2025).** Mastery vs performance orientation study.

Mastery orientation → Critical thinking: OR = 35.7
Mastery orientation → Applied knowledge: OR = 14.0
Performance orientation → Critical thinking: Z = -6.295 (negative)

Learners are 35.7× more likely to maintain critical thinking than output-focused users.

---

### Expertise Effects

**Fernandes, T., et al. (2025).** *CHI 2025*.

Higher AI literacy correlated with worse metacognitive accuracy: r = 0.21. The AI literacy paradox.

**Demirer, D., et al. (2024).** Productivity study.

Junior developers: 27-39% productivity gain from AI.
Senior developers: 7-16% (non-significant).

---

## Alignment & Interpretability

### Constitutional AI

**Bai, Y., Kadavath, S., Kundu, S., et al. (2022).** "Constitutional AI: Harmlessness from AI Feedback." *Anthropic*.

Principle-based self-critique and RLHF from AI feedback. Two-phase training: fine-tune on model-revised responses, then train preference model on AI-generated comparisons. Result: Pareto improvement — higher helpfulness AND harmlessness.

**Anthropic (2023).** "Collective Constitutional AI: Aligning a Language Model with Public Input."

~1,000 Americans drafted constitutional principles democratically. Resulting model showed less bias on BBQ benchmark while maintaining helpfulness.

---

### Direct Preference Optimization

**Rafailov, R., Sharma, A., Mitchell, E., et al. (2023).** "Direct Preference Optimization: Your Language Model is Secretly a Reward Model." *NeurIPS 2023*.

Eliminates RL loop by reparameterizing reward model. Matches or exceeds PPO-RLHF on sentiment, summarization, dialogue. Now used in Llama 3, GPT-4, Claude, Gemini.

---

### Mechanistic Interpretability

**Anthropic (2024).** "Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet."

Extracted 34 million interpretable features using sparse autoencoders. 70% rated interpretable by human evaluators. Features are abstract, multilingual, multimodal.

**Anthropic (2025).** "Circuit Tracing: Revealing Computational Graphs in Language Models."

Maps computational pathways using attribution graphs. Applied to Claude 3.5 Haiku. Reveals multi-step reasoning circuits. Limitation: succeeds on only ~25% of investigated prompts.

---

### Multi-Agent Debate

**Du, Y., Li, S., Torralba, A., et al. (2024).** "Improving Factuality and Reasoning in Language Models through Multiagent Debate." *ICML 2024*. MIT/Google DeepMind.

Multiple LLM instances propose, critique, and refine answers. ~50% → ~80% accuracy on arithmetic with 3 agents over 2 rounds.

---

## Reasoning Scaffolds (Diminishing Returns)

**Meincke, L., et al. (2025).** "The Decreasing Value of Chain-of-Thought in Reasoning Models." *Wharton Generative AI Labs*.

For modern reasoning models, added benefits of explicit CoT are negligible and may not justify 20-80% increase in processing time. Claude 4.5 and similar models reason well natively.

---

## Statistical Reference

| Statistic | Interpretation |
|-----------|----------------|
| **β (beta)** | Regression coefficient. β = 0.5 is moderate-to-strong. |
| **r (correlation)** | -1 to +1. 0.3 moderate, 0.5 strong, 0.7 very strong. |
| **OR (odds ratio)** | Likelihood multiplier. OR = 2 means 2× more likely. |
| **d (Cohen's d)** | Effect size in SDs. 0.2 small, 0.5 medium, 0.8 large. |
| **AUC-PR** | Area under precision-recall curve. Higher = better detection. |
