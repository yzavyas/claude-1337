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
