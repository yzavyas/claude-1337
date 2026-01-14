# Iterative Evaluation (Ralph Pattern)

Using eval failures as feedback to measure recoverability and improvement potential.

## The Problem Traditional Evals Don't Solve

Traditional eval:
```
Run agent → Get score → Done
Result: 60% pass rate
```

This tells you capability. It doesn't tell you:
- Can the agent recover from failures with guidance?
- Is 60% the ceiling, or just first-try performance?
- Should you invest in better prompts or better feedback loops?

## The Iterative Pattern

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│   Run agent ──▶ Eval result ──▶ Pass? ──▶ Done        │
│       ▲              │           │                     │
│       │              ▼           ▼ No                  │
│       │         Generate    ◀────┘                     │
│       │         feedback                               │
│       │              │                                 │
│       └──────────────┘                                 │
│         (retry with feedback)                          │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## What Iterative Eval Measures

| Metric | Formula | Question Answered |
|--------|---------|-------------------|
| **pass@1** | First try success | Baseline capability |
| **pass@k (iterative)** | Success within k retries | Recoverable capability |
| **iterations_to_pass** | Retries until success | Learning speed |
| **recovery_rate** | (pass@k - pass@1) / (1 - pass@1) | % of failures that recover |
| **feedback_sensitivity** | Δscore per iteration | Does guidance help? |
| **ceiling_score** | Max score across iterations | Best achievable |

## Concrete Use Case: Code Agent

### Scenario

You have a code-fixing agent. Traditional eval shows 60% pass@1.

### Questions You Can't Answer

- Is 60% the agent's limit?
- If I show it the test failures, can it fix them?
- Should I build a retry mechanism or improve prompts?

### Iterative Eval Answers These

```python
async def iterative_code_eval(agent, test_cases):
    results = []

    for case in test_cases:
        attempts = []
        feedback = ""

        for iteration in range(3):  # Max 3 tries
            # Run with accumulated feedback
            prompt = f"Fix: {case.description}"
            if feedback:
                prompt += f"\n\nPrevious attempt failed:\n{feedback}"

            result = await agent.run(prompt)
            test_output = run_tests(case.repo)
            passed = test_output.returncode == 0

            attempts.append({
                "iteration": iteration + 1,
                "passed": passed,
                "output": test_output.stderr[:500]
            })

            if passed:
                break

            # Feedback for next iteration
            feedback = test_output.stderr

        results.append({
            "case": case.id,
            "attempts": attempts,
            "final_passed": attempts[-1]["passed"],
            "iterations_needed": len(attempts)
        })

    return analyze_results(results)
```

### Example Output

```
Code Agent Iterative Eval:
├── pass@1: 60%         (baseline)
├── pass@2: 82%         (+22% with one retry)
├── pass@3: 91%         (+9% more)
├── recovery_rate: 78%  (78% of failures recovered)
├── avg_iterations: 1.6
└── feedback_helps: True

Interpretation:
  Agent CAN fix 91% of bugs, but needs test feedback.
  Deploy with retry loop, not better prompts.
```

### Contrast: When Feedback Doesn't Help

```
Code Agent Iterative Eval:
├── pass@1: 60%
├── pass@2: 63%         (+3% - minimal improvement)
├── pass@3: 64%         (+1% - plateau)
├── recovery_rate: 10%
├── feedback_helps: False

Interpretation:
  Agent is at capability ceiling.
  Retry won't help. Need better model or prompts.
```

## Implementation

### Basic Iterative Harness

```python
class IterativeEvaluator:
    def __init__(self, agent, eval_fn, max_iterations=5):
        self.agent = agent
        self.eval_fn = eval_fn
        self.max_iterations = max_iterations

    async def evaluate(self, task: str, context: dict = None):
        attempts = []
        feedback_context = ""

        for i in range(self.max_iterations):
            # Build prompt with feedback
            prompt = task
            if feedback_context:
                prompt = f"{task}\n\nFeedback from previous attempt:\n{feedback_context}"

            # Run agent
            result = await self.agent.run(prompt, context=context)

            # Evaluate
            eval_result = self.eval_fn(result, task)

            attempts.append({
                "iteration": i + 1,
                "score": eval_result["score"],
                "passed": eval_result["passed"],
                "details": eval_result
            })

            if eval_result["passed"]:
                break

            # Generate feedback for next iteration
            feedback_context = self._generate_feedback(eval_result)

        return self._analyze(attempts)

    def _generate_feedback(self, eval_result: dict) -> str:
        """Convert eval failure into actionable feedback."""
        parts = []

        if eval_result.get("test_failures"):
            parts.append(f"Tests failed:\n{eval_result['test_failures']}")

        if eval_result.get("missing_elements"):
            parts.append(f"Missing: {eval_result['missing_elements']}")

        if eval_result.get("errors"):
            parts.append(f"Errors: {eval_result['errors']}")

        return "\n\n".join(parts) if parts else "Try a different approach."

    def _analyze(self, attempts: list) -> dict:
        scores = [a["score"] for a in attempts]
        passed_at = next((i+1 for i, a in enumerate(attempts) if a["passed"]), None)

        return {
            "pass@1": attempts[0]["passed"],
            "passed": attempts[-1]["passed"],
            "iterations_to_pass": passed_at,
            "iterations_run": len(attempts),
            "score_trajectory": scores,
            "improvement": scores[-1] - scores[0] if len(scores) > 1 else 0,
            "ceiling_score": max(scores),
            "attempts": attempts
        }
```

### Aggregating Across Test Cases

```python
def aggregate_iterative_results(case_results: list) -> dict:
    n = len(case_results)

    pass_1 = sum(1 for r in case_results if r["pass@1"]) / n
    pass_k = sum(1 for r in case_results if r["passed"]) / n

    iterations = [r["iterations_to_pass"] for r in case_results if r["iterations_to_pass"]]
    avg_iterations = sum(iterations) / len(iterations) if iterations else None

    improvements = [r["improvement"] for r in case_results]
    avg_improvement = sum(improvements) / len(improvements)

    return {
        "pass@1": pass_1,
        "pass@k": pass_k,
        "recovery_rate": (pass_k - pass_1) / (1 - pass_1) if pass_1 < 1 else 1.0,
        "avg_iterations_to_pass": avg_iterations,
        "avg_improvement": avg_improvement,
        "feedback_helps": avg_improvement > 0.05
    }
```

## When to Use Iterative Eval

| Scenario | Traditional | Iterative |
|----------|-------------|-----------|
| Measuring baseline capability | ✓ | |
| Regression testing (CI/CD) | ✓ | |
| Comparing models | ✓ | |
| Deciding: retry loop vs better prompts? | | ✓ |
| Finding capability ceiling | | ✓ |
| Optimizing feedback mechanisms | | ✓ |
| Evaluating agent improvability | | ✓ |

## Metrics Deep Dive

### Recovery Rate

```python
recovery_rate = (pass_at_k - pass_at_1) / (1 - pass_at_1)
```

| Recovery Rate | Interpretation |
|---------------|----------------|
| 0% | Failures are permanent |
| 25% | Some failures recoverable |
| 50% | Half of failures recover |
| 75%+ | Most failures recover with feedback |

### Feedback Sensitivity

```python
# Score trajectory: [0.3, 0.5, 0.7, 0.8, 0.8]
feedback_sensitivity = (final_score - initial_score) / iterations
# (0.8 - 0.3) / 4 = 0.125 per iteration
```

| Sensitivity | Interpretation |
|-------------|----------------|
| <0.02 | Agent doesn't learn from feedback |
| 0.02-0.10 | Modest improvement |
| 0.10-0.20 | Good feedback response |
| >0.20 | Highly feedback-responsive |

### Ceiling Score

The maximum score achieved across all iterations.

```python
ceiling = max(attempt["score"] for attempt in attempts)
```

- If ceiling >> pass@1: Agent capable but needs guidance
- If ceiling ≈ pass@1: Agent at its limit

## Integration with Standard Metrics

Combine iterative metrics with traditional ones:

```python
def full_evaluation(agent, test_cases, n_independent=5, max_iterative=3):
    """
    Run both independent trials and iterative refinement.
    """
    results = {"cases": []}

    for case in test_cases:
        # Traditional: n independent runs
        independent_passes = 0
        for _ in range(n_independent):
            result = agent.run(case)
            if eval(result):
                independent_passes += 1

        # Iterative: run with feedback
        iterative = run_iterative_eval(agent, case, max_iterations=max_iterative)

        results["cases"].append({
            "case_id": case.id,
            # Traditional metrics
            "pass@1": independent_passes >= 1,
            "pass@5": independent_passes >= 1,  # Any of 5
            "pass^5": independent_passes == 5,  # All of 5
            "success_rate": independent_passes / n_independent,
            # Iterative metrics
            "pass@k_iterative": iterative["passed"],
            "iterations_to_pass": iterative["iterations_to_pass"],
            "recovery_rate": iterative.get("recovery_rate"),
            "feedback_sensitivity": iterative["improvement"] / max_iterative
        })

    return aggregate(results)
```

## Gotchas

| Trap | Problem | Fix |
|------|---------|-----|
| Unlimited retries | Cost explosion | Set max_iterations |
| Same feedback | Agent loops on same approach | Vary feedback phrasing |
| Contamination | Later attempts see earlier context | Reset agent state |
| Overfitting feedback | Agent only works with specific format | Vary feedback structure |
| Cost blindness | Iterative is expensive | Track cost per case |

## Cost Considerations

Iterative eval costs more than traditional:

```python
# Traditional: n_cases × 1 run
traditional_cost = n_cases * cost_per_run

# Iterative: n_cases × avg_iterations runs
iterative_cost = n_cases * avg_iterations * cost_per_run

# With avg_iterations = 2.5
# Iterative costs ~2.5x more
```

Set budget limits:

```python
MAX_COST_PER_CASE = 0.50  # $0.50 per case max
MAX_TOTAL_COST = 50.00    # $50 total

running_cost = 0
for case in cases:
    if running_cost >= MAX_TOTAL_COST:
        break

    result = iterative_eval(case, cost_limit=MAX_COST_PER_CASE)
    running_cost += result["cost"]
```

## Sources

- [Ralph Wiggum Pattern](https://ghuntley.com/ralph/) - Original iterative loop concept
- [Anthropic Agent Evaluation](https://www.anthropic.com/engineering/building-effective-agents) - Feedback loops in agent development
