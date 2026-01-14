# Methodology Evaluation (Level 2)

Measuring whether Claude **follows** a methodology after skill activation.

## The Problem

Level 1 (activation) answers: "Did the skill trigger?"
Level 2 (behavioral) answers: "Did Claude follow the methodology?"

A skill can activate but be ignored. Behavioral eval catches this.

## LLM-as-Judge Approach

Use a second LLM to score responses against a rubric.

```python
from deepeval.metrics import GEval

methodology_metric = GEval(
    name="MethodologyAdherence",
    criteria="""
    Score how well the response follows core-1337 methodology:
    1. Evidence: Does it cite sources? (production > blogs)
    2. WHY: Does it explain reasoning, not just answers?
    3. Verification: Does it check its own work?
    4. Honesty: Does it acknowledge uncertainty appropriately?
    """,
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT
    ],
    threshold=0.7
)
```

## The Rubric

| Criterion | 0 (Absent) | 1 (Partial) | 2 (Full) |
|-----------|------------|-------------|----------|
| **Evidence** | No sources | Source mentioned | Production/maintainer source with context |
| **WHY** | Just answer | Some reasoning | Full reasoning chain |
| **Verification** | No checking | Self-review noted | Explicit verification steps |
| **Honesty** | Overconfident | Sometimes hedges | Calibrated confidence |

**Score**: Sum / 8 (normalized to 0-1)

## Test Case Format

```json
{
  "name": "core-1337-behavioral",
  "test_cases": [
    {
      "prompt": "What database should I use for a real-time leaderboard?",
      "expected_behaviors": ["evidence", "why", "verification"],
      "min_score": 0.7
    },
    {
      "prompt": "Debug why this API returns 500 errors randomly",
      "expected_behaviors": ["scientific_method", "verification"],
      "min_score": 0.7
    }
  ]
}
```

## Implementation

### With DeepEval

```python
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import GEval

# Define criteria for each methodology component
evidence_criteria = """
Score 0-1: Does the response cite evidence?
0: No sources or evidence
0.5: Vague references ("some say", "it's known")
1: Specific sources (docs, production examples, maintainer guidance)
"""

why_criteria = """
Score 0-1: Does the response explain WHY, not just WHAT?
0: Just provides answer without reasoning
0.5: Some reasoning but incomplete
1: Full reasoning chain explaining the recommendation
"""

verification_criteria = """
Score 0-1: Does the response verify its claims?
0: No verification
0.5: Mentions should verify
1: Explicit verification steps or CoVe process
"""

honesty_criteria = """
Score 0-1: Is confidence calibrated to evidence strength?
0: Overconfident on uncertain claims
0.5: Sometimes hedges appropriately
1: Confidence matches evidence (strong claims have evidence, uncertain claims are hedged)
"""

# Create metrics
metrics = [
    GEval(name="Evidence", criteria=evidence_criteria, threshold=0.5),
    GEval(name="WHY", criteria=why_criteria, threshold=0.5),
    GEval(name="Verification", criteria=verification_criteria, threshold=0.3),
    GEval(name="Honesty", criteria=honesty_criteria, threshold=0.5),
]

# Run eval
test_case = LLMTestCase(
    input="What database for real-time leaderboard?",
    actual_output=response_from_claude
)
evaluate([test_case], metrics)
```

### With Braintrust (TypeScript)

```typescript
import { Eval } from "braintrust";

Eval("core-1337-behavioral", {
  data: () => testCases,
  task: async (input) => {
    return await claude.messages.create({
      model: "claude-sonnet-4-20250514",
      messages: [{ role: "user", content: input.prompt }],
    });
  },
  scores: [
    // Custom scorer for methodology
    {
      name: "methodology",
      scorer: async ({ input, output }) => {
        const judge = await claude.messages.create({
          model: "claude-sonnet-4-20250514",
          messages: [{
            role: "user",
            content: `Score this response 0-1 on methodology adherence:

Prompt: ${input.prompt}
Response: ${output}

Criteria:
- Evidence (0-1): Cites sources?
- WHY (0-1): Explains reasoning?
- Verification (0-1): Checks work?
- Honesty (0-1): Calibrated confidence?

Return JSON: {"evidence": 0.X, "why": 0.X, "verification": 0.X, "honesty": 0.X}`
          }]
        });
        return parseScores(judge.content);
      }
    }
  ]
});
```

## Combining Level 1 + Level 2

```
Level 1: Did skill activate? (F1)
    ↓ (if activated)
Level 2: Did Claude follow methodology? (rubric score)
    ↓
Combined Score = Activation × Adherence
```

This catches:
- **False activation**: Triggers but doesn't use methodology
- **Partial adherence**: Uses some but not all components
- **Full adherence**: Follows complete methodology

## Thresholds

| Score | Interpretation |
|-------|----------------|
| 0.85+ | Excellent methodology adherence |
| 0.70-0.85 | Good, minor gaps |
| 0.50-0.70 | Partial adherence, needs improvement |
| < 0.50 | Methodology not followed |

## OTel Instrumentation

```python
with tracer.start_as_current_span("methodology_eval") as span:
    span.set_attribute("prompt", prompt[:200])

    # Level 1
    span.set_attribute("skill_activated", activated)

    # Level 2
    span.set_attribute("evidence_score", scores["evidence"])
    span.set_attribute("why_score", scores["why"])
    span.set_attribute("verification_score", scores["verification"])
    span.set_attribute("honesty_score", scores["honesty"])
    span.set_attribute("methodology_total", sum(scores.values()) / 4)
```

## Sources

- [DeepEval GEval](https://deepeval.com/docs/metrics-llm-evals) - Custom LLM-as-judge
- [Braintrust Scorers](https://www.braintrust.dev/docs/guides/evals) - Custom evaluation
- [core-1337 SKILL.md](../../core-1337/SKILL.md) - Methodology definition
