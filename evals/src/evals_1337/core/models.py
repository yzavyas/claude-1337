"""Core evaluation models.

These models are shared across all extension types (skills, agents, MCP, etc.).
Extension-specific models extend these in their respective modules.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Expectation(str, Enum):
    """Ground truth: should this test case trigger/pass?

    Used for classification metrics (precision/recall/F1).
    """

    MUST_PASS = "must_pass"
    """Clear positive case. Counts toward recall if missed."""

    MUST_FAIL = "must_fail"
    """Clear negative case. Counts toward precision if triggered."""

    ACCEPTABLE = "acceptable"
    """Ambiguous case. Excluded from metrics."""


class Outcome(str, Enum):
    """Classification outcome based on expectation vs actual."""

    TP = "tp"
    """True positive: expected pass, actually passed."""

    FP = "fp"
    """False positive: expected fail, actually passed (noise)."""

    TN = "tn"
    """True negative: expected fail, actually failed (correct rejection)."""

    FN = "fn"
    """False negative: expected pass, actually failed (miss)."""

    ACCEPTABLE = "acceptable"
    """Ambiguous case, excluded from metrics."""

    ERROR = "error"
    """Execution error, excluded from metrics."""


def compute_outcome(expectation: Expectation, passed: bool) -> Outcome:
    """Determine outcome from expectation and actual result."""
    if expectation == Expectation.ACCEPTABLE:
        return Outcome.ACCEPTABLE

    if expectation == Expectation.MUST_PASS:
        return Outcome.TP if passed else Outcome.FN

    # MUST_FAIL
    return Outcome.FP if passed else Outcome.TN


class TestCase(BaseModel):
    """A single test case with ground truth expectation.

    Extension-specific test cases add fields (e.g., skill name, tool call).
    """

    prompt: str = Field(min_length=1)
    """The input to evaluate."""

    expectation: Expectation
    """Ground truth: what should happen?"""

    rationale: str = ""
    """Why this expectation is correct. Documents the test case."""


class EvalMetrics(BaseModel):
    """Classification metrics: precision, recall, F1.

    These metrics apply to any binary classification:
    - Skill activation (did it trigger?)
    - Task completion (did it succeed?)
    - Tool call accuracy (correct tool?)
    """

    tp: int = Field(default=0, ge=0)
    fp: int = Field(default=0, ge=0)
    tn: int = Field(default=0, ge=0)
    fn: int = Field(default=0, ge=0)
    acceptable: int = Field(default=0, ge=0)
    errors: int = Field(default=0, ge=0)

    @property
    def total(self) -> int:
        """Total classified cases (excludes acceptable/errors)."""
        return self.tp + self.fp + self.tn + self.fn

    @property
    def precision(self) -> float:
        """When it passes/triggers, is it correct?"""
        denom = self.tp + self.fp
        return self.tp / denom if denom > 0 else 0.0

    @property
    def recall(self) -> float:
        """When it should pass/trigger, does it?"""
        denom = self.tp + self.fn
        return self.tp / denom if denom > 0 else 0.0

    @property
    def f1(self) -> float:
        """Harmonic mean of precision and recall."""
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if (p + r) > 0 else 0.0

    @property
    def accuracy(self) -> float:
        """Overall accuracy: (TP + TN) / total."""
        return (self.tp + self.tn) / self.total if self.total > 0 else 0.0

    def is_passing(self, min_f1: float = 0.7) -> bool:
        """Check if metrics meet threshold."""
        return self.f1 >= min_f1


class EvalResult(BaseModel):
    """Result of a single test case evaluation."""

    test_case: TestCase
    """The test case that was run."""

    passed: bool
    """Did the test pass? (interpretation depends on eval type)"""

    outcome: Outcome
    """Classification outcome based on expectation."""

    duration_ms: int = 0
    """Execution time in milliseconds."""

    details: dict[str, Any] = Field(default_factory=dict)
    """Extension-specific details (e.g., skills activated, tools called)."""

    error: str | None = None
    """Error message if execution failed."""

    timestamp: datetime = Field(default_factory=datetime.now)


class EvalReport(BaseModel):
    """Complete evaluation report."""

    name: str
    """Report name (e.g., skill name, suite name)."""

    target_type: str
    """Extension type: skills, agents, mcp, commands, hooks."""

    results: list[EvalResult] = Field(default_factory=list)
    """Individual test results."""

    config: dict[str, Any] = Field(default_factory=dict)
    """Evaluation configuration (mode, runs, etc.)."""

    timestamp: datetime = Field(default_factory=datetime.now)

    def metrics(self) -> EvalMetrics:
        """Compute aggregate metrics from results."""
        m = EvalMetrics()
        for r in self.results:
            match r.outcome:
                case Outcome.TP:
                    m.tp += 1
                case Outcome.FP:
                    m.fp += 1
                case Outcome.TN:
                    m.tn += 1
                case Outcome.FN:
                    m.fn += 1
                case Outcome.ACCEPTABLE:
                    m.acceptable += 1
                case Outcome.ERROR:
                    m.errors += 1
        return m

    def summary(self) -> dict[str, Any]:
        """Summary suitable for JSON serialization."""
        m = self.metrics()
        return {
            "name": self.name,
            "target_type": self.target_type,
            "timestamp": self.timestamp.isoformat(),
            "total_results": len(self.results),
            "metrics": {
                "precision": round(m.precision, 3),
                "recall": round(m.recall, 3),
                "f1": round(m.f1, 3),
                "accuracy": round(m.accuracy, 3),
            },
            "confusion_matrix": {
                "tp": m.tp,
                "fp": m.fp,
                "tn": m.tn,
                "fn": m.fn,
            },
            "excluded": {
                "acceptable": m.acceptable,
                "errors": m.errors,
            },
        }
