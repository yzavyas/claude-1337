"""Domain models for lab-1337.

Pydantic models for the experiment domain. These represent the core concepts:

Terminology (from Karman's ontology):
- Condition: The independent variable (was "Treatment")
- Task: A problem to solve
- Batch: A specific execution configuration (was "Scenario")
- Run: A single task + condition + attempt
- RunResult: The outcome of a Run
"""

from datetime import datetime
from enum import Enum
from typing import Any, Iterator

from pydantic import BaseModel, ConfigDict, Field, computed_field


# --- Enums ---


class ConditionType(str, Enum):
    """Type of experimental condition."""
    BASELINE = "baseline"      # Control - no special prompting
    MOTIVATION = "motivation"  # WHAT + WHY + CONSTRAINTS
    MANDATE = "mandate"        # WHAT + WHY + CONSTRAINTS + HOW


class RunStatus(str, Enum):
    """Status of a Run."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class IterationStrategy(str, Enum):
    """How the agent iterates on solutions."""
    NONE = "none"                    # Single shot
    SELF_REVIEW = "self-review"      # Agent reviews own work
    TEST_FEEDBACK = "test-feedback"  # Feed test failures back


# --- Value Objects (frozen models) ---


class IterationConfig(BaseModel):
    """Configuration for iteration behavior.

    Value object - immutable after creation.
    """
    model_config = ConfigDict(frozen=True)

    strategy: IterationStrategy = IterationStrategy.NONE
    max_iterations: int = Field(default=1, ge=1)
    review_prompt: str = "Review your solution for correctness and edge cases."


class Condition(BaseModel):
    """An experimental condition (the independent variable).

    This is what we vary between runs. For REP-002, these are
    different prompting strategies (motivation vs mandate).

    Value object - immutable after creation.
    """
    model_config = ConfigDict(frozen=True)

    name: str
    type: ConditionType
    prompt: str
    description: str = ""
    style: str | None = None  # e.g., "template", "structure", "role"

    @computed_field
    @property
    def is_mandate(self) -> bool:
        return self.type == ConditionType.MANDATE

    @computed_field
    @property
    def is_baseline(self) -> bool:
        return self.type == ConditionType.BASELINE


class Task(BaseModel):
    """A problem for the agent to solve.

    Unified model that works for SWE-bench, HumanEval, or custom tasks.

    Value object - immutable after creation.
    """
    model_config = ConfigDict(frozen=True)

    id: str
    prompt: str  # The problem statement

    # Context (varies by dataset)
    repo: str = ""
    base_commit: str = ""

    # Ground truth for evaluation
    fail_to_pass: tuple[str, ...] = ()  # Tests that should pass after fix
    pass_to_pass: tuple[str, ...] = ()  # Tests that should stay passing

    # Metadata
    difficulty: str = "medium"
    hints: str = ""


class RunIdentity(BaseModel):
    """Unique identity of a Run for deduplication and resumption.

    Value object - immutable after creation.
    """
    model_config = ConfigDict(frozen=True)

    task_id: str
    condition_name: str
    attempt: int

    def __hash__(self) -> int:
        return hash((self.task_id, self.condition_name, self.attempt))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RunIdentity):
            return NotImplemented
        return (
            self.task_id == other.task_id
            and self.condition_name == other.condition_name
            and self.attempt == other.attempt
        )


class RunResult(BaseModel):
    """The outcome of a single Run.

    Value object - immutable after creation.
    """
    model_config = ConfigDict(frozen=True)

    task_id: str
    condition_name: str
    attempt: int

    # Outcome
    passed: bool
    score: float | None = None  # For graded evaluations (0.0-1.0)

    # Diagnostics
    iterations_used: int = 0
    tokens_input: int = 0
    tokens_output: int = 0
    duration_ms: int = 0

    # Error tracking
    error: str | None = None

    # Tracing
    trace_id: str | None = None

    # Timestamp
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

    # NEW: Stored for post-hoc analysis (LLM-as-judge)
    solution: str | None = None  # Git diff or code output
    conversation_trace: list[dict] | None = None  # Full message history

    # NEW: Quality metrics (filled by LLM-as-judge post-processing)
    quality_scores: dict | None = None  # {problem_understanding: 0-3, ...}

    @computed_field
    @property
    def total_tokens(self) -> int:
        return self.tokens_input + self.tokens_output

    @computed_field
    @property
    def identity(self) -> RunIdentity:
        return RunIdentity(
            task_id=self.task_id,
            condition_name=self.condition_name,
            attempt=self.attempt,
        )


# --- Entities (mutable state) ---


class Run(BaseModel):
    """A single execution of one task under one condition.

    The atomic unit of experimentation. Has identity and lifecycle.
    """
    model_config = ConfigDict(validate_assignment=True)

    task_id: str
    condition_name: str
    attempt: int  # Which repetition (1-indexed)

    status: RunStatus = RunStatus.PENDING
    result: RunResult | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None

    @computed_field
    @property
    def identity(self) -> RunIdentity:
        """Get the unique identity of this run."""
        return RunIdentity(
            task_id=self.task_id,
            condition_name=self.condition_name,
            attempt=self.attempt,
        )

    def start(self) -> None:
        """Mark run as started."""
        self.status = RunStatus.RUNNING
        self.started_at = datetime.now()

    def complete(self, result: RunResult) -> None:
        """Mark run as completed with result."""
        self.status = RunStatus.COMPLETED
        self.result = result
        self.completed_at = datetime.now()

    def fail(self, error: str) -> None:
        """Mark run as failed."""
        self.status = RunStatus.FAILED
        self.result = RunResult(
            task_id=self.task_id,
            condition_name=self.condition_name,
            attempt=self.attempt,
            passed=False,
            error=error,
        )
        self.completed_at = datetime.now()


class Batch(BaseModel):
    """A specific execution configuration.

    Combines tasks, conditions, and run parameters into an executable unit.
    Supports streaming via generator methods.
    """
    model_config = ConfigDict(validate_assignment=True)

    name: str
    tasks: list[Task]
    conditions: list[Condition]
    runs_per_condition: int = Field(default=5, ge=1)

    # Model and iteration config
    model: str = "sonnet"
    iteration: IterationConfig = Field(default_factory=IterationConfig)

    # Metadata
    description: str = ""
    hypothesis: str = ""

    @computed_field
    @property
    def total_runs(self) -> int:
        """Total number of runs in this batch."""
        return len(self.tasks) * len(self.conditions) * self.runs_per_condition

    def generate_runs(self) -> Iterator[Run]:
        """Generate runs lazily (streaming).

        Yields one Run at a time instead of building a list.
        Memory-efficient for large experiments.
        """
        for task in self.tasks:
            for condition in self.conditions:
                for attempt in range(1, self.runs_per_condition + 1):
                    yield Run(
                        task_id=task.id,
                        condition_name=condition.name,
                        attempt=attempt,
                    )

    def get_task(self, task_id: str) -> Task | None:
        """Get task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_condition(self, name: str) -> Condition | None:
        """Get condition by name."""
        for condition in self.conditions:
            if condition.name == name:
                return condition
        return None


# --- Aggregates ---


class ConditionSummary(BaseModel):
    """Summary statistics for a single condition."""
    model_config = ConfigDict(validate_assignment=True)

    condition_name: str
    total_runs: int = 0
    passed: int = 0
    failed: int = 0

    total_tokens: int = 0
    total_iterations: int = 0
    total_duration_ms: int = 0

    @computed_field
    @property
    def pass_rate(self) -> float:
        return self.passed / self.total_runs if self.total_runs > 0 else 0.0

    @computed_field
    @property
    def avg_tokens(self) -> float:
        return self.total_tokens / self.total_runs if self.total_runs > 0 else 0.0

    @computed_field
    @property
    def avg_iterations(self) -> float:
        return self.total_iterations / self.total_runs if self.total_runs > 0 else 0.0

    @computed_field
    @property
    def avg_duration_ms(self) -> float:
        return self.total_duration_ms / self.total_runs if self.total_runs > 0 else 0.0


class BatchResults(BaseModel):
    """Aggregated results for a batch run."""
    model_config = ConfigDict(validate_assignment=True)

    batch_name: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

    # Overall stats
    total_runs: int = 0
    completed_runs: int = 0
    passed_runs: int = 0

    # Per-condition stats
    by_condition: dict[str, ConditionSummary] = Field(default_factory=dict)

    def add_result(self, result: RunResult) -> None:
        """Add a result to the summary (online aggregation)."""
        self.total_runs += 1
        self.completed_runs += 1

        if result.passed:
            self.passed_runs += 1

        # Update per-condition stats
        if result.condition_name not in self.by_condition:
            self.by_condition[result.condition_name] = ConditionSummary(
                condition_name=result.condition_name
            )

        summary = self.by_condition[result.condition_name]
        summary.total_runs += 1
        if result.passed:
            summary.passed += 1
        else:
            summary.failed += 1
        summary.total_tokens += result.total_tokens
        summary.total_iterations += result.iterations_used
        summary.total_duration_ms += result.duration_ms

    @computed_field
    @property
    def pass_rate(self) -> float:
        return self.passed_runs / self.completed_runs if self.completed_runs > 0 else 0.0
