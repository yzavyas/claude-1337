"""Tests for hex architecture ports."""

import pytest

from evals_1337.ports import ExtensionRunner, RunnerRegistry
from evals_1337.ports.observer import Observation
from evals_1337.core.models import TestCase, EvalResult, EvalReport, Expectation, Outcome


class MockRunner:
    """Mock runner for testing the registry."""

    def __init__(self, ext_type: str, runtime: str):
        self._extension_type = ext_type
        self._runtime = runtime

    @property
    def extension_type(self) -> str:
        return self._extension_type

    @property
    def runtime(self) -> str:
        return self._runtime

    async def run_single(self, test_case: TestCase, **kwargs) -> EvalResult:
        return EvalResult(
            test_case=test_case,
            passed=True,
            outcome=Outcome.TP,
            duration_ms=100,
        )

    async def run_batch(self, test_cases: list[TestCase], runs: int = 1, **kwargs) -> EvalReport:
        return EvalReport(name="mock", target_type=self.extension_type)


class TestRunnerRegistry:
    """Test the RunnerRegistry."""

    def test_register_and_get(self):
        registry = RunnerRegistry()
        runner = MockRunner("skills", "simulation")

        registry.register(runner)
        retrieved = registry.get("skills", "simulation")

        assert retrieved is runner

    def test_get_default_runtime(self):
        registry = RunnerRegistry()
        registry.register(MockRunner("skills", "headless"))

        # Default runtime is headless
        retrieved = registry.get("skills")
        assert retrieved.runtime == "headless"

    def test_get_nonexistent_raises(self):
        registry = RunnerRegistry()

        with pytest.raises(ValueError) as exc:
            registry.get("skills", "nonexistent")

        assert "No runner for skills:nonexistent" in str(exc.value)

    def test_list_runners(self):
        registry = RunnerRegistry()
        registry.register(MockRunner("skills", "simulation"))
        registry.register(MockRunner("skills", "headless"))
        registry.register(MockRunner("agents", "headless"))

        runners = registry.list_runners()

        assert ("skills", "simulation") in runners
        assert ("skills", "headless") in runners
        assert ("agents", "headless") in runners
        assert len(runners) == 3

    def test_supports(self):
        registry = RunnerRegistry()
        registry.register(MockRunner("skills", "simulation"))

        assert registry.supports("skills", "simulation")
        assert not registry.supports("skills", "headless")
        assert not registry.supports("agents", "simulation")


class TestObservation:
    """Test the Observation dataclass."""

    def test_create_observation(self):
        obs = Observation(
            extension_type="skills",
            extension_name="rust-1337",
            triggered=True,
            success=None,
            duration_ms=150,
            details={"mode": "baseline"},
            raw_output='{"type": "tool_use", "name": "Skill"}',
        )

        assert obs.extension_type == "skills"
        assert obs.extension_name == "rust-1337"
        assert obs.triggered is True
        assert obs.success is None
        assert obs.duration_ms == 150

    def test_observation_with_minimal_fields(self):
        """Observation with only required fields."""
        obs = Observation(
            extension_type="hooks",
            extension_name=None,
            triggered=True,
            success=None,
            duration_ms=0,
            details={},
        )

        assert obs.extension_name is None
        assert obs.success is None
        assert obs.duration_ms == 0
        assert obs.details == {}
        assert obs.raw_output is None  # This one has a default


class TestProtocolCompliance:
    """Test that mock runner satisfies the protocol."""

    def test_mock_runner_is_extension_runner(self):
        runner = MockRunner("skills", "simulation")

        # Protocol checking via isinstance
        assert isinstance(runner, ExtensionRunner)
