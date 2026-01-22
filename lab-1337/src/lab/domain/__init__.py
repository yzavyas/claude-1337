"""Lab-1337 Domain Layer.

Pure domain models with zero external dependencies.
Based on Karman's ontology (domain-ontology.md).

This package contains:
- models: Core entities (Condition, Task, Batch, Run, RunResult)
- services: Domain services (PromptBuilder, RunSelector)
- statistics: Online statistics (Welford's algorithm)
"""

from .models import (
    Condition,
    ConditionType,
    Task,
    Batch,
    Run,
    RunStatus,
    RunResult,
    BatchResults,
    IterationStrategy,
    IterationConfig,
)

from .services import PromptBuilder

from .statistics import OnlineStatistics, PerConditionStatistics

__all__ = [
    # Models
    "Condition",
    "ConditionType",
    "Task",
    "Batch",
    "Run",
    "RunStatus",
    "RunResult",
    "BatchResults",
    "IterationStrategy",
    "IterationConfig",
    # Services
    "PromptBuilder",
    # Statistics
    "OnlineStatistics",
    "PerConditionStatistics",
]
