"""Pydantic models for skill activation testing.

Key concepts:
- Expectation: Ground truth label for whether a skill SHOULD activate
- Outcome: Classification result (TP/FP/TN/FN) based on expectation vs actual
- Metrics: Precision, recall, F1 computed from outcomes
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class RunStatus(str, Enum):
    """Status of a single test run."""

    ACTIVATED = "activated"  # Skill() tool was called
    NOT_ACTIVATED = "not_activated"  # No Skill() call detected
    ERROR = "error"  # Test failed


class Expectation(str, Enum):
    """Ground truth label: should this prompt trigger the skill?

    MUST_ACTIVATE: Clear match, skill should definitely fire
    SHOULD_NOT_ACTIVATE: Off-topic, skill should NOT fire
    ACCEPTABLE: Ambiguous case, either outcome is reasonable
    """

    MUST_ACTIVATE = "must_activate"
    SHOULD_NOT_ACTIVATE = "should_not_activate"
    ACCEPTABLE = "acceptable"  # Either outcome is fine


class Outcome(str, Enum):
    """Classification outcome based on expectation vs actual.

    TP: Expected activation, skill activated (correct)
    FP: Expected no activation, skill activated (noise)
    TN: Expected no activation, skill didn't activate (correct)
    FN: Expected activation, skill didn't activate (missed)
    ACCEPTABLE: Ambiguous case, not counted in precision/recall
    ERROR: Test failed, excluded from metrics
    """

    TRUE_POSITIVE = "tp"
    FALSE_POSITIVE = "fp"
    TRUE_NEGATIVE = "tn"
    FALSE_NEGATIVE = "fn"
    ACCEPTABLE = "acceptable"
    ERROR = "error"


class TestCase(BaseModel):
    """A single test case with ground truth label.

    Unlike the old model which only had "expected_triggers",
    this explicitly labels what SHOULD happen.
    """

    prompt: str = Field(description="The prompt to send to Claude")
    expectation: Expectation = Field(description="Ground truth: should skill activate?")
    rationale: str = Field(default="", description="Why this expectation is correct")


class SkillTestSpec(BaseModel):
    """Test specification for a skill with labeled test cases."""

    name: str = Field(description="Skill name as it appears in available_skills")
    plugin: str = Field(description="Plugin containing the skill")
    test_cases: list[TestCase] = Field(description="Labeled test cases")


class ActivationRun(BaseModel):
    """Result of a single activation test run."""

    skill_name: str
    prompt: str
    expectation: Expectation
    status: RunStatus
    outcome: Outcome = Outcome.ERROR
    skill_called: bool = False
    skills_activated: list[str] = Field(default_factory=list)
    tool_calls: list[str] = Field(default_factory=list)
    response_preview: str = ""
    duration_ms: int = 0
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


def compute_outcome(expectation: Expectation, activated: bool) -> Outcome:
    """Determine outcome from expectation and actual activation."""
    if expectation == Expectation.ACCEPTABLE:
        return Outcome.ACCEPTABLE

    if expectation == Expectation.MUST_ACTIVATE:
        return Outcome.TRUE_POSITIVE if activated else Outcome.FALSE_NEGATIVE

    # SHOULD_NOT_ACTIVATE
    return Outcome.FALSE_POSITIVE if activated else Outcome.TRUE_NEGATIVE


class EvalMetrics(BaseModel):
    """Precision/recall metrics for rigorous evaluation."""

    true_positives: int = 0
    false_positives: int = 0
    true_negatives: int = 0
    false_negatives: int = 0
    acceptable: int = 0
    errors: int = 0

    @property
    def total_classified(self) -> int:
        """Total runs that count toward precision/recall (excludes acceptable/errors)."""
        return self.true_positives + self.false_positives + self.true_negatives + self.false_negatives

    @property
    def precision(self) -> float:
        """When skill activates, how often is it correct?"""
        denominator = self.true_positives + self.false_positives
        return self.true_positives / denominator if denominator > 0 else 0.0

    @property
    def recall(self) -> float:
        """When skill should activate, how often does it?"""
        denominator = self.true_positives + self.false_negatives
        return self.true_positives / denominator if denominator > 0 else 0.0

    @property
    def f1_score(self) -> float:
        """Harmonic mean of precision and recall."""
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if (p + r) > 0 else 0.0

    @property
    def accuracy(self) -> float:
        """Overall accuracy (TP + TN) / total."""
        if self.total_classified == 0:
            return 0.0
        return (self.true_positives + self.true_negatives) / self.total_classified

    @property
    def activation_rate(self) -> float:
        """Raw activation rate (for comparison with old metric)."""
        activated = self.true_positives + self.false_positives
        total = self.total_classified
        return activated / total if total > 0 else 0.0


class TestSuite(BaseModel):
    """Configuration for a rigorous test suite."""

    name: str
    description: str = ""
    skills: list[SkillTestSpec]
    runs_per_case: int = Field(default=5, ge=1, le=20)
    # Negative test cases that should NOT trigger any skill
    negative_cases: list[TestCase] = Field(default_factory=list)


class ActivationReport(BaseModel):
    """Complete activation test report with rigorous metrics."""

    suite_name: str
    timestamp: datetime = Field(default_factory=datetime.now)
    runs: list[ActivationRun] = Field(default_factory=list)
    config_description: str = ""  # e.g., "baseline" or "with_forced_eval"

    @property
    def total_runs(self) -> int:
        return len(self.runs)

    def compute_metrics(self) -> EvalMetrics:
        """Compute precision/recall metrics from runs."""
        metrics = EvalMetrics()
        for run in self.runs:
            match run.outcome:
                case Outcome.TRUE_POSITIVE:
                    metrics.true_positives += 1
                case Outcome.FALSE_POSITIVE:
                    metrics.false_positives += 1
                case Outcome.TRUE_NEGATIVE:
                    metrics.true_negatives += 1
                case Outcome.FALSE_NEGATIVE:
                    metrics.false_negatives += 1
                case Outcome.ACCEPTABLE:
                    metrics.acceptable += 1
                case Outcome.ERROR:
                    metrics.errors += 1
        return metrics

    def skill_metrics(self) -> dict[str, EvalMetrics]:
        """Get metrics broken down by skill."""
        by_skill: dict[str, list[ActivationRun]] = {}
        for run in self.runs:
            if run.skill_name not in by_skill:
                by_skill[run.skill_name] = []
            by_skill[run.skill_name].append(run)

        result = {}
        for skill_name, skill_runs in by_skill.items():
            # Create a temporary report to compute metrics
            temp = ActivationReport(suite_name="", runs=skill_runs)
            result[skill_name] = temp.compute_metrics()

        return result

    # Keep old method for backwards compatibility
    @property
    def activation_rate(self) -> float:
        """Raw activation rate (legacy metric)."""
        return self.compute_metrics().activation_rate

    @property
    def activated_count(self) -> int:
        metrics = self.compute_metrics()
        return metrics.true_positives + metrics.false_positives

    def skill_stats(self) -> dict[str, dict]:
        """Legacy method for backwards compatibility."""
        skill_metrics = self.skill_metrics()
        result = {}
        for skill_name, metrics in skill_metrics.items():
            activated = metrics.true_positives + metrics.false_positives
            total = metrics.total_classified + metrics.acceptable + metrics.errors
            result[skill_name] = {
                "total": total,
                "activated": activated,
                "rate": activated / total if total > 0 else 0,
                "precision": metrics.precision,
                "recall": metrics.recall,
                "f1": metrics.f1_score,
            }
        return result


# Backwards compatibility alias
SkillReference = SkillTestSpec
