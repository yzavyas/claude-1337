"""Tests for core models."""

import pytest

from evals_1337.core.models import (
    TestCase,
    EvalResult,
    EvalReport,
    EvalMetrics,
    Expectation,
    Outcome,
    compute_outcome,
)


class TestExpectation:
    """Test Expectation enum."""

    def test_values(self):
        assert Expectation.MUST_PASS.value == "must_pass"
        assert Expectation.MUST_FAIL.value == "must_fail"
        assert Expectation.ACCEPTABLE.value == "acceptable"


class TestOutcome:
    """Test Outcome enum."""

    def test_values(self):
        assert Outcome.TP.value == "tp"
        assert Outcome.FP.value == "fp"
        assert Outcome.TN.value == "tn"
        assert Outcome.FN.value == "fn"


class TestComputeOutcome:
    """Test outcome computation."""

    def test_must_pass_and_passed(self):
        result = compute_outcome(Expectation.MUST_PASS, passed=True)
        assert result == Outcome.TP

    def test_must_pass_and_failed(self):
        result = compute_outcome(Expectation.MUST_PASS, passed=False)
        assert result == Outcome.FN

    def test_must_fail_and_passed(self):
        result = compute_outcome(Expectation.MUST_FAIL, passed=True)
        assert result == Outcome.FP

    def test_must_fail_and_failed(self):
        result = compute_outcome(Expectation.MUST_FAIL, passed=False)
        assert result == Outcome.TN

    def test_acceptable(self):
        result = compute_outcome(Expectation.ACCEPTABLE, passed=True)
        assert result == Outcome.ACCEPTABLE

        result = compute_outcome(Expectation.ACCEPTABLE, passed=False)
        assert result == Outcome.ACCEPTABLE


class TestTestCase:
    """Test TestCase model."""

    def test_create(self):
        case = TestCase(
            prompt="Test prompt",
            expectation=Expectation.MUST_PASS,
            rationale="Test rationale",
        )
        assert case.prompt == "Test prompt"
        assert case.expectation == Expectation.MUST_PASS
        assert case.rationale == "Test rationale"

    def test_requires_prompt(self):
        with pytest.raises(Exception):
            TestCase(
                prompt="",  # Empty prompt should fail
                expectation=Expectation.MUST_PASS,
            )


class TestEvalMetrics:
    """Test EvalMetrics model."""

    def test_precision(self):
        # TP=3, FP=1 -> precision = 3/4 = 0.75
        m = EvalMetrics(tp=3, fp=1, tn=0, fn=0)
        assert m.precision == 0.75

    def test_recall(self):
        # TP=3, FN=1 -> recall = 3/4 = 0.75
        m = EvalMetrics(tp=3, fp=0, tn=0, fn=1)
        assert m.recall == 0.75

    def test_f1(self):
        # P=0.75, R=0.75 -> F1 = 0.75
        m = EvalMetrics(tp=3, fp=1, tn=0, fn=1)
        assert m.f1 == 0.75

    def test_f1_zero_division(self):
        # No positives
        m = EvalMetrics(tp=0, fp=0, tn=5, fn=0)
        assert m.f1 == 0.0

    def test_accuracy(self):
        # TP=3, TN=2, FP=1, FN=1 -> (3+2)/(3+2+1+1) = 5/7
        m = EvalMetrics(tp=3, fp=1, tn=2, fn=1)
        assert abs(m.accuracy - 5 / 7) < 0.001

    def test_total(self):
        m = EvalMetrics(tp=1, fp=2, tn=3, fn=4, acceptable=5, errors=6)
        # Total excludes acceptable and errors
        assert m.total == 10

    def test_is_passing(self):
        # F1 = 0.75 >= 0.7
        m = EvalMetrics(tp=3, fp=1, tn=0, fn=1)
        assert m.is_passing(min_f1=0.7)
        assert not m.is_passing(min_f1=0.8)


class TestEvalReport:
    """Test EvalReport model."""

    def test_metrics_aggregation(self):
        report = EvalReport(name="test", target_type="skills")

        # Add some results
        case = TestCase(prompt="test", expectation=Expectation.MUST_PASS)
        report.results.append(EvalResult(
            test_case=case, passed=True, outcome=Outcome.TP,
        ))
        report.results.append(EvalResult(
            test_case=case, passed=False, outcome=Outcome.FN,
        ))
        report.results.append(EvalResult(
            test_case=case, passed=True, outcome=Outcome.FP,
        ))

        metrics = report.metrics()
        assert metrics.tp == 1
        assert metrics.fn == 1
        assert metrics.fp == 1

    def test_summary(self):
        report = EvalReport(name="test", target_type="skills")
        summary = report.summary()

        assert summary["name"] == "test"
        assert summary["target_type"] == "skills"
        assert "metrics" in summary
        assert "confusion_matrix" in summary
