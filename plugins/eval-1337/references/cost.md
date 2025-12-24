# Cost and Token Tracking

Measuring context consumption and cost efficiency.

## What to Measure

| Metric | Question | Unit |
|--------|----------|------|
| Token count | How many tokens per request? | tokens |
| Cost per run | How much does each eval cost? | $/run |
| Context efficiency | How much context is consumed? | % of limit |
| Cost per success | What's the cost of correct outputs? | $/success |

## Langfuse Integration

[Langfuse](https://langfuse.com/docs/model-usage-and-cost) provides automatic cost tracking:

```python
from langfuse import Langfuse
from langfuse.decorators import observe

langfuse = Langfuse()

@observe()
def my_agent(input):
    # Your agent logic
    return result

# After running
trace = langfuse.get_trace(trace_id)
print(f"Input tokens: {trace.input_tokens}")
print(f"Output tokens: {trace.output_tokens}")
print(f"Total cost: ${trace.total_cost}")
```

**TypeScript:**
```typescript
import { Langfuse } from "langfuse";

const langfuse = new Langfuse();

const trace = langfuse.trace({ name: "my-eval" });
const generation = trace.generation({
  name: "llm-call",
  model: "claude-3-5-sonnet-20241022",
  usage: { input: 1000, output: 500 }
});

// Langfuse calculates cost automatically from model pricing
```

## Tokencost Library

[Tokencost](https://github.com/AgentOps-AI/tokencost) for programmatic cost calculation:

```python
import tokencost

# Calculate cost from tokens
cost = tokencost.calculate_prompt_cost(
    prompt="Your prompt here",
    model="claude-3-5-sonnet-20241022"
)
print(f"Prompt cost: ${cost}")

# Or from token counts
cost = tokencost.calculate_cost(
    input_tokens=1000,
    output_tokens=500,
    model="claude-3-5-sonnet-20241022"
)
```

## Cost Tracking in Evals

```python
def run_eval_with_cost(test_cases):
    results = []

    for case in test_cases:
        start_tokens = get_usage()

        output = agent(case.input)

        end_tokens = get_usage()
        tokens_used = end_tokens - start_tokens
        cost = calculate_cost(tokens_used)

        results.append({
            "input": case.input,
            "output": output,
            "correct": output == case.expected,
            "tokens": tokens_used,
            "cost": cost
        })

    # Aggregate metrics
    total_cost = sum(r["cost"] for r in results)
    correct_count = sum(r["correct"] for r in results)
    cost_per_success = total_cost / correct_count if correct_count else float('inf')

    return {
        "total_cost": total_cost,
        "cost_per_success": cost_per_success,
        "avg_tokens": sum(r["tokens"] for r in results) / len(results)
    }
```

## Context Window Efficiency

Track how much context you're consuming:

```python
def context_efficiency(trace):
    model_limits = {
        "claude-3-5-sonnet-20241022": 200_000,
        "gpt-4o": 128_000,
        "claude-3-opus-20240229": 200_000,
    }

    limit = model_limits.get(trace.model, 100_000)
    used = trace.input_tokens + trace.output_tokens

    return {
        "tokens_used": used,
        "context_limit": limit,
        "efficiency": used / limit,
        "headroom": limit - used
    }
```

## Budget Guardrails

Set cost limits for evals:

```python
MAX_COST_PER_RUN = 0.10  # $0.10 per test case
MAX_TOTAL_BUDGET = 10.00  # $10 total for eval suite

running_cost = 0.0

for case in test_cases:
    if running_cost >= MAX_TOTAL_BUDGET:
        print(f"Budget exceeded at ${running_cost}")
        break

    cost = run_single_eval(case)
    running_cost += cost

    if cost > MAX_COST_PER_RUN:
        print(f"Warning: case cost ${cost} > limit ${MAX_COST_PER_RUN}")
```

## Gotchas

| Trap | Fix |
|------|-----|
| Ignoring retries | Count ALL API calls, including retries |
| Missing embeddings | Embedding calls have costs too |
| Dev vs prod pricing | Some providers have different pricing tiers |
| Caching not tracked | Don't count cached responses as "free" |

## Cost Comparison

| Model | Input ($/1M) | Output ($/1M) |
|-------|--------------|---------------|
| claude-3-5-sonnet | $3.00 | $15.00 |
| claude-3-opus | $15.00 | $75.00 |
| gpt-4o | $2.50 | $10.00 |
| gpt-4o-mini | $0.15 | $0.60 |

*Prices as of Dec 2024. Check provider docs for current rates.*
