# IMP-001: Rigor is What You Want

- **Status**: Draft
- **LEP**: [LEP-001](../proposals/lep-001-rigor-is-what-you-want.md)
- **Created**: 2026-01-15
- **Authors**: Collaborative Intelligence Session

## Overview

Implementation plan for measuring the effectiveness of spec-driven development frameworks (BMAD, GSD, spec-kit) compared to baseline Claude.

## Design

### Experimental Conditions

| Condition | Description |
|-----------|-------------|
| `baseline` | Pure Claude, no methodology |
| `speckit` | GitHub's 7-step process (Constitution→Implement) |
| `gsd` | Get Shit Done (PROJECT/ROADMAP/STATE/PLAN) |
| `bmad` | BMAD Method (21 agents, scale-adaptive) |

### Task Corpus

Stratified by complexity:

| Category | Example | Hypothesis |
|----------|---------|------------|
| `trivial` | Fix typo | Methodology overhead hurts |
| `simple` | Add endpoint | Minimal difference |
| `multi-step` | Add auth flow | Methodologies may help |
| `architecture` | Refactor service | Methodologies should help |
| `ambiguous` | "Make it faster" | Clarification value |

### Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `pass@k` | completion | Task succeeds in k attempts |
| `pass^k` | reliability | Task succeeds in ALL k attempts |
| `code_quality` | LLM-judge | Maintainability, structure |
| `tokens_used` | efficiency | Cost measurement |
| `recovery_rate` | robustness | (pass@3 - pass@1) / (1 - pass@1) |

### Architecture

```
experiments/lep-001-rigor-is-what-you-want/
├── src/
│   └── rigor_experiment/
│       ├── __main__.py       # CLI entrypoint
│       ├── conditions.py     # Methodology loaders
│       ├── tasks.py          # Task corpus
│       ├── runner.py         # Experiment orchestration
│       └── metrics.py        # Measurement & analysis
├── methodologies/            # Crystallized methodology prompts
│   ├── speckit.md
│   ├── gsd.md
│   └── bmad.md
├── corpus/                   # Task definitions + test suites
│   └── tasks.json
└── results/                  # Output
```

### Methodology Loading

Each methodology crystallized into a system prompt:

```python
def load_methodology(name: str) -> str | None:
    """Load methodology prompt for condition."""
    if name == "baseline":
        return None
    path = METHODOLOGIES_DIR / f"{name}.md"
    return path.read_text()

async def run_task(task: Task, methodology: str | None) -> Result:
    """Run single task with optional methodology."""
    messages = [{"role": "user", "content": task.prompt}]

    client = anthropic.Anthropic()
    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        system=methodology,  # None for baseline
        messages=messages,
        max_tokens=8192,
    )
    # ...
```

## Implementation

### Phase 1: Infrastructure

- [ ] Create experiment package structure
- [ ] Crystallize methodology prompts (speckit, gsd, bmad)
- [ ] Implement task corpus loader
- [ ] Implement condition runner

### Phase 2: Task Corpus

- [ ] Define 5+ tasks per category
- [ ] Create test suites for each task (ground truth)
- [ ] Validate tasks work with baseline Claude

### Phase 3: Metrics

- [ ] Implement pass@k calculation
- [ ] Implement LLM-as-judge for code quality
- [ ] Add token/time tracking
- [ ] Report generation

### Phase 4: Execution

- [ ] Run pilot (1 task, all conditions, 3 runs)
- [ ] Validate metrics collection
- [ ] Run full experiment
- [ ] Generate report

## Testing Strategy

- Unit tests for corpus loading, metric calculation
- Integration test: single task through full pipeline
- Pilot run before full execution

## Dependencies

- `anthropic` - Claude Agent SDK
- `pydantic` - Data models
- `rich` - CLI output
- `pandas` - Results analysis
- `plotly` - Visualization

## Risks

| Risk | Mitigation |
|------|------------|
| High API cost | Start with pilot, estimate full cost |
| Task corpus bias | Multiple reviewers, stratified sampling |
| Methodology loading variance | Fixed prompts, version control |
| Model stochasticity | Multiple runs per condition (5+) |

## Open Questions

1. **Task selection**: Source from existing benchmarks (SWE-bench) or create custom? Custom gives control, existing gives comparability.

2. **Model coverage**: Run on Sonnet only, or also Haiku/Opus to check if results generalize?

3. **Methodology fairness**: How to ensure each framework is represented fairly as a prompt? May need review by framework authors.
