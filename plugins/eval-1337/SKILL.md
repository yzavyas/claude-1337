---
name: eval-1337
description: "Write rigorous evals for LLM agents, skills, MCP servers, and prompts. Use when: building test suites, measuring agent effectiveness, evaluating tool reliability, or choosing eval frameworks. Covers: DeepEval, Braintrust, RAGAS, precision/recall, F1, task completion."
---

# Eval-1337

Write evals that measure what matters. Not vanity metrics.

## The Core Problem

```python
# This tells you NOTHING
activation_rate = 100%  # Activates on every prompt = useless
```

Single metrics lie. You need to measure BOTH failure modes.

## Match Metric to Target

| Target | What to Measure | Metric | Framework |
|--------|-----------------|--------|-----------|
| **Agents** | Task completion | Accuracy (pass/fail) | DeepEval |
| **Agents** | Tool usage | ToolCorrectnessMetric | DeepEval |
| **Skills** | Activation | Precision/Recall/F1 | Custom |
| **MCP Servers** | Tool calls | ToolCallAccuracy | RAGAS |
| **MCP Servers** | Reliability | MCPGauge 4-dim | Custom |
| **Prompts** | Output quality | LLM-as-judge | Braintrust |
| **Any** | Cost/tokens | $/1M tokens, context | Tokencost |
| **Any** | Traces | Span analysis | Phoenix (local) |
| **Any** | Drift | Behavioral change | Custom baseline |
| **Any** | Security | Attack resistance | Promptfoo, garak |
| **Any** | Benchmarks | Standardized | SWE-bench, ToolBench |

## Three Metric Types

| Type | Formula | Use When |
|------|---------|----------|
| **Accuracy** | Correct / Total | Task completion (did it work?) |
| **F1** | 2×(P×R)/(P+R) | Classification (triggers, detection) |
| **LLM-as-judge** | Score 1-5 | Quality (subjective output eval) |

## Framework Decision

| Situation | Use | Why |
|-----------|-----|-----|
| Python agent evals | **DeepEval** | TaskCompletionMetric, ToolCorrectness, full trace |
| TypeScript/Node | **Braintrust** | Identical Python/TS API, Factuality scorer |
| RAG pipelines | **RAGAS** | ToolCallF1, context metrics |
| Skill activation | **Custom** | Precision/recall with labeled expectations |

## Production Gotchas

| Trap | Fix |
|------|-----|
| Single test run | **5+ runs per case** - LLMs are stochastic |
| Measuring recall only | **Add precision** - high recall + low precision = noise |
| "Forced eval" inflation | **Test realistic conditions** - forced mode inflates scores |
| No ground truth | **Label expectations** - must_trigger, should_not_trigger |
| Wrong metric for target | **Match to objective** - accuracy ≠ F1 ≠ quality |

## Classification Metrics (F1)

Use when you have TWO failure modes:

```
                      ACTUAL
                      Yes         No
                  +-----------+-----------+
EXPECTED    Yes   |    TP     |    FN     |
                  |  Correct  |  Missed   |
                  +-----------+-----------+
            No    |    FP     |    TN     |
                  |   Noise   |  Correct  |
                  +-----------+-----------+

Precision = TP / (TP + FP)   "when it fires, is it right?"
Recall    = TP / (TP + FN)   "when it should fire, does it?"
F1        = 2×(P×R)/(P+R)    "balanced score"
```

**Why F1?** Can't game by going extreme:

| P | R | Avg | F1 |
|---|---|-----|-----|
| 100% | 0% | 50% | **0%** |
| 80% | 80% | 80% | **80%** |

## Labeled Test Cases

```json
{"input": "What crate for CLI args?", "expectation": "must_trigger"}
{"input": "Write a haiku", "expectation": "should_not_trigger"}
{"input": "Explain ownership", "expectation": "acceptable"}
```

| Label | Meaning | Measures |
|-------|---------|----------|
| must_trigger | Should definitely fire | Recall (misses) |
| should_not_trigger | Must not fire | Precision (noise) |
| acceptable | Either outcome fine | Excluded from metrics |

## The Eval Workflow

```
1. DEFINE   → What objective? What target?
2. DESIGN   → Create labeled test cases
3. RUN      → Execute 5+ times per case
4. MEASURE  → Compute appropriate metric
5. ITERATE  → Improve based on failures
6. SHIP     → Only when metrics meet threshold
```

## Domain Routing

| Detected | Load |
|----------|------|
| agent, task completion | [agents.md](references/agents.md) |
| skill, activation, trigger | [skills.md](references/skills.md) |
| MCP, tool call, server | [mcp.md](references/mcp.md) |
| prompt, quality, judge | [prompts.md](references/prompts.md) |
| cost, tokens, budget | [cost.md](references/cost.md) |
| trace, debug, interpret | [observability.md](references/observability.md) |
| OTel, instrument, plugin | [otel.md](references/otel.md) |
| security, red team, adversarial | [security.md](references/security.md) |
| benchmark, SWE-bench, ToolBench | [benchmarks.md](references/benchmarks.md) |
| dataset, labeling, augmentation | [datasets.md](references/datasets.md) |
| DeepEval, Braintrust, RAGAS | [frameworks.md](references/frameworks.md) |

## Quick Reference

```
AGENTS
  DeepEval: TaskCompletionMetric(threshold=0.7)
  Measures: Did it complete the task?

SKILLS
  Custom F1 with labeled expectations
  Measures: Activation precision/recall

MCP
  RAGAS: ToolCallAccuracy, ToolCallF1
  MCPGauge: proactivity, compliance, effectiveness, overhead
  Measures: Tool call success + reliability

PROMPTS
  Braintrust: Factuality, custom scorers
  Measures: Output quality (1-5 scale)

COST
  Tokencost: $/run, tokens/request (local library)
  Measures: Context consumption, budget

OBSERVABILITY
  Phoenix: trace spans, latency (runs locally)
  Measures: Debug traces, interpretability

OTEL (ALL PLUGIN TYPES)
  Skills: skill_check, skill_match spans
  Agents: agent_run, llm_call, tool_call spans
  Commands: command, command_execute spans
  Hooks: hook_trigger, hook_handler spans
  MCP: mcp_server, mcp_call spans

DRIFT
  Baseline z-score comparison
  Measures: Behavioral change over time

SECURITY
  Promptfoo redteam, garak, PyRIT
  Measures: Attack resistance, injection defense

BENCHMARKS
  SWE-bench: Code agents (500 verified)
  ToolBench: Tool calling (16k+ APIs)
  WebArena: Web agents (812 tasks)

DATASETS
  Labeled expectations, augmentation
  Measures: Coverage, balance
```

## Sources

- [arxiv:2507.21504](https://arxiv.org/abs/2507.21504) - LLM Agent Evaluation Survey (KDD 2025)
- [DeepEval](https://deepeval.com/docs/metrics-task-completion) - TaskCompletionMetric
- [Braintrust](https://github.com/braintrustdata/autoevals) - AutoEvals
- [RAGAS](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/agents/) - Agent Metrics
- [MCPGauge](https://arxiv.org/abs/2506.07540) - MCP Server Evaluation (Jun 2025)
- [Tokencost](https://github.com/AgentOps-AI/tokencost) - Local Cost Calculation
- [Phoenix](https://docs.arize.com/phoenix) - LLM Observability and Tracing
- [Phoenix Evals](https://github.com/Arize-ai/phoenix) - Local LLM Evaluation
- [Claude Agent SDK](https://code.claude.com/docs/en/monitoring-usage) - Native OTel
- [Google ADK](https://google.github.io/adk-docs/observability/cloud-trace/) - Native OTel
- [Scott Spence](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably) - Skills Activation Study
- [SWE-bench](https://www.swebench.com/) - Code Agent Benchmark
- [Promptfoo](https://promptfoo.dev/docs/red-team/) - Red Teaming
- [garak](https://github.com/leondz/garak) - LLM Vulnerability Scanner
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) - Security Risks
