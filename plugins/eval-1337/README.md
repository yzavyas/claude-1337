# eval-1337

Write evals that measure what matters. Not vanity metrics.

## Install

```
/plugin install eval-1337@claude-1337
```

## What It Does

Guides you to write rigorous evals for:

- **Agents** - Task completion, tool correctness
- **Skills** - Activation precision/recall
- **MCP Servers** - Tool call reliability
- **Prompts** - Output quality scoring

## The Problem It Solves

"My agent works 84% of the time" tells you nothing without knowing:
- Is that 84% precision or recall?
- What about the other 16%?
- How many runs did you test?

## Framework Recommendations

| Target | Framework | Why |
|--------|-----------|-----|
| Python agents | DeepEval | TaskCompletionMetric, full trace analysis |
| TypeScript | Braintrust | Identical API, Factuality scorer |
| RAG + tools | RAGAS | ToolCallAccuracy, ToolCallF1 |
| Skills | Custom | Precision/recall with labeled expectations |

## Sources

Built from research:
- [LLM Agent Evaluation Survey](https://arxiv.org/abs/2507.21504) (KDD 2025)
- [DeepEval](https://deepeval.com/) framework docs
- [Braintrust AutoEvals](https://github.com/braintrustdata/autoevals)
- [RAGAS](https://docs.ragas.io/) agent metrics
- [Scott Spence](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably) skills study
