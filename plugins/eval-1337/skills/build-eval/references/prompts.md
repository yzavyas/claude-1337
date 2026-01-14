# Prompt Evaluation

Measuring output quality using LLM-as-judge and rubrics.

## Three Approaches

| Approach | When to Use | Pros | Cons |
|----------|-------------|------|------|
| LLM-as-judge | Subjective quality | Flexible, scalable | Depends on judge LLM |
| Rubric-based | Clear criteria | Reproducible | Requires upfront work |
| Rules-based | Deterministic checks | Fast, consistent | Limited to format |

## LLM-as-Judge

Use another LLM to rate output quality.

### Braintrust Factuality

```typescript
import { Factuality } from "autoevals";

const result = await Factuality({
  input: "Which country has highest population?",
  output: "People's Republic of China",
  expected: "China",
});

console.log(result.score);  // 0-1
console.log(result.metadata?.rationale);
```

### Custom Scorer

```typescript
import { LLMClassifierFromSpec } from "autoevals";

const ToneScorer = LLMClassifierFromSpec("Tone", {
  prompt: `Rate the tone of this response:

{output}

Is it professional and helpful?`,
  choice_scores: {
    "Professional": 1.0,
    "Neutral": 0.5,
    "Unprofessional": 0.0,
  },
});
```

### DeepEval G-Eval

```python
from deepeval.metrics import GEval

metric = GEval(
    name="Helpfulness",
    criteria="How helpful is the response for the user's question?",
    evaluation_params=["input", "actual_output"],
)
```

## Rubric-Based Scoring

Define explicit criteria:

```python
RUBRIC = {
    5: "Exceeds requirements. Complete, accurate, well-formatted.",
    4: "Meets requirements. Minor issues only.",
    3: "Partially meets. Some gaps or errors.",
    2: "Significant gaps. Multiple issues.",
    1: "Fails requirements. Major problems.",
}

# Use in LLM-as-judge prompt
prompt = f"""
Rate this response on a scale of 1-5:

{response}

Rubric:
{RUBRIC}

Score:
"""
```

## Rules-Based Checks

Deterministic validation:

```python
def validate_output(output):
    checks = []

    # Format checks
    checks.append(("has_greeting", output.startswith("Hello")))
    checks.append(("under_limit", len(output) < 1000))

    # Content checks
    checks.append(("no_pii", not contains_pii(output)))
    checks.append(("no_profanity", not contains_profanity(output)))

    # Code checks (if applicable)
    if "```" in output:
        checks.append(("valid_syntax", parse_code(output) is not None))

    return {name: passed for name, passed in checks}
```

## Combining Approaches

Best practice: layer multiple approaches:

```
1. Rules-based    → Fast filter (format, length, forbidden content)
2. LLM-as-judge   → Quality assessment (helpfulness, accuracy)
3. Human review   → Final sample check (10% of outputs)
```

## Reliability Across Runs

LLM-as-judge is stochastic. Run multiple times:

```python
scores = []
for _ in range(5):
    score = llm_judge(output)
    scores.append(score)

mean_score = sum(scores) / len(scores)
variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)

# Report: 4.2 ± 0.3
```

## Gotchas

| Trap | Fix |
|------|-----|
| Judge LLM too lenient | Calibrate with known bad examples |
| Vague rubric | Specific, measurable criteria |
| Ignoring edge cases | Include adversarial inputs |
| No baseline | Compare against simple baseline |

## Eval File Convention

Braintrust pattern:

```
*.eval.ts     # TypeScript
*.eval.js     # JavaScript
eval_*.py     # Python
```

Example:

```typescript
// quality.eval.ts
import { Eval } from "braintrust";
import { Factuality } from "autoevals";

Eval("QualityEval", {
  data: () => loadTestCases(),
  task: async (input) => await myLLM(input),
  scores: [Factuality],
});
```

## Phoenix LLM-as-Judge (Local)

No cloud dependency:

```python
from phoenix.evals import llm_classify, OpenAIModel
import pandas as pd

eval_model = OpenAIModel(model="gpt-4o-mini")

# Custom quality rubric
results = llm_classify(
    dataframe=pd.DataFrame({"response": responses}),
    template="""Rate this response:

{response}

Is it helpful, accurate, and well-formatted?""",
    model=eval_model,
    rails=["excellent", "good", "poor"],
)
```

## Anthropic-Specific Patterns

For Claude-generated outputs:

```python
# Use Claude as judge for Claude outputs
from anthropic import Anthropic

client = Anthropic()

def claude_judge(output: str, criteria: str) -> int:
    response = client.messages.create(
        model="claude-3-5-haiku-20241022",  # Fast, cheap judge
        max_tokens=10,
        messages=[{
            "role": "user",
            "content": f"""Rate this output 1-5 based on: {criteria}

Output: {output}

Score (just the number):"""
        }]
    )
    return int(response.content[0].text.strip())
```

## Sources

- [Braintrust AutoEvals](https://github.com/braintrustdata/autoevals) - Factuality, custom scorers
- [DeepEval G-Eval](https://deepeval.com/docs/metrics-g-eval) - Rubric-based evaluation
- [Phoenix Evals](https://github.com/Arize-ai/phoenix) - Local LLM-as-judge
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) - Claude evaluation patterns
- [LLM-as-Judge Survey](https://arxiv.org/abs/2310.05470) - Judging LLM-as-a-Judge (NeurIPS 2023)
