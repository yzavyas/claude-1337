# REP-002: Mandates vs Motivations

> Does prescribing HOW help, hurt, or not matter?

## Hypothesis

Given WHAT + WHY + CONSTRAINTS, does adding HOW (mandate) improve outcomes?

```
Shared (all conditions):
├── WHAT: the task/goal
├── WHY: reasoning for quality
└── CONSTRAINTS: requirements, boundaries

Variable:
└── HOW: prescribed process (mandate) vs absent (motivation)
```

## Conditions

| Condition | Receives | HOW prescribed? |
|-----------|----------|-----------------|
| `motivation` | WHAT + WHY + CONSTRAINTS | No — Claude derives |
| `mandate-template` | + template artifacts | Yes — fill these sections |
| `mandate-structure` | + file/format structure | Yes — create these files |
| `mandate-role` | + expert persona | Yes — you are the architect |

## Dataset

**SWE-bench Verified** — Real GitHub issues requiring judgment.

Why: Tasks have natural ambiguity where mandate vs motivation should differentiate.

## Metrics

| Metric | What it measures | Grader |
|--------|------------------|--------|
| `pass@k` | Task completion | Code (test suite) |
| `recovery_rate` | Self-correction | Code (iterative) |
| `tokens_used` | Efficiency | Count |

## Run Phases

| Phase | Tasks | Runs/condition | Purpose |
|-------|-------|----------------|---------|
| Pilot | 2 | 5 | Validate harness |
| Signal | 20 | 5 | Detect effects |
| Full | 100+ | 5 | Statistical power |

## Usage

```bash
# From lab-1337/
uv run lab-1337 run -c experiments/rep-002/scenarios/pilot.yaml
```

## Structure

```
rep-002/
├── README.md
├── conditions/           # Prompting styles (the IV)
│   ├── motivation.md
│   ├── mandate-template.md
│   ├── mandate-structure.md
│   └── mandate-role.md
├── tasks/
│   └── pilot/            # 2 tasks for validation
├── scenarios/
│   └── pilot.yaml        # Run configuration
└── results/
```

## References

- [REP-002 Proposal](../../reps/rep-002-mandates-vs-motivations.md)
- [eval-1337](../../../plugins/eval-1337/) — Evaluation methodology
- [SWE-bench](https://www.swebench.com/) — Dataset
