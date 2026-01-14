# Multi-Agent Evaluation

Measuring coordination, communication, and collective task completion.

## Why Multi-Agent Evals Differ

Single-agent metrics miss:

| Gap | What's Hidden |
|-----|---------------|
| Communication overhead | Agents chattering without progress |
| Role confusion | Multiple agents doing same work |
| Handoff failures | Tasks dropped between agents |
| Coordination bottlenecks | Waiting on each other |
| Emergent failures | System fails despite individual success |

## Coordination Topologies

Test different structures:

```
STAR              CHAIN             TREE              GRAPH
  ┌─────┐           A                 A               A───B
  │  O  │           │                / \             /│\ /│
  └──┬──┘           B               B   C           C D E F
   ┌─┼─┐            │               │               │ └┬┘ │
   A B C            C               D               └──G──┘

Orchestrator     Sequential      Hierarchical     Peer-to-peer
```

| Topology | Best For | Failure Mode |
|----------|----------|--------------|
| Star | Central control | Orchestrator bottleneck |
| Chain | Sequential workflows | Single point of failure |
| Tree | Hierarchical delegation | Deep chains slow |
| Graph | Flexible collaboration | Coordination chaos |

## Pipeline Evaluation (Chain/Sequential)

Sequential agent pipelines (A → B → C) are common but don't need full coordination metrics.

### When to Use Pipeline vs Multi-Agent Metrics

| Pattern | Example | Eval Approach |
|---------|---------|---------------|
| **Pipeline** | Planner → Executor → Reviewer | Per-stage + handoffs + end-to-end |
| **Tool-as-Agent** | Agent A calls Agent B as tool | Single-agent (A is primary) |
| **Coordinated** | A ↔ B (back-and-forth) | Full multi-agent metrics |
| **Parallel** | A \|\| B (concurrent) | Multi-agent + parallel efficiency |

### Three-Level Pipeline Eval

```
┌─────────────────────────────────────────────────────────┐
│  LEVEL 3: END-TO-END                                    │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐             │
│  │ Agent A │───▶│ Agent B │───▶│ Agent C │             │
│  │ (plan)  │    │ (execute)│   │ (review)│             │
│  └─────────┘    └─────────┘    └─────────┘             │
│       │              │              │                   │
│  LEVEL 1:       LEVEL 1:       LEVEL 1:                │
│  Single-agent   Single-agent   Single-agent            │
│                                                         │
│       └──── LEVEL 2: Handoff Quality ────┘             │
└─────────────────────────────────────────────────────────┘
```

### Level 1: Per-Stage Metrics

Evaluate each agent in isolation:

```python
def eval_pipeline_stages(pipeline, test_cases):
    """Evaluate each stage independently."""
    stage_results = {}

    for stage in pipeline.stages:
        stage_cases = extract_stage_cases(test_cases, stage.name)

        stage_results[stage.name] = {
            "task_completion": eval_task_completion(stage, stage_cases),
            "tool_correctness": eval_tool_correctness(stage, stage_cases),
            "pass@1": eval_pass_at_1(stage, stage_cases)
        }

    return stage_results
```

### Level 2: Handoff Metrics

Did output of Stage N work as input for Stage N+1?

| Metric | Formula | Question |
|--------|---------|----------|
| **Handoff Success** | Valid handoffs / total | Does output connect? |
| **Schema Compliance** | Valid schemas / total | Correct format? |
| **Information Loss** | Missing fields / expected | Data preserved? |
| **Error Propagation** | Downstream failures from upstream | Do errors cascade? |

```python
def eval_handoffs(pipeline, test_cases):
    """Evaluate handoff quality between stages."""
    results = []

    for case in test_cases:
        handoff_results = []
        prev_output = case.input

        for i, stage in enumerate(pipeline.stages):
            output = stage.run(prev_output)

            if i < len(pipeline.stages) - 1:
                next_stage = pipeline.stages[i + 1]

                handoff_results.append({
                    "from": stage.name,
                    "to": next_stage.name,
                    "output_valid": is_valid_output(output, stage.output_schema),
                    "input_valid": is_valid_input(output, next_stage.input_schema),
                    "handoff_success": can_accept(next_stage, output)
                })

            prev_output = output

        results.append({
            "case": case.id,
            "handoffs": handoff_results,
            "all_handoffs_success": all(h["handoff_success"] for h in handoff_results)
        })

    return {
        "handoff_success_rate": mean(r["all_handoffs_success"] for r in results),
        "per_handoff": aggregate_by_handoff(results)
    }
```

### Level 3: End-to-End Metrics

The whole pipeline as one unit:

```python
def eval_pipeline_e2e(pipeline, test_cases, n_trials=5):
    """Evaluate complete pipeline end-to-end."""
    results = []

    for case in test_cases:
        trial_results = []

        for trial in range(n_trials):
            # Run full pipeline
            trace = pipeline.run(case.input)

            trial_results.append({
                "success": verify_output(trace.final_output, case.expected),
                "stages_completed": trace.stages_completed,
                "total_tokens": trace.total_tokens,
                "total_latency_ms": trace.total_latency_ms,
                "failure_stage": trace.failure_stage if not trace.success else None
            })

        results.append({
            "case": case.id,
            "pass@1": trial_results[0]["success"],
            "pass@k": any(t["success"] for t in trial_results),
            "success_rate": mean(t["success"] for t in trial_results),
            "avg_tokens": mean(t["total_tokens"] for t in trial_results),
            "avg_latency_ms": mean(t["total_latency_ms"] for t in trial_results)
        })

    return aggregate_pipeline_results(results)
```

### Pipeline-Specific Metrics

| Metric | Formula | Question |
|--------|---------|----------|
| **Stage Success Rate** | Per-stage pass / total | Which stage fails most? |
| **Bottleneck Stage** | Max(latency or tokens) | Where to optimize? |
| **Error Origin** | First failure stage | Root cause location |
| **Recovery Potential** | Failures recoverable downstream | Can later stages fix? |

```python
def identify_bottleneck(pipeline_results):
    """Find the slowest or most expensive stage."""
    stage_stats = {}

    for result in pipeline_results:
        for stage, metrics in result["stage_metrics"].items():
            if stage not in stage_stats:
                stage_stats[stage] = {"latencies": [], "tokens": [], "failures": 0}

            stage_stats[stage]["latencies"].append(metrics["latency_ms"])
            stage_stats[stage]["tokens"].append(metrics["tokens"])
            if not metrics["success"]:
                stage_stats[stage]["failures"] += 1

    return {
        "latency_bottleneck": max(stage_stats, key=lambda s: mean(stage_stats[s]["latencies"])),
        "token_bottleneck": max(stage_stats, key=lambda s: mean(stage_stats[s]["tokens"])),
        "failure_bottleneck": max(stage_stats, key=lambda s: stage_stats[s]["failures"])
    }
```

### Pipeline Dataset Structure

```json
{
  "name": "code-review-pipeline-v1",
  "target": "pipeline",
  "stages": [
    {"name": "analyzer", "input_schema": "code", "output_schema": "analysis"},
    {"name": "reviewer", "input_schema": "analysis", "output_schema": "review"},
    {"name": "suggester", "input_schema": "review", "output_schema": "suggestions"}
  ],
  "cases": [
    {
      "id": "pipeline-001",
      "input": {"code": "def foo(): pass"},
      "expected_final": {"suggestions": ["Add docstring", "Add type hints"]},
      "stage_expectations": {
        "analyzer": {"must_detect": ["missing_docstring"]},
        "reviewer": {"must_flag": "documentation"},
        "suggester": {"min_suggestions": 1}
      }
    }
  ]
}
```

## Core Metrics

### Task Achievement

| Metric | Formula | Measures |
|--------|---------|----------|
| **Task Score** | Σ(milestone × weight) | Overall goal completion |
| **Milestone KPI** | Milestones hit / total | Incremental progress |
| **Time to Complete** | End - start | Efficiency |

```python
def task_score(milestones: list, achieved: set) -> float:
    return sum(
        m["weight"] for m in milestones
        if m["id"] in achieved
    )

# Example
milestones = [
    {"id": "research", "weight": 0.2},
    {"id": "draft", "weight": 0.3},
    {"id": "review", "weight": 0.2},
    {"id": "final", "weight": 0.3}
]
achieved = {"research", "draft", "review"}
score = task_score(milestones, achieved)  # 0.7
```

### Communication

| Metric | Formula | Measures |
|--------|---------|----------|
| **Communication Efficiency** | Useful messages / total | Signal vs noise |
| **Coordination Overhead** | Meta-messages / total | Planning vs doing |
| **Response Latency** | Avg time to respond | Responsiveness |

```python
def communication_metrics(messages: list) -> dict:
    useful = [m for m in messages if m.type in ("task", "result", "data")]
    meta = [m for m in messages if m.type in ("query", "status", "ack")]

    return {
        "efficiency": len(useful) / len(messages) if messages else 0,
        "overhead": len(meta) / len(messages) if messages else 0,
        "total_messages": len(messages)
    }
```

### Coordination

| Metric | Formula | Measures |
|--------|---------|----------|
| **Handoff Success** | Completed handoffs / expected | Task transfers work? |
| **Parallel Efficiency** | Concurrent work / total | Using parallelism? |
| **Conflict Rate** | Conflicts / decisions | Disagreement frequency |
| **Resolution Rate** | Resolved / conflicts | Can they resolve? |

```python
def handoff_success(expected_handoffs: list, messages: list) -> float:
    """
    Track if expected task transfers actually happened.
    """
    completed = set()

    # Look for task->result pairs between expected agents
    for i, msg in enumerate(messages):
        if msg.type == "task":
            # Find corresponding result
            for future in messages[i+1:]:
                if (future.sender == msg.receiver and
                    future.receiver == msg.sender and
                    future.type == "result"):
                    completed.add((msg.sender, msg.receiver))
                    break

    expected_set = {(h["from"], h["to"]) for h in expected_handoffs}
    return len(completed & expected_set) / len(expected_set) if expected_set else 1.0
```

### Role Adherence

| Metric | Formula | Measures |
|--------|---------|----------|
| **Role Adherence** | On-role actions / total | Staying specialized? |
| **Work Duplication** | Duplicate tasks / total | Redundant effort? |
| **Capability Match** | Capable actions / assigned | Right agent for job? |

```python
def role_adherence(agents: dict, actions: list) -> float:
    """
    Check if agents stick to their defined capabilities.
    """
    on_role = 0

    for action in actions:
        agent = agents[action.agent_id]
        if action.type in agent["capabilities"]:
            on_role += 1

    return on_role / len(actions) if actions else 1.0
```

## Theory of Mind (ToM)

Can agents reason about each other's states?

| Test | Scenario | Optimal Behavior |
|------|----------|------------------|
| **Proactive Sharing** | A has info B needs | A shares without being asked |
| **Action Coordination** | A's action blocks B | A checks with B first |
| **Error Awareness** | A made mistake B saw | B informs A |
| **Belief Tracking** | A knows X, B doesn't know A knows | A anticipates B's uncertainty |

```python
def eval_theory_of_mind(system, scenarios: list) -> dict:
    """
    Test ToM capabilities.
    Based on LLM-Coordination benchmark (NAACL 2025).
    """
    results = []

    for scenario in scenarios:
        # Set up information asymmetry
        setup_scenario(system, scenario)

        # Run interaction
        trace = system.run(max_steps=10)

        # Check for ToM behavior
        exhibited = check_tom_behavior(trace, scenario["optimal"])

        results.append({
            "scenario": scenario["name"],
            "passed": exhibited,
            "behavior_observed": extract_behavior(trace)
        })

    return {
        "tom_score": sum(r["passed"] for r in results) / len(results),
        "weak_areas": [r["scenario"] for r in results if not r["passed"]]
    }
```

## Dataset Structure

```json
{
  "name": "multi-agent-research-v1",
  "target": "multi-agent",
  "topology": "star",
  "agents": [
    {
      "id": "coordinator",
      "role": "orchestrator",
      "capabilities": ["planning", "delegation", "synthesis"]
    },
    {
      "id": "researcher",
      "role": "gatherer",
      "capabilities": ["search", "summarize"]
    },
    {
      "id": "writer",
      "role": "creator",
      "capabilities": ["draft", "edit"]
    }
  ],
  "cases": [
    {
      "id": "report-001",
      "task": "Write report on AI safety",
      "milestones": [
        {"id": "sources", "description": "Sources gathered", "weight": 0.2},
        {"id": "outline", "description": "Outline created", "weight": 0.1},
        {"id": "draft", "description": "Draft complete", "weight": 0.4},
        {"id": "final", "description": "Final delivered", "weight": 0.3}
      ],
      "expected_handoffs": [
        {"from": "coordinator", "to": "researcher", "task": "gather"},
        {"from": "researcher", "to": "coordinator", "task": "sources_ready"},
        {"from": "coordinator", "to": "writer", "task": "write"},
        {"from": "writer", "to": "coordinator", "task": "draft_ready"}
      ],
      "max_rounds": 20,
      "max_messages": 50
    }
  ]
}
```

## Evaluation Implementation

```python
class MultiAgentEvaluator:
    def __init__(self, config: dict):
        self.agents = {a["id"]: a for a in config["agents"]}
        self.topology = config["topology"]
        self.messages = []
        self.actions = []
        self.milestones_achieved = set()

    def evaluate(self, test_case: dict) -> dict:
        """Run full multi-agent evaluation."""

        # Run the system
        trace = self.run_system(test_case)

        # Compute all metrics
        return {
            # Task
            "task_score": self._task_score(test_case),
            "milestones": len(self.milestones_achieved),

            # Communication
            "comm_efficiency": self._comm_efficiency(),
            "total_messages": len(self.messages),

            # Coordination
            "handoff_success": self._handoff_success(test_case),
            "parallel_efficiency": self._parallel_efficiency(),

            # Roles
            "role_adherence": self._role_adherence(),

            # Cost
            "total_tokens": sum(m.tokens for m in self.messages),
            "tokens_per_milestone": self._tokens_per_milestone()
        }

    def _task_score(self, case: dict) -> float:
        return sum(
            m["weight"] for m in case["milestones"]
            if m["id"] in self.milestones_achieved
        )

    def _comm_efficiency(self) -> float:
        if not self.messages:
            return 0
        useful = sum(1 for m in self.messages if m.type in ("task", "result"))
        return useful / len(self.messages)

    def _parallel_efficiency(self) -> float:
        """Measure concurrent vs sequential work."""
        if not self.actions:
            return 0

        # Bucket by time window (1 second)
        buckets = {}
        for action in self.actions:
            bucket = int(action.timestamp)
            if bucket not in buckets:
                buckets[bucket] = set()
            buckets[bucket].add(action.agent_id)

        # Parallel = multiple agents same bucket
        parallel = sum(1 for agents in buckets.values() if len(agents) > 1)
        return parallel / len(buckets)
```

## Thresholds

| Metric | Poor | Acceptable | Good | Excellent |
|--------|------|------------|------|-----------|
| Task Score | <0.5 | 0.5-0.7 | 0.7-0.9 | >0.9 |
| Comm Efficiency | <0.3 | 0.3-0.5 | 0.5-0.7 | >0.7 |
| Handoff Success | <0.6 | 0.6-0.8 | 0.8-0.95 | >0.95 |
| Role Adherence | <0.7 | 0.7-0.85 | 0.85-0.95 | >0.95 |
| ToM Score | <0.3 | 0.3-0.5 | 0.5-0.7 | >0.7 |

## Common Failure Patterns

| Pattern | Symptom | Fix |
|---------|---------|-----|
| Chatter loop | High messages, low progress | Add conversation limits |
| Role confusion | Multiple agents same task | Clearer role definitions |
| Handoff drops | Tasks disappear | Explicit acknowledgments |
| Bottleneck | One agent overwhelmed | Better load distribution |
| No parallelism | Sequential when could parallel | Identify independent tasks |

## Sources

- [MultiAgentBench (ACL 2025)](https://aclanthology.org/2025.acl-long.421/) - Milestone KPI, coordination protocols
- [LLM-Coordination (NAACL 2025)](https://aclanthology.org/2025.findings-naacl.448/) - Theory of Mind evaluation
- [Multi-Agent Reasoning Benchmark](https://arxiv.org/abs/2503.01935) - Collaboration vs competition
