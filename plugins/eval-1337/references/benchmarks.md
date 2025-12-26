# Benchmarks Reference

Standard benchmarks for evaluating agents, skills, MCP, and prompts.

## Benchmark by Target

| Target | Benchmark | Measures | Size |
|--------|-----------|----------|------|
| **Code Agents** | SWE-bench | Issue resolution | 2,294 |
| **Code Agents** | SWE-bench Verified | Human-validated | 500 |
| **Tool Use** | ToolBench | API calling | 16,464 |
| **Tool Use** | API-Bank | Function calling | 2,138 |
| **Multi-Agent** | MultiAgentBench | Coordination | varies |
| **Research** | ScienceAgentBench | Scientific workflows | 102 |
| **Security** | SEC-bench | Security tasks | varies |
| **Browsing** | WebArena | Web navigation | 812 |

## Code Agent Benchmarks

### SWE-bench

Industry-standard for code agents.

```
Input: GitHub issue + repository
Output: Generated patch
Success: Repository tests pass

Accuracy = Resolved / Total
```

**Variants:**
| Variant | Size | Notes |
|---------|------|-------|
| Full | 2,294 | Original, noisy |
| Lite | 300 | Subset |
| Verified | 500 | Human-validated |
| Pro | 1,865 | Anti-contamination |

**Run locally:**
```bash
git clone https://github.com/princeton-nlp/SWE-bench
cd SWE-bench
pip install -e .

# Evaluate
python -m swebench.harness.run_evaluation \
    --predictions_path ./preds.json \
    --swe_bench_tasks test \
    --log_dir ./logs
```

### HumanEval

Code generation (not agent-specific but useful baseline).

```python
# Example task
def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """Check if any two numbers are closer than threshold."""
    pass  # Model completes this
```

**Metric:** pass@k (passes k attempts)

## Tool Use Benchmarks

### ToolBench

Large-scale API benchmark.

| Stat | Value |
|------|-------|
| APIs | 16,464 |
| Categories | 49 |
| Tools | 3,451 |

**Metrics:**
- Pass Rate: Task completed
- Win Rate: vs baseline

### API-Bank

Function calling evaluation.

```python
# Example
{
    "query": "Book a flight from NYC to LA on Dec 25",
    "expected_calls": [
        {"function": "search_flights", "args": {...}},
        {"function": "book_flight", "args": {...}}
    ]
}
```

### BFCL (Berkeley Function Calling Leaderboard)

Live leaderboard for function calling.

**Categories:**
- Simple (single function)
- Multiple (parallel calls)
- Parallel (concurrent execution)
- Nested (function in function)

**URL:** [gorilla.cs.berkeley.edu/leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html)

## Multi-Agent Benchmarks

### MultiAgentBench (2025)

```python
# Evaluates
- Communication efficiency
- Task coordination
- Role specialization
- Conflict resolution
```

### ChatDev

Software development with agent teams.

```
Roles: CEO, CTO, Programmer, Tester
Task: Build application from description
Metric: Functional code produced
```

## Research & Reasoning

### ScienceAgentBench

Scientific workflow automation.

```
Tasks: Data analysis, hypothesis generation, paper writing
Size: 102 expert-validated tasks
Metric: Task completion accuracy
```

### AAAR-1.0

Academic research reasoning.

```
Focus: Paper comprehension, citation analysis
Metric: Accuracy on research tasks
```

## Web & Browsing

### WebArena

Realistic web navigation.

```python
# Example task
{
    "task": "Find cheapest flight from NYC to LA for Dec 25",
    "start_url": "https://booking-site.com",
    "success": "Booking confirmation displayed"
}
```

**Size:** 812 tasks

### Mind2Web

Web agent generalization.

```
Websites: 137 real sites
Tasks: 2,000+ annotated
Focus: Cross-site generalization
```

## Security Benchmarks

### SEC-bench

Security-focused agent tasks.

```
Tasks:
- Vulnerability analysis
- Patch generation
- Security audit
```

### CyberSecEval

Meta's cybersecurity benchmark.

```
Categories:
- Exploit generation (should refuse)
- Defense recommendations
- Code review
```

## Benchmark Selection Guide

| Goal | Use | Why |
|------|-----|-----|
| Code agent | SWE-bench Verified | Gold standard, validated |
| Tool calling | BFCL | Live leaderboard |
| API coverage | ToolBench | Scale |
| Web agent | WebArena | Realistic |
| Security | SEC-bench + CyberSecEval | Both offense/defense |
| Research | ScienceAgentBench | Domain expertise |

## CLASSic Framework (Enterprise)

Five dimensions for enterprise evaluation:

| Dimension | Metric | Target |
|-----------|--------|--------|
| **C**ost | $/task | Budget |
| **L**atency | Time to complete | SLA |
| **A**ccuracy | Task success | >90% |
| **S**tability | Variance across runs | <10% |
| **S**ecurity | Attack resistance | >95% |

```python
def classic_eval(agent, test_cases):
    results = []
    for case in test_cases:
        start = time.time()
        cost_before = get_cost()

        output = agent.run(case.input)

        results.append({
            "cost": get_cost() - cost_before,
            "latency": time.time() - start,
            "accuracy": output == case.expected,
            "security": security_check(output)
        })

    # Aggregate
    return {
        "cost_avg": mean([r["cost"] for r in results]),
        "latency_p50": percentile([r["latency"] for r in results], 50),
        "accuracy": mean([r["accuracy"] for r in results]),
        "security": mean([r["security"] for r in results]),
    }
```

## Running Benchmarks Locally

```bash
# SWE-bench
pip install swebench
python -m swebench.harness.run_evaluation ...

# ToolBench
git clone https://github.com/OpenBMB/ToolBench
python eval/eval_pass_rate.py ...

# WebArena
git clone https://github.com/web-arena-x/webarena
python run.py --agent your_agent
```

## Sources

- [SWE-bench](https://www.swebench.com/) - Code agent benchmark
- [ToolBench](https://github.com/OpenBMB/ToolBench) - API calling
- [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) - Function calling leaderboard
- [WebArena](https://webarena.dev/) - Web agent benchmark
- [MultiAgentBench](https://arxiv.org/abs/2503.01935) - Multi-agent evaluation
- [CLASSic](https://arxiv.org/abs/2502.xxxxx) - Enterprise AI evaluation (ICLR 2025)
- [KDD 2025 Tutorial](https://sap-samples.github.io/llm-agents-eval-tutorial/) - Comprehensive guide
