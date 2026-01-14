# Cost and Token Tracking

Measuring context consumption and cost efficiency. All local, no cloud.

## What to Measure

| Metric | Question | Unit |
|--------|----------|------|
| Token count | How many tokens per request? | tokens |
| Cost per run | How much does each eval cost? | $/run |
| Context efficiency | How much context is consumed? | % of limit |
| Cost per success | What's the cost of correct outputs? | $/success |

## Tokencost (Primary)

[Tokencost](https://github.com/AgentOps-AI/tokencost) - local library, no cloud:

```python
import tokencost

# Calculate cost from prompt text
cost = tokencost.calculate_prompt_cost(
    prompt="Your prompt here",
    model="claude-3-5-sonnet-20241022"
)
print(f"Prompt cost: ${cost}")

# Or from token counts directly
cost = tokencost.calculate_cost(
    input_tokens=1000,
    output_tokens=500,
    model="claude-3-5-sonnet-20241022"
)
print(f"Total cost: ${cost}")

# Count tokens locally
tokens = tokencost.count_tokens("Your text here", model="claude-3-5-sonnet-20241022")
```

**Install:**
```bash
pip install tokencost
```

## TypeScript: tiktoken

For TypeScript/Bun, use tiktoken for token counting:

```typescript
import { encoding_for_model } from "tiktoken";

const enc = encoding_for_model("gpt-4o");
const tokens = enc.encode("Your text here");
console.log(`Token count: ${tokens.length}`);
enc.free();

// Manual cost calculation
const PRICING = {
  "claude-3-5-sonnet-20241022": { input: 3.0, output: 15.0 }, // per 1M
  "gpt-4o": { input: 2.5, output: 10.0 },
};

function calculateCost(model: string, inputTokens: number, outputTokens: number) {
  const pricing = PRICING[model];
  return (inputTokens * pricing.input + outputTokens * pricing.output) / 1_000_000;
}
```

**Install:**
```bash
bun add tiktoken
```

## Cost Tracking in Evals

```python
import tokencost

def run_eval_with_cost(test_cases, model="claude-3-5-sonnet-20241022"):
    results = []

    for case in test_cases:
        # Track input cost
        input_cost = tokencost.calculate_prompt_cost(case.input, model)

        output = agent(case.input)

        # Track output cost
        output_cost = tokencost.calculate_completion_cost(output, model)
        total_cost = input_cost + output_cost

        results.append({
            "input": case.input,
            "output": output,
            "correct": output == case.expected,
            "cost": total_cost
        })

    # Aggregate
    total_cost = sum(r["cost"] for r in results)
    correct_count = sum(r["correct"] for r in results)
    cost_per_success = total_cost / correct_count if correct_count else float('inf')

    return {
        "total_cost": total_cost,
        "cost_per_success": cost_per_success,
        "accuracy": correct_count / len(results)
    }
```

## Context Window Efficiency

Track how much context you're consuming:

```python
MODEL_LIMITS = {
    "claude-3-5-sonnet-20241022": 200_000,
    "claude-3-opus-20240229": 200_000,
    "gpt-4o": 128_000,
    "gpt-4o-mini": 128_000,
}

def context_efficiency(model, input_tokens, output_tokens):
    limit = MODEL_LIMITS.get(model, 100_000)
    used = input_tokens + output_tokens

    return {
        "tokens_used": used,
        "context_limit": limit,
        "utilization": used / limit,
        "headroom": limit - used
    }

# Example
eff = context_efficiency("claude-3-5-sonnet-20241022", 50_000, 10_000)
# {'tokens_used': 60000, 'context_limit': 200000, 'utilization': 0.3, 'headroom': 140000}
```

## Budget Guardrails

Set cost limits for evals:

```python
MAX_COST_PER_RUN = 0.10  # $0.10 per test case
MAX_TOTAL_BUDGET = 10.00  # $10 total for eval suite

running_cost = 0.0

for case in test_cases:
    if running_cost >= MAX_TOTAL_BUDGET:
        print(f"Budget exceeded at ${running_cost:.2f}")
        break

    cost = run_single_eval(case)
    running_cost += cost

    if cost > MAX_COST_PER_RUN:
        print(f"Warning: case cost ${cost:.4f} > limit ${MAX_COST_PER_RUN}")
```

## Gotchas

| Trap | Fix |
|------|-----|
| Ignoring retries | Count ALL API calls, including retries |
| Missing embeddings | Embedding calls have costs too |
| Dev vs prod pricing | Some providers have different pricing tiers |
| Stale pricing | Update tokencost regularly for latest prices |

## Cost Comparison

| Model | Input ($/1M) | Output ($/1M) |
|-------|--------------|---------------|
| claude-3-5-sonnet | $3.00 | $15.00 |
| claude-3-opus | $15.00 | $75.00 |
| gpt-4o | $2.50 | $10.00 |
| gpt-4o-mini | $0.15 | $0.60 |

*Prices as of Dec 2024. Check provider docs for current rates.*

## Sources

- [Tokencost](https://github.com/AgentOps-AI/tokencost) - Local token counting and cost calculation
- [tiktoken](https://github.com/openai/tiktoken) - OpenAI's tokenizer (works for estimation)
- [Anthropic Pricing](https://www.anthropic.com/pricing) - Official Claude pricing
- [OpenAI Pricing](https://openai.com/api/pricing/) - Official GPT pricing
