# How LLMs Actually Reason (And How to Help Them)

When you ask an AI to solve a complex problem, what happens inside? And more importantly — how can you get better results?

This reference covers the research on structured reasoning. Not as academic trivia, but as practical knowledge: what works, when, and why.

---

## The Core Insight

Here's what researchers discovered: Large language models can reason through complex problems, but **only if you structure the problem right**.

Wei et al. (NeurIPS 2022) showed something surprising: if you just ask GPT-3 "What is 23 × 47?", it often fails. But if you show it examples where someone works through the problem step by step, suddenly it can do it too. The model had the capability — it just needed to be shown the pattern.

This sparked a whole field of research into *how* to structure problems for AI reasoning.

---

## The Techniques (Quick Reference)

| When you need... | Use this | What it does |
|------------------|----------|--------------|
| Multi-step math or logic | Chain-of-Thought | Shows reasoning steps |
| Higher confidence | Self-Consistency | Tries multiple paths, votes |
| Exploration of options | Tree-of-Thoughts | Searches through possibilities |
| Fact-checking | Chain-of-Verification | Independently verifies claims |
| Uncertainty detection | Semantic Entropy | Spots when the model isn't sure |

Now let's understand each one.

---

## Chain-of-Thought: Teaching the Model to Show Its Work

**The problem it solves:** Models jump to answers without working through the logic.

**What researchers found:** Wei et al. tested this across three major models (LaMDA-137B, PaLM-540B, GPT-3). When they added "let's think step by step" examples, math problem accuracy jumped dramatically. The model wasn't learning new facts — it was learning to *use* what it already knew.

**How it works in practice:**

Instead of:
> "What is 23 × 47?"

You prompt:
> "Let's work through this step by step. 23 × 47 = 23 × (50 - 3) = 23 × 50 - 23 × 3 = 1150 - 69 = 1081"

The model learns the pattern and applies it to new problems.

**The catch:** This only works with large models (100B+ parameters). Smaller models produce *fluent nonsense* — reasoning that sounds logical but reaches wrong conclusions. Turpin et al. (NeurIPS 2023) also found that models sometimes reach correct answers through incorrect reasoning — the explanation isn't always faithful to how the model actually computed the answer.

**When to use it:**
- Math problems
- Multi-step logic
- Symbolic reasoning
- Any task where "showing work" helps

**When to skip it:** Modern reasoning models (Claude 4.5, o1) already think this way internally. Explicit prompting shows diminishing returns.

---

## Self-Consistency: The Wisdom of Multiple Attempts

**The problem it solves:** A single reasoning path might be wrong. How do you know?

**What researchers found:** Wang et al. (ICLR 2023) discovered something elegant: ask the model to solve the same problem multiple times, then take the most common answer. On GSM8K math problems, this boosted accuracy by 17.9%.

**Why it works:** Different reasoning paths make different mistakes. If five out of seven attempts reach the same answer, that answer is probably right. The errors cancel out.

**The intuition:** Imagine asking seven people to calculate a tip. If five say "$18" and two say "$24", you'd trust the $18. Same principle.

**How to use it:**
1. Generate 5-20 reasoning paths (run the same prompt multiple times with temperature > 0)
2. Extract the final answer from each
3. Take the majority vote

**The limitation:** If all paths make the *same* mistake, voting won't help. Self-consistency catches random errors, not systematic biases.

**Cost:** 5-20x more compute, but it's parallelizable — all paths can run simultaneously.

---

## Tree-of-Thoughts: Exploring Before Committing

**The problem it solves:** Some problems require backtracking. If you go down the wrong path, you're stuck.

**What researchers found:** Yao et al. (NeurIPS 2023) tested this on the "Game of 24" — a puzzle where you use four numbers and basic operations to make 24. GPT-4 with chain-of-thought: 4% success. GPT-4 with Tree-of-Thoughts: 74% success. That's an 18.5x improvement.

**Why the difference?** Chain-of-thought commits to each step. If step 2 is wrong, you can't go back. Tree-of-Thoughts explores multiple possibilities at each step, evaluates them, and only expands the promising ones.

**How it works:**

```
Problem: Make 24 from [4, 5, 6, 10]

Step 1: Generate candidate operations
  → 4 + 5 = 9 (leaves [6, 9, 10])
  → 4 × 5 = 20 (leaves [6, 10, 20])
  → 10 - 6 = 4 (leaves [4, 4, 5])

Step 2: Evaluate each
  → [6, 9, 10]: Can we make 24? Let's score...
  → [6, 10, 20]: Can we make 24? Yes! 20 + 10 - 6 = 24

Step 3: Expand the best one, backtrack if needed
```

**When to use it:**
- Problems with many possible approaches
- Constraint satisfaction (scheduling, planning)
- Creative tasks where you want to explore options
- Any problem where "try something else" matters

**The cost:** 5-20x more compute. Each node in the tree requires LLM calls for generation and evaluation. You can reduce cost by using a smaller model for evaluation.

---

## Chain-of-Verification: Fact-Checking Your Own Output

**The problem it solves:** Models confidently state wrong things. How do you catch that?

**What researchers found:** Dhuliawala et al. at Meta AI (ACL 2024) built a four-stage pipeline that cuts hallucination by 50-70%. The key insight: **verification must be independent from generation**.

**Why independence matters:** If you ask a model to verify its own claim in the same context, it's biased toward confirming itself. The researchers tested "joint verification" (one prompt) vs "factored verification" (separate prompts for each check). Joint verification barely helped. Factored verification dramatically reduced errors.

**The pipeline:**

1. **Generate:** Write the initial response
2. **Plan:** Identify claims that need checking, create verification questions
3. **Execute:** Answer each question in a *fresh context* (no access to original response)
4. **Synthesize:** Update the original based on verification results

**Example:**

> **Original claim:** "Einstein won the Nobel Prize for relativity in 1921."
>
> **Verification question:** "What did Einstein win the Nobel Prize for?"
>
> **Independent answer:** "The photoelectric effect, not relativity."
>
> **Corrected claim:** "Einstein won the Nobel Prize for the photoelectric effect in 1921."

**When to use it:**
- Factual claims that matter
- Recommendations you're acting on
- Anything where being wrong has consequences

**The limitation:** Can only verify against the model's training data. If the model never learned the correct fact, verification won't help.

**Cost:** 3-4x more compute (each verification question needs a separate call).

---

## Semantic Entropy: Detecting When the Model Doesn't Know

**The problem it solves:** How do you tell the difference between a confident correct answer and a confident wrong one?

**What researchers found:** Farquhar et al. (Nature 2024) discovered that when models don't know something, they give *semantically different* answers each time. When they do know, they give semantically similar answers (even if worded differently).

**The insight:** "Uncertainty" isn't about word variation — it's about meaning variation.

**Example:**

> **Question:** "What year was the Treaty of Westphalia signed?"
>
> **Model knows:** Samples all say "1648" (maybe "in 1648", "the year 1648", etc.)
> → Low semantic entropy → Likely correct
>
> **Model doesn't know:** Samples say "1648", "1658", "1638", "the 17th century"
> → High semantic entropy → Uncertain, might be wrong

**How to measure it:**
1. Sample 5+ responses to the same question
2. Cluster them by meaning (using an NLI model to check equivalence)
3. Compute entropy over the clusters

**When to use it:**
- High-stakes decisions where being wrong matters
- Questions that might be outside training data
- Any time you need to know "how confident should I be?"

**Cost:** ~10x (multiple samples + NLI classification).

---

## Reflexion: Learning from Mistakes

**The problem it solves:** The model fails, but it can't learn from the failure.

**What researchers found:** Shinn et al. (NeurIPS 2023) created a loop: try, get feedback, reflect on what went wrong, try again with that knowledge. On HumanEval code generation, this raised success from 80% to 91%.

**Why it works:** The model stores a "verbal memory" of what failed and why. Next attempt, it avoids those mistakes. It's like a developer who remembers "last time I forgot to handle the null case."

**The catch:** You need real feedback. A failing test, a tool returning an error, something external. Without that grounding, the model can't tell if it improved or not. Huang et al. (2024) showed that asking a model to "try again" without external feedback often makes things *worse*.

**When to use it:**
- Code generation (tests provide feedback)
- Tasks with clear success/failure signals
- Anything where you can verify the output

**When it fails:**
- Complex math where intermediate steps can't be verified
- Long chains where you can't tell which step was wrong
- Tasks that exceed the model's memory capacity

---

## Multi-Agent Debate: Multiple Perspectives

**The problem it solves:** One model might be biased or wrong. Multiple models can challenge each other.

**What researchers found:** Du et al. (ICML 2024) had multiple LLM instances debate each other. On arithmetic, accuracy went from ~50% to ~80% with 3 agents over 2 rounds.

**How it works:**
1. Multiple models each generate an answer
2. They see each other's answers and critique them
3. They revise based on the critique
4. Repeat for a few rounds
5. Final answer emerges from consensus

**The intuition:** Like peer review. Your first draft has blind spots. Others catch them.

**Cost:** 6-30x (multiple agents × multiple rounds). Expensive, but powerful for high-stakes reasoning.

---

## Choosing the Right Technique

**For math and logic:** Start with Chain-of-Thought. Add Self-Consistency (5-10 samples) for higher confidence.

**For factual accuracy:** Use Chain-of-Verification. Make sure verification is independent.

**For exploration problems:** Use Tree-of-Thoughts. Accept the computational cost.

**For code generation:** Use Reflexion with test feedback.

**For uncertainty detection:** Use Semantic Entropy.

**For high-stakes decisions:** Layer multiple techniques. Verify, check uncertainty, escalate to human when needed.

---

## What the Research Actually Shows

| Finding | Source | What it means |
|---------|--------|---------------|
| Step-by-step prompting unlocks reasoning | Wei et al. 2022 | The capability exists; you have to elicit it |
| Models can reach right answers via wrong reasoning | Turpin et al. 2023 | Don't trust explanations blindly |
| Multiple samples catch random errors | Wang et al. 2023 | Voting works, but can't catch systematic bias |
| Search dramatically helps exploration problems | Yao et al. 2023 | 18.5x improvement isn't magic — it's structure |
| Independent verification cuts hallucination in half | Dhuliawala et al. 2024 | Separation matters more than the check itself |
| Meaning variation reveals uncertainty | Farquhar et al. 2024 | This is state-of-the-art uncertainty detection |
| Feedback loops enable learning | Shinn et al. 2023 | But only with external grounding |
| Self-correction without feedback hurts | Huang et al. 2024 | "Try again" doesn't work |

---

## Sources

**Primary research:**
- Wei, J. et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." NeurIPS 2022. *Foundational work showing how step-by-step prompting unlocks reasoning.*
- Yao, S. et al. (2023). "Tree of Thoughts: Deliberate Problem Solving with Large Language Models." NeurIPS 2023 Oral. *Introduced search-based reasoning.*
- Wang, X. et al. (2023). "Self-Consistency Improves Chain of Thought Reasoning." ICLR 2023. *The majority-voting approach.*
- Dhuliawala, S. et al. (2024). "Chain-of-Verification Reduces Hallucination in Large Language Models." ACL 2024. *The factored verification insight.*
- Farquhar, S. et al. (2024). "Detecting Hallucinations in Large Language Models Using Semantic Entropy." Nature. *State-of-the-art uncertainty detection.*
- Shinn, N. et al. (2023). "Reflexion: Language Agents with Verbal Reinforcement Learning." NeurIPS 2023. *Learning from verbal feedback.*
- Huang, J. et al. (2024). "Large Language Models Cannot Self-Correct Reasoning Yet." *The limitation of intrinsic self-correction.*

**Additional:**
- Turpin, M. et al. (2023). "Language Models Don't Always Say What They Think." NeurIPS 2023. *On unfaithful explanations.*
- Du, Y. et al. (2024). "Improving Factuality and Reasoning through Multiagent Debate." ICML 2024. *Multi-agent approach.*
- Besta, M. et al. (2024). "Graph of Thoughts." AAAI 2024. *Extended tree search to graphs.*
