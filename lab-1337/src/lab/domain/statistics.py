"""Online statistics for streaming experiments.

Uses Welford's algorithm for running mean/variance calculations.
Memory-efficient: O(1) regardless of number of samples.
"""

from collections import defaultdict
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, computed_field

from .models import RunResult


class OnlineStatistics(BaseModel):
    """Welford's algorithm for running mean/variance.

    Computes statistics incrementally without storing all values.
    Numerically stable for large datasets.

    Example:
        stats = OnlineStatistics()
        for result in results:
            stats.update(result)
        print(f"Pass rate: {stats.pass_rate:.1%}")
    """
    model_config = ConfigDict(validate_assignment=True)

    n: int = 0
    mean_tokens: float = 0.0
    M2_tokens: float = 0.0  # Sum of squares of differences (for variance)

    passed: int = 0
    failed: int = 0

    total_tokens: int = 0
    total_iterations: int = 0
    total_duration_ms: int = 0

    def update(self, result: RunResult) -> None:
        """Update statistics with one result.

        Uses Welford's online algorithm for numerically stable variance.
        """
        self.n += 1

        # Pass/fail counting
        if result.passed:
            self.passed += 1
        else:
            self.failed += 1

        # Running totals
        tokens = result.total_tokens
        self.total_tokens += tokens
        self.total_iterations += result.iterations_used
        self.total_duration_ms += result.duration_ms

        # Welford's online algorithm for mean and variance
        delta = tokens - self.mean_tokens
        self.mean_tokens += delta / self.n
        delta2 = tokens - self.mean_tokens
        self.M2_tokens += delta * delta2

    @computed_field
    @property
    def pass_rate(self) -> float:
        """Proportion of runs that passed."""
        return self.passed / self.n if self.n > 0 else 0.0

    @computed_field
    @property
    def fail_rate(self) -> float:
        """Proportion of runs that failed."""
        return self.failed / self.n if self.n > 0 else 0.0

    @computed_field
    @property
    def avg_tokens(self) -> float:
        """Mean tokens per run."""
        return self.mean_tokens

    @computed_field
    @property
    def var_tokens(self) -> float:
        """Sample variance of tokens (Bessel's correction)."""
        if self.n < 2:
            return 0.0
        return self.M2_tokens / (self.n - 1)

    @computed_field
    @property
    def std_tokens(self) -> float:
        """Sample standard deviation of tokens."""
        return self.var_tokens ** 0.5

    @computed_field
    @property
    def avg_iterations(self) -> float:
        """Mean iterations per run."""
        return self.total_iterations / self.n if self.n > 0 else 0.0

    @computed_field
    @property
    def avg_duration_ms(self) -> float:
        """Mean duration per run in milliseconds."""
        return self.total_duration_ms / self.n if self.n > 0 else 0.0

    def merge(self, other: "OnlineStatistics") -> "OnlineStatistics":
        """Merge two OnlineStatistics (parallel computation).

        Uses Chan's parallel algorithm for combining running statistics.
        """
        if self.n == 0:
            return other.model_copy()
        if other.n == 0:
            return self.model_copy()

        combined = OnlineStatistics()
        combined.n = self.n + other.n
        combined.passed = self.passed + other.passed
        combined.failed = self.failed + other.failed
        combined.total_tokens = self.total_tokens + other.total_tokens
        combined.total_iterations = self.total_iterations + other.total_iterations
        combined.total_duration_ms = self.total_duration_ms + other.total_duration_ms

        # Chan's parallel algorithm for mean and variance
        delta = other.mean_tokens - self.mean_tokens
        combined.mean_tokens = (
            self.mean_tokens + delta * other.n / combined.n
        )
        combined.M2_tokens = (
            self.M2_tokens + other.M2_tokens +
            delta * delta * self.n * other.n / combined.n
        )

        return combined


class PerConditionStatistics(BaseModel):
    """Track statistics per condition.

    Maintains separate OnlineStatistics for each condition name,
    plus an overall aggregate.
    """
    model_config = ConfigDict(validate_assignment=True)

    by_condition: dict[str, OnlineStatistics] = Field(default_factory=dict)
    overall: OnlineStatistics = Field(default_factory=OnlineStatistics)

    def update(self, result: RunResult) -> None:
        """Update statistics for a result."""
        if result.condition_name not in self.by_condition:
            self.by_condition[result.condition_name] = OnlineStatistics()
        self.by_condition[result.condition_name].update(result)
        self.overall.update(result)

    def get_condition(self, name: str) -> OnlineStatistics:
        """Get statistics for a specific condition."""
        if name not in self.by_condition:
            return OnlineStatistics()
        return self.by_condition[name]


class TaskStatistics(BaseModel):
    """Track statistics per task.

    Useful for identifying which tasks are harder or easier.
    """
    model_config = ConfigDict(validate_assignment=True)

    by_task: dict[str, OnlineStatistics] = Field(default_factory=dict)

    def update(self, result: RunResult) -> None:
        """Update statistics for a result."""
        if result.task_id not in self.by_task:
            self.by_task[result.task_id] = OnlineStatistics()
        self.by_task[result.task_id].update(result)

    def get_task(self, task_id: str) -> OnlineStatistics:
        """Get statistics for a specific task."""
        if task_id not in self.by_task:
            return OnlineStatistics()
        return self.by_task[task_id]

    def hardest_tasks(self, n: int = 5) -> list[tuple[str, float]]:
        """Get the n tasks with lowest pass rates."""
        tasks = [
            (task_id, stats.pass_rate)
            for task_id, stats in self.by_task.items()
            if stats.n > 0
        ]
        return sorted(tasks, key=lambda x: x[1])[:n]

    def easiest_tasks(self, n: int = 5) -> list[tuple[str, float]]:
        """Get the n tasks with highest pass rates."""
        tasks = [
            (task_id, stats.pass_rate)
            for task_id, stats in self.by_task.items()
            if stats.n > 0
        ]
        return sorted(tasks, key=lambda x: x[1], reverse=True)[:n]
