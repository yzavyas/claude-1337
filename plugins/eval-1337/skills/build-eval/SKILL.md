---
name: build-eval
description: "Write rigorous evals for LLM agents, multi-agent systems, skills, MCP servers, and prompts. Use when: building test suites, measuring agent effectiveness, evaluating coordination, or choosing eval frameworks. Covers: DeepEval, Braintrust, RAGAS, precision/recall, F1, task completion, pass@k, iterative metrics, multi-agent coordination."
---

# Eval-1337

Write evals that measure what matters. Not vanity metrics.

The key to success is **measuring performance and iterating** (Anthropic 2026).

## The Core Problem

```python
# This tells you NOTHING
activation_rate = 100%  # Activates on every prompt = useless
```

Single metrics lie. You need to measure BOTH failure modes.

## Three Grader Types

| Type | Examples | Use When |
|------|----------|----------|
| **Code-based** | String match, regex, test suites, outcome verification | Deterministic checks (speed, objectivity) |
| **Model-based** | LLM rubric scoring, pairwise comparison, multi-judge | Open-ended tasks (flexibility, nuance) |
| **Human** | Expert review, crowdsourced judgment, spot-check | Gold standard (expensive, slow) |

**Code-based first:** Prefer deterministic graders; use model-based for flexibility; apply partial credit for multi-component tasks. "Grade what the agent produced, not the path it took" (Anthropic 2026).

## Match Eval to Agent Type

| Agent Type | Primary Grader | Key Metrics | Benchmark |
|------------|----------------|-------------|-----------|
| **Coding** | Code (test suites) | Tests pass, no regressions | SWE-bench Verified |
| **Conversational** | Multi (state + transcript + rubric) | Resolution, turn limits, tone | τ2-Bench |
| **Research** | Model (groundedness, coverage) | Claim support, source quality | Custom |
| **Computer Use** | Code (screenshot, state inspection) | GUI state, file system | WebArena, OSWorld |
| **Skills** | Code (activation) + Model (methodology) | F1 + adherence rubric | Custom |
| **Multi-Agent** | Multi (milestones + coordination) | Task score, handoff success | MultiAgentBench |
| **Pipeline** | Per-stage + handoffs + end-to-end | Stage success, bottleneck | Custom |

## Non-Determinism Metrics

LLMs are stochastic. Run 5+ trials per task.

| Metric | Formula | Use When |
|--------|---------|----------|
| **pass@k** | P(≥1 success in k trials) | One success is enough |
| **pass^k** | P(all k trials succeed) | Reliability-critical |

**Example:** 75% per-trial success → pass@3 ≈ 98%, pass^3 ≈ 42%.

Use pass@k for exploration; pass^k for production reliability.

## Iterative Metrics (Ralph Pattern)

Traditional pass@k treats trials as independent. Iterative eval uses failures as feedback:

| Metric | Formula | Question |
|--------|---------|----------|
| **pass@k (iterative)** | Success within k retries with feedback | Can it recover? |
| **iterations_to_pass** | Retries until success | Learning speed |
| **recovery_rate** | (pass@k - pass@1) / (1 - pass@1) | % failures that recover |
| **feedback_sensitivity** | Δscore per iteration | Does guidance help? |

**Use case:** Agent has 60% pass@1. Is that its ceiling, or can it do better with feedback?

```
Iterative eval result:
├── pass@1: 60%         (baseline)
├── pass@3: 91%         (with retry + feedback)
└── recovery_rate: 78%  → Deploy with retry loop, not better prompts
```

## Multi-Agent Metrics

Single-agent metrics miss coordination failures:

| Metric | Formula | Measures |
|--------|---------|----------|
| **Task Score** | Σ(milestone × weight) | Goal achievement |
| **Handoff Success** | Completed / expected | Task transfers work? |
| **Comm Efficiency** | Useful messages / total | Signal vs noise |
| **Role Adherence** | On-role actions / total | Staying specialized? |
| **ToM Score** | Passed scenarios / total | Theory of mind |

## Match Metric to Target

| Target | What to Measure | Metric | Framework |
|--------|-----------------|--------|-----------|
| **Agents** | Task completion | pass@k / accuracy | DeepEval |
| **Agents** | Tool usage | ToolCorrectnessMetric | DeepEval |
| **Skills** | Activation (L1) | Precision/Recall/F1 | Custom |
| **Skills** | Methodology (L2) | LLM rubric | DeepEval GEval |
| **MCP Servers** | Tool calls | ToolCallAccuracy | RAGAS |
| **MCP Servers** | Reliability | MCPGauge 4-dim | Custom |
| **Prompts** | Output quality | LLM-as-judge | Braintrust |
| **Any** | Traces | Span analysis | Phoenix (local) |
| **Any** | Behavioral | Bloom scenarios | Anthropic Bloom |

## Building Evals: The Roadmap

From Anthropic's agent evaluation guide (2026):

```
Step 0: Start early with 20-50 tasks from actual failures
Step 1: Write unambiguous tasks (pass expert test)
Step 2: Build balanced problem sets (positive AND negative)
Step 3: Robust harness with clean environments per trial
Step 4: Thoughtful grader design (deterministic preferred)
Step 5: Read transcripts (verify graders, understand failures)
Step 6: Monitor saturation (100% → only tracks regressions)
Step 7: Maintain as living artifact (dedicated ownership)
```

## Common Pitfalls

| Trap | Fix |
|------|-----|
| Single test run | **5+ runs** - stochastic outputs |
| One-sided test set | **Balance positive/negative** - prevents overfitting |
| Measuring recall only | **Add precision** - high recall + low precision = noise |
| "Forced eval" inflation | **Realistic conditions** - forced mode inflates scores |
| No ground truth | **Label expectations** - must_trigger, should_not |
| Grader too rigid | **Accept valid variations** - grade outcome, not path |
| Shared state between runs | **Isolate environments** - leftover files cause correlation |
| Bypass vulnerabilities | **Design to require solving** - agents exploit loopholes |
| Eval saturation | **Expand difficulty** - high pass rates mask improvements |

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
| acceptable | Either outcome fine | Excluded |

## Defense in Depth (Swiss Cheese)

No single eval method catches everything. Layer them:

| Method | Speed | Coverage | Best For |
|--------|-------|----------|----------|
| Automated evals | Fast | Narrow | Regression prevention |
| Production monitoring | Real-time | Broad | Real behavior |
| A/B testing | Days/weeks | Statistical | Outcome measurement |
| Manual transcript review | Slow | Deep | Building intuition |
| Human studies | Very slow | Gold-standard | Subjective quality |

Use multiple methods; each layer catches what others miss.

## Framework Decision

| Situation | Use | Why |
|-----------|-----|-----|
| Python agent evals | **DeepEval** | TaskCompletionMetric, ToolCorrectness |
| TypeScript/Node | **Braintrust** | Identical Python/TS API |
| RAG pipelines | **RAGAS** | ToolCallF1, context metrics |
| Skill activation | **Custom** | Precision/recall with labeled expectations |
| Behavioral evals | **Bloom** | Automated scenario generation |
| Infrastructure | **Harbor, Promptfoo** | Containerized, YAML-based |

## Quick Reference

```
AGENTS
  Coding: Test suites (SWE-bench pattern)
  Conversational: Multi-grader (state + transcript + rubric)
  Research: LLM groundedness + coverage
  Metrics: pass@k (exploration), pass^k (reliability)

MULTI-AGENT
  Task: Milestone-weighted task score
  Coordination: Handoff success, comm efficiency
  Roles: Role adherence, work duplication
  Advanced: Theory of Mind (ToM) scenarios

PIPELINE (Sequential A → B → C)
  Level 1: Single-agent metrics per stage
  Level 2: Handoff quality between stages
  Level 3: End-to-end pipeline metrics
  Key: Find bottleneck stage, error propagation

ITERATIVE (Ralph Pattern)
  When: Deciding retry loop vs better prompts
  Metrics: iterations_to_pass, recovery_rate, feedback_sensitivity
  Key insight: pass@1 ≠ capability ceiling

SKILLS
  Level 1 (Activation): F1 with labeled expectations
  Level 2 (Methodology): GEval rubric (evidence, WHY, verification)
  Observable: skill_check, skill_match spans

MCP SERVERS
  RAGAS: ToolCallAccuracy, ToolCallF1
  MCPGauge: proactivity, compliance, effectiveness, overhead

BEHAVIORAL
  Bloom: Automated scenario generation for alignment properties
  Targets: sycophancy, self-preservation, sabotage

OBSERVABILITY
  ALL extensions should have OTel spans
  Skills: skill_check, skill_match
  Agents: agent_run, llm_call, tool_call
  MCP: mcp_server, mcp_call
```

## Domain Routing

| Detected | Load |
|----------|------|
| agent, task completion, pass@k | [agents.md](references/agents.md) |
| multi-agent, coordination, handoff | [multi-agent.md](references/multi-agent.md) |
| pipeline, sequential, stage, chain | [multi-agent.md](references/multi-agent.md#pipeline-evaluation-chainsequential) |
| iterative, retry, recovery, ralph | [iterative.md](references/iterative.md) |
| skill, activation, trigger | [skills.md](references/skills.md) |
| methodology, behavioral, adherence | [methodology.md](references/methodology.md) |
| MCP, tool call, server | [mcp.md](references/mcp.md) |
| prompt, quality, judge | [prompts.md](references/prompts.md) |
| trace, debug, analyze spans | [observability.md](references/observability.md) |
| security, red team, adversarial | [security.md](references/security.md) |
| benchmark, SWE-bench, WebArena | [benchmarks.md](references/benchmarks.md) |
| dataset, labeling | [datasets.md](references/datasets.md) |
| DeepEval, Braintrust, RAGAS | [frameworks.md](references/frameworks.md) |
| Full citations | [sources.md](references/sources.md) |
