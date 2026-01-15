"""Base experiment infrastructure."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class ExperimentConfig:
    """Configuration for an experiment run."""

    name: str
    description: str = ""
    runs_per_condition: int = 5
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 8192
    conditions: dict[str, dict[str, Any]] = field(default_factory=dict)
    output_dir: Path | None = None

    def __post_init__(self):
        if self.output_dir is None:
            self.output_dir = Path("results")


@dataclass
class ConditionResult:
    """Result from a single condition run."""

    condition: str
    run_index: int
    success: bool
    metrics: dict[str, Any]
    tokens_used: int = 0
    duration_ms: int = 0
    error: str | None = None
    raw_output: str | None = None


@dataclass
class ExperimentResult:
    """Aggregated results from an experiment."""

    config: ExperimentConfig
    started_at: datetime
    completed_at: datetime | None = None
    condition_results: list[ConditionResult] = field(default_factory=list)

    def add_result(self, result: ConditionResult):
        self.condition_results.append(result)

    def summary(self) -> dict[str, Any]:
        """Generate summary statistics per condition."""
        by_condition: dict[str, list[ConditionResult]] = {}
        for r in self.condition_results:
            by_condition.setdefault(r.condition, []).append(r)

        summary = {}
        for condition, results in by_condition.items():
            successes = sum(1 for r in results if r.success)
            total = len(results)
            summary[condition] = {
                "success_rate": successes / total if total > 0 else 0,
                "runs": total,
                "successes": successes,
                "avg_tokens": sum(r.tokens_used for r in results) / total if total > 0 else 0,
                "avg_duration_ms": sum(r.duration_ms for r in results) / total if total > 0 else 0,
            }

        return summary

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict for JSON output."""
        return {
            "config": {
                "name": self.config.name,
                "description": self.config.description,
                "runs_per_condition": self.config.runs_per_condition,
                "model": self.config.model,
                "conditions": list(self.config.conditions.keys()),
            },
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "summary": self.summary(),
            "results": [
                {
                    "condition": r.condition,
                    "run": r.run_index,
                    "success": r.success,
                    "metrics": r.metrics,
                    "tokens_used": r.tokens_used,
                    "duration_ms": r.duration_ms,
                    "error": r.error,
                }
                for r in self.condition_results
            ],
        }


class Experiment(ABC):
    """Base class for experiments."""

    def __init__(self, config: ExperimentConfig):
        self.config = config

    @abstractmethod
    async def run_condition(
        self, condition: str, condition_config: dict[str, Any], run_index: int
    ) -> ConditionResult:
        """Run a single condition. Implement in subclass."""
        pass

    @abstractmethod
    def evaluate(self, output: str, condition: str) -> dict[str, Any]:
        """Evaluate output and return metrics. Implement in subclass."""
        pass
