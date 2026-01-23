# Reasoning Techniques Deep Dive

Comprehensive reference for structured reasoning architectures. Load when you need detailed technique guidance beyond the SKILL.md summary.

---

## Structured Reasoning Landscape

Research on structured prompting has progressed from foundational Chain-of-Thought to increasingly sophisticated architectures that explicitly model search, decomposition, and verification.

**Key finding:** Emergent reasoning capabilities require both scale (>100B parameters) AND explicit structural scaffolding in prompts.

---

## Chain-of-Thought (CoT)

**Source:** Wei et al., NeurIPS 2022

Including intermediate reasoning steps in few-shot exemplars unlocks multi-step reasoning. Testing across LaMDA-137B, PaLM-540B, and GPT-3 showed state-of-the-art on GSM8K math problems with just 8 exemplars.

### Critical Limitations

| Limitation | Evidence |
|------------|----------|
| **Threshold effect** | Models <100B produce fluent but illogical chains |
| **Correct by chance** | ~2% of correct answers come from incorrect reasoning |
| **Unfaithful explanations** | Turpin et al. (NeurIPS 2023): models reach correct answers despite biased reasoning chains |

### When to Use

| Scenario | CoT Appropriate |
|----------|-----------------|
| Arithmetic, multi-step logic | Yes |
| Symbolic reasoning | Yes |
| Simple factual lookup | No (overkill) |
| Modern reasoning models | Diminishing returns |

---

## Tree-of-Thoughts (ToT)

**Source:** Yao et al., NeurIPS 2023 Oral

Generalizes CoT by modeling reasoning as a search tree with LLM-based thought generation and evaluation.

### Performance

**18.5x improvement** on Game of 24 (74% vs 4% for GPT-4 with CoT).

### How It Works

```
1. Generate candidate thoughts
2. Evaluate each thought (LLM scoring)
3. Expand promising branches (BFS/DFS)
4. Backtrack when needed
```

### Cost-Performance Tradeoff

Multiple LLM calls per node. GPT-4 generation paired with GPT-3.5 evaluation maintains performance while reducing costs.

### When to Use

| Scenario | ToT Appropriate |
|----------|-----------------|
| Problems requiring exploration | Yes |
| Constraint satisfaction | Yes |
| Planning with uncertainty | Yes |
| Simple sequential reasoning | No (use CoT) |

---

## Self-Consistency

**Source:** Wang et al., ICLR 2023

Sample multiple reasoning paths, select most frequent answer via majority voting.

### Performance

| Benchmark | Improvement |
|-----------|-------------|
| GSM8K (PaLM-540B) | +17.9% |
| AQuA | +12.2% |

### How It Works

```
1. Generate N reasoning paths (5-20)
2. Extract final answer from each
3. Majority vote
```

### Properties

| Property | Implication |
|----------|-------------|
| Parallelizable | Fast with batch inference |
| Composes with CoT | Works with few-shot and zero-shot |
| Catches inconsistent errors | Different paths catch different mistakes |
| Cannot catch systematic bias | All paths make same mistake |

### Default Configuration

5-10 samples for critical reasoning. More samples = higher accuracy but diminishing returns.

---

## Graph-of-Thoughts (GoT)

**Source:** Besta et al., AAAI 2024

Extends ToT to arbitrary directed graphs, enabling thought aggregation and refinement loops.

### Performance

On sorting 128 elements: **62% quality improvement over ToT with >31% cost reduction**.

### When to Use

Complex constraint satisfaction where thoughts can be combined, not just branched.

Requires domain-specific graph design.

---

## Decomposition Strategies

### Least-to-Most Prompting

**Source:** Zhou et al., ICLR 2023

Explicitly decompose problems and solve subproblems sequentially.

**Performance:** 99.7% on SCAN vs near-random CoT performance.

Addresses compositional generalization to harder problems than exemplars.

### ReAct

**Source:** Yao et al., ICLR 2023 Notable Top 5%

Interleaves reasoning with external tool use.

**Performance:** +34% absolute success rate on ALFWorld. Reduces hallucination through API grounding.

```
Thought → Action → Observation → Thought → ...
```

---

## Chain-of-Verification (CoVe)

**Source:** Dhuliawala et al., ACL 2024 Findings (Meta AI)

Four-stage pipeline for verification:

### The Pipeline

| Stage | Action |
|-------|--------|
| **Generate** | Initial response |
| **Plan** | Verification questions targeting specific claims |
| **Execute** | Answer each question INDEPENDENTLY (no access to initial response) |
| **Synthesize** | Correct based on verification answers |

### Critical Design Choice

**Factored execution is essential.** Joint verification (single prompt) performs worst. Independent verification achieves 50-70% hallucination reduction.

### Performance

| Task | Hallucination Reduction |
|------|------------------------|
| Wikidata list questions | 50-70% |
| MultiSpanQA | 50-70% |
| Long-form biography | 50-70% |

### Overhead

3-4x baseline inference (each verification question = separate call).

### Limitation

Relies on model's parametric knowledge. Cannot verify claims outside training data.

---

## SelfCheckGPT

**Source:** Manakul et al., EMNLP 2023

Black-box hallucination detection through sampling consistency.

### Intuition

Factual knowledge produces consistent samples. Hallucinations diverge.

### Method

1. Generate 20 stochastic samples
2. Use LLM-based consistency prompting
3. Inconsistent claims = likely hallucination

### Performance

**AUC-PR 93.42%** for non-factual sentence detection on WikiBio.

### Limitations

- Cannot catch consistent hallucinations
- Cannot catch facts requiring external verification
- 20x overhead

---

## Multi-Agent Debate

**Source:** Du et al., ICML 2024 (MIT/Google DeepMind)

Multiple LLM instances propose, critique, and refine answers through structured debate.

### Performance

~50% → ~80% accuracy on arithmetic with 3 agents over 2 rounds.

### Extensions

Tool-MAD (2025) integrates external retrieval: **35.5% improvement over standard multi-agent debate**.

### Overhead

6-30x (multiple agents × multiple rounds).

---

## Reflexion

**Source:** Shinn et al., NeurIPS 2023

Verbal reinforcement learning — reinforcing agents through linguistic feedback stored in episodic memory.

### Architecture

| Component | Role |
|-----------|------|
| Actor | Generates outputs |
| Evaluator | Provides feedback (often external: tests, verification) |
| Self-reflection | Converts sparse signals to actionable insights |

### Performance

**91% pass@1 on HumanEval** vs 80% GPT-4 baseline.

### Requirements

- Clear feedback signals exist
- Reasoning trace is recoverable
- Task within memory capacity

### Fails When

- Nuanced mathematical reasoning
- Credit assignment over long chains
- Tasks exceeding memory capacity

---

## Semantic Entropy

**Source:** Farquhar et al., Nature 2024

State-of-the-art hallucination detection by computing entropy in meaning space.

### Method

```
1. Sample 5+ responses
2. Cluster by semantic equivalence (NLI models)
3. Compute entropy over clusters
```

### Interpretation

| Pattern | Meaning |
|---------|---------|
| High semantic entropy | Genuine uncertainty (different answers) |
| Low entropy, high confidence | Likely reliable |
| Low entropy, low confidence | Investigate |

### Performance

State-of-the-art AUROC across GPT-4, LLaMA 2, Falcon.

### Overhead

~10x (multiple samples + NLI clustering).

---

## Decision Framework

### For Arithmetic and Multi-Step Reasoning

Start with CoT, add Self-Consistency (5-20 samples), majority vote.
Expected: +10-17% over greedy decoding.
Requirements: >100B parameters.

### For Factual Accuracy

Implement CoVe with factored execution.
For knowledge-intensive: combine with retrieval (CoV-RAG pattern).
Expected: 50-70% hallucination reduction at 3-4x cost.

### For High-Stakes Decisions

Layer Semantic Entropy for uncertainty quantification.
Confidence-gated human escalation at calibrated thresholds.
Maintain full audit trails.
Use verbalized confidence for RLHF models.

### For Code Generation

Deploy Reflexion with unit test feedback.
Expected: 3-5 iterations for convergence, 91% pass rates achievable.

### For Problems Requiring Exploration

Use ToT with BFS/DFS search.
Consider GoT for complex constraint satisfaction.
Accept 5-20x computational overhead.

---

## Comparative Analysis

| Technique | Traceability | Transparency | Controllability | Overhead |
|-----------|--------------|--------------|-----------------|----------|
| Chain-of-Thought | Medium | Medium | Low | 1x |
| Tree-of-Thoughts | High | High | Medium | 5-20x |
| Self-Consistency | Low | Low | Low | 5-40x |
| Chain-of-Verification | High | High | Medium | 3-4x |
| SelfCheckGPT | Medium | Low | Low | 20x |
| Multi-Agent Debate | High | High | Medium | 6-30x |
| Reflexion | High | High | Medium | 3-10 trials |
| Semantic Entropy | Medium | Low | Low | 10x |

---

## Sources

**Foundational:**
- Wei et al. (2022). Chain-of-Thought Prompting. NeurIPS 2022.
- Yao et al. (2023). Tree of Thoughts. NeurIPS 2023 Oral.
- Wang et al. (2023). Self-Consistency. ICLR 2023.

**Verification:**
- Dhuliawala et al. (2024). Chain-of-Verification. ACL 2024.
- Manakul et al. (2023). SelfCheckGPT. EMNLP 2023.
- Min et al. (2023). FActScore. EMNLP 2023.

**Metacognition:**
- Shinn et al. (2023). Reflexion. NeurIPS 2023.
- Farquhar et al. (2024). Semantic Entropy. Nature.
- Tian et al. (2023). Calibrated Confidence. EMNLP 2023.

**Decomposition:**
- Zhou et al. (2023). Least-to-Most Prompting. ICLR 2023.
- Yao et al. (2023). ReAct. ICLR 2023.

**Extended:**
- Besta et al. (2024). Graph-of-Thoughts. AAAI 2024.
- Du et al. (2024). Multi-Agent Debate. ICML 2024.
