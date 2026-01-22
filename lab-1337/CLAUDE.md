# Lab-1337 Project Documentation

Evidence-based research for cognitive extension methodology. This lab produces hard data, not opinions.

---

## Project Structure

```
lab-1337/
├── reps/                   # REPs (Research Enhancement Proposals)
├── rips/                   # RIPs (Research Implementation Plans)
├── experiments/            # Each experiment is its own workspace
│   └── rep-002/
│       ├── conditions/     # Independent variables (prompting styles)
│       ├── tasks/          # Problems to solve
│       ├── scenarios/      # Batch configurations
│       └── results/        # Output data
├── findings/               # Published findings
├── agents/                 # Custom agents for analysis/reporting
├── src/lab/               # Core harness (hexagonal architecture)
└── scratch/               # Working documents (gitignored)
```

---

## Hexagonal Architecture

The harness uses ports-and-adapters for clean separation:

```
                    ┌─────────────────────────────────────────┐
                    │              DOMAIN LAYER               │
                    │  models.py: Condition, Task, Batch, Run │
                    │  services.py: PromptBuilder, RunSelector│
                    │  statistics.py: Welford's algorithm     │
                    └─────────────────────────────────────────┘
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         │                             │                             │
         ▼                             ▼                             ▼
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│  DRIVING PORTS  │         │   CONTAINER.PY  │         │  DRIVEN PORTS   │
│  (Primary)      │         │   (DI wiring)   │         │  (Secondary)    │
│  - use_cases.py │◀────────│                 │────────▶│  - llm.py       │
│                 │         │                 │         │  - grader.py    │
│                 │         │                 │         │  - tracer.py    │
└─────────────────┘         └─────────────────┘         │  - storage.py   │
                                                        └─────────────────┘
                                                                 │
                                    ┌────────────────────────────┼────────────────────────────┐
                                    │                            │                            │
                                    ▼                            ▼                            ▼
                         ┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
                         │   LLM ADAPTERS  │          │ GRADER ADAPTERS │          │ OTHER ADAPTERS  │
                         │  claude_sdk.py  │          │  mock_grader    │          │  filesystem.py  │
                         │                 │          │  function       │          │  phoenix.py     │
                         │                 │          │                 │          │  console_tracer │
                         └─────────────────┘          └─────────────────┘          └─────────────────┘
```

### Key Files

| File | Purpose |
|------|---------|
| `domain/models.py` | Pydantic models: Condition, Task, Batch, Run, RunResult |
| `domain/services.py` | PromptBuilder (combines condition + task), RunSelector |
| `ports/driving/use_cases.py` | RunExperimentUseCase - main orchestration |
| `ports/driven/*.py` | Port interfaces (LLMPort, GraderPort, etc.) |
| `adapters/driven/*.py` | Implementations (ClaudeSDK, FunctionGrader, etc.) |
| `container.py` | Dependency injection - wires adapters together |
| `cli.py` | Domain-driven CLI (noun-verb pattern) |

---

## Domain Ontology

| Concept | Definition | Maps To |
|---------|------------|---------|
| **Experiment** | A scientific investigation | `experiments/<name>/` directory |
| **Batch** | A specific execution configuration | `scenarios/*.yaml` |
| **Condition** | The independent variable (prompting style) | `conditions/*.md` |
| **Task** | A problem to solve | `tasks/*.yaml` |
| **Run** | Single task + condition + attempt | Generated at runtime |
| **RunResult** | Outcome with metrics | Stored in `results/` |

### Condition → Task → Run Flow

```
Condition (system prompt)  ─┐
                            ├─→ Run ─→ RunResult
Task (user message)        ─┘
```

1. **Condition.prompt** becomes the **system prompt** (how to approach work)
2. **Task.prompt** becomes the **user message** (what to solve)
3. **Run** executes the combination, captures metrics

---

## CLI Reference

### Installation

```bash
cd lab-1337
uv sync                    # Install dependencies
uv run lab-1337 --help     # Verify installation
```

### Core Commands

```bash
# Experiment management
lab-1337 experiment list                    # List all experiments
lab-1337 experiment show rep-002            # Show experiment details
lab-1337 experiment init my-experiment      # Scaffold new experiment
lab-1337 experiment validate rep-002        # Validate structure

# Batch execution
lab-1337 batch list -e rep-002              # List batches
lab-1337 batch show pilot -e rep-002        # Show batch details
lab-1337 batch validate pilot -e rep-002    # Validate batch config
lab-1337 batch run pilot -e rep-002         # Execute batch

# Inspection
lab-1337 condition list -e rep-002          # List conditions
lab-1337 condition show motivation -e rep-002
lab-1337 task list -e rep-002               # List tasks
lab-1337 task show pytest-dev__pytest-10051 -e rep-002

# Results
lab-1337 result list -e rep-002             # List result files
lab-1337 result show results.json -e rep-002
lab-1337 result verify results.json         # Strawberry verification

# Observability
lab-1337 observe phoenix                    # Launch Phoenix UI
```

### Grader Options

```bash
lab-1337 batch run pilot -e rep-002 --grader mock           # Random pass/fail
lab-1337 batch run pilot -e rep-002 --grader function       # Custom function grader
```

---

## Running Experiments

### Batch Execution Flow

```
1. CLI loads batch config (scenarios/*.yaml)
2. Container wires up adapters (LLM, Grader, Tracer, Storage)
3. For each Run (task × condition × attempt):
   a. Grader.setup() → prepares workspace
   b. LLM.generate() → Claude solves with condition as system prompt
   c. Grader.get_solution() → captures solution
   d. Grader.grade() → evaluates via function grader
   e. Storage.append_result() → streams to disk
4. Storage.save_summary() → final aggregation
```

### Full Experiment Example

```bash
# 1. Validate experiment structure
lab-1337 experiment validate rep-002

# 2. Validate batch configuration
lab-1337 batch validate v2-pilot -e rep-002

# 3. Dry run (show what would execute)
lab-1337 batch run v2-pilot -e rep-002 -n

# 4. Execute with function grader
lab-1337 batch run v2-pilot -e rep-002 --grader function
```

### Scenario Configuration

```yaml
# scenarios/v2-pilot.yaml
name: rep-002-v2-pilot

# Grader selection
grader: function  # or: mock

# Task references (full path or short name)
tasks:
  - tasks/discriminating/safe-calculator-task.yaml

# Condition references (full path or short name)
conditions:
  - conditions/baseline.md
  - conditions/motivation.md
  - conditions/mandate-template.md

# Execution settings
model: sonnet              # sonnet, opus, haiku
runs_per_condition: 3      # Repetitions for statistical power

# Iteration strategy
iteration:
  strategy: none           # none, self-review, external
  max_iterations: 1
```

### Condition File Format

```markdown
---
name: motivation
description: WHAT + WHY + CONSTRAINTS only. Claude derives HOW.
type: motivation
---

# Motivation Condition

You're solving a real software issue. Here's what matters:

## WHY Quality Matters
- This is production code that real users depend on
- Your fix becomes part of the codebase others maintain

## CONSTRAINTS
- The fix must pass the existing test suite
- Don't break unrelated functionality

## Your Task
Understand the issue deeply. Fix it properly.
```

The markdown body (after frontmatter) becomes the **system prompt**.

---

## Task File Format

### Function Grader Tasks

```yaml
id: safe-calculator
prompt: |
  Write a function `calculate(expression: str) -> float` that
  safely evaluates arithmetic expressions.
grader:
  type: function
  module: lab.evals.safe_calculator
  function: grade_implementation
```

---

## Adding New Graders

Implement the `GraderPort` protocol:

```python
class GraderPort(Protocol):
    async def setup(self, task: Task) -> str | None:
        """Setup workspace, return cwd for agent."""
        ...

    async def get_solution(self, task: Task) -> str:
        """Capture agent's solution after execution."""
        ...

    async def grade(self, solution: str, task: Task) -> GradeResult:
        """Evaluate the solution."""
        ...

    async def teardown(self, task: Task) -> None:
        """Cleanup resources."""
        ...
```

Register in `container.py`:
```python
elif self.config.grader == "my-grader":
    self._grader = MyGraderAdapter(...)
```

---

## Observability

### Phoenix (Local Tracing)

```bash
# Launch Phoenix UI
lab-1337 observe phoenix

# Visit http://localhost:6006
# All experiment runs stream traces automatically
```

### Console Tracer (Default)

Rich console output with structured spans:
```
▸ experiment_batch started
  batch_name: rep-002-pilot
  total_runs: 15
  ▸ experiment_run started
    task_id: pytest-dev__pytest-10051
    condition: motivation
    passed: True
  ◂ experiment_run (45230ms)
```

---

## Current Experiments

### REP-001: Rigor is What You Want

**Status**: Implemented
**Finding**: Self-review iteration improves pass rate 86.6% → 98.8%

### REP-002: Mandates vs Motivations

**Status**: Running
**Hypothesis**: Motivation-based prompting discriminates on high-ambiguity tasks

**Conditions**:
| Condition | Type | WHAT | WHY | CONSTRAINTS | HOW |
|-----------|------|------|-----|-------------|-----|
| baseline | Control | ✓ | | | |
| motivation | Motivation | ✓ | ✓ | ✓ | |
| mandate-template | Mandate | ✓ | ✓ | ✓ | Template artifacts |
| mandate-structure | Mandate | ✓ | ✓ | ✓ | File structure |
| mandate-role | Mandate | ✓ | ✓ | ✓ | Expert persona |

**Tasks**: Custom discriminating tasks with function grader
**Design**: Uses function grader for flexible evaluation

---

## Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `LAB_ROOT` | Override lab root directory | `/path/to/lab-1337` |
| `ANTHROPIC_API_KEY` | Claude API access | (set in environment) |

---

## Development

### Running Tests

```bash
uv run pytest tests/
```

### Adding Dependencies

```bash
uv add <package>
uv add --dev <dev-package>
```

### Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **DI Container** | Manual (container.py) | No magic, explicit wiring |
| **Domain Models** | Pydantic | Validation + serialization |
| **CLI** | Click + Rich | Domain-driven, beautiful output |
| **Async** | asyncio | Streaming results, concurrent ops |
| **Tracing** | OTel → Phoenix | Local-first observability |

---

## For New Claude Instances

1. **Understand the domain**: Read `scratch/domain-ontology.md`
2. **Check current work**: Look at `reps/rep-002-*.md` for active experiments
3. **Run commands**: Use `lab-1337 --help` to explore CLI
4. **Read conditions**: Understand what's being tested in `experiments/rep-002/conditions/`

---

## TODOs

### LLM-as-Judge Methodology (Priority: High)

**Problem**: Current `llm_judge.py` imports DeepEval but doesn't use it properly — just prompts Claude Haiku with a rubric.

**What's needed**:
1. Implement DeepEval GEval correctly for rubric-based evaluation
2. Or replace with proper evaluation framework
3. Add inter-rater reliability testing
4. Document calibration approach

**Why it matters**: LLM-as-judge favored verbose code over secure code. Without proper evaluation methodology, quality metrics are unreliable.

**Files**: `src/lab/adapters/driven/llm_judge.py`

**Reference**: REP-002 interim findings show LLM-as-judge and approach analysis disagree — need to understand why and fix evaluation.
