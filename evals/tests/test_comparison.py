"""Tests for configuration-driven baseline comparison."""

from pathlib import Path

import pytest

from evals_1337.ports.runtime import EvalConfig, RuntimeResult
from evals_1337.adapters.anthropic_api import MockAdapter
from evals_1337.core.comparison import (
    ComparisonTestCase,
    ComparisonRunner,
    ConfigResult,
    ComparisonReport,
)
from evals_1337.core.models import Expectation, Outcome


class TestEvalConfig:
    """Test EvalConfig system prompt composition."""

    def test_empty_config(self):
        """Empty config produces empty system prompt."""
        config = EvalConfig()
        assert config.build_system_prompt() == ""

    def test_base_system_prompt_only(self):
        """Just base system prompt."""
        config = EvalConfig(system_prompt="You are a helpful assistant.")
        assert config.build_system_prompt() == "You are a helpful assistant."

    def test_with_available_skills(self):
        """Available skills produce XML block."""
        config = EvalConfig(
            available_skills=[
                {"name": "rust-1337", "description": "Rust expertise"},
                {"name": "core-1337", "description": "Core methodology"},
            ]
        )
        prompt = config.build_system_prompt()
        assert "<available_skills>" in prompt
        assert "<name>rust-1337</name>" in prompt
        assert "<description>Rust expertise</description>" in prompt

    def test_with_claude_md(self, tmp_path: Path):
        """CLAUDE.md content is loaded."""
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text("# Project\n\nThis is the project context.")

        config = EvalConfig(claude_md_path=claude_md)
        prompt = config.build_system_prompt()

        assert "# Project Context" in prompt
        assert "This is the project context." in prompt

    def test_with_skill_paths(self, tmp_path: Path):
        """Skill files are loaded."""
        skill = tmp_path / "test-skill.md"
        skill.write_text("# Test Skill\n\nSkill content here.")

        config = EvalConfig(skill_paths=[skill])
        prompt = config.build_system_prompt()

        assert "# Skill: test-skill" in prompt
        assert "Skill content here." in prompt

    def test_full_layered_config(self, tmp_path: Path):
        """Full config with all layers."""
        claude_md = tmp_path / "CLAUDE.md"
        claude_md.write_text("Project context.")

        skill = tmp_path / "my-skill.md"
        skill.write_text("Skill content.")

        ref = tmp_path / "reference.md"
        ref.write_text("Reference content.")

        config = EvalConfig(
            system_prompt="Base prompt.",
            claude_md_path=claude_md,
            skill_paths=[skill],
            reference_paths=[ref],
            available_skills=[{"name": "test", "description": "test skill"}],
        )

        prompt = config.build_system_prompt()

        # All layers present, separated by ---
        assert "Base prompt." in prompt
        assert "Project context." in prompt
        assert "Skill content." in prompt
        assert "Reference content." in prompt
        assert "<available_skills>" in prompt
        assert prompt.count("---") >= 4  # Separators between layers


class TestMockAdapter:
    """Test the mock adapter for unit testing."""

    @pytest.mark.asyncio
    async def test_returns_canned_response(self):
        """Mock returns configured responses."""
        responses = [
            RuntimeResult(response="First", skills_activated=["skill-a"]),
            RuntimeResult(response="Second", skills_activated=["skill-b"]),
        ]
        adapter = MockAdapter(responses=responses)

        config = EvalConfig()
        r1 = await adapter.run("prompt 1", config)
        r2 = await adapter.run("prompt 2", config)
        r3 = await adapter.run("prompt 3", config)  # Cycles back

        assert r1.response == "First"
        assert r2.response == "Second"
        assert r3.response == "First"  # Cycled

    @pytest.mark.asyncio
    async def test_records_calls(self):
        """Mock records all calls for assertions."""
        adapter = MockAdapter()
        config = EvalConfig(system_prompt="test")

        await adapter.run("prompt 1", config)
        await adapter.run("prompt 2", config)

        assert len(adapter.calls) == 2
        assert adapter.calls[0][0] == "prompt 1"
        assert adapter.calls[1][0] == "prompt 2"


class TestComparisonRunner:
    """Test the comparison orchestrator."""

    @pytest.mark.asyncio
    async def test_runs_all_configs(self):
        """Runner executes test cases against all configs."""
        # Mock that activates skill for first config only
        responses = [
            RuntimeResult(response="yes", skills_activated=["target"]),  # baseline
            RuntimeResult(response="yes", skills_activated=["target"]),
            RuntimeResult(response="no", skills_activated=[]),  # with_skill
            RuntimeResult(response="no", skills_activated=[]),
        ]
        adapter = MockAdapter(responses=responses)
        runner = ComparisonRunner(adapter)

        test_cases = [
            ComparisonTestCase(
                prompt="Test prompt",
                expectation=Expectation.MUST_PASS,
                target_skill="target",
            ),
        ]

        configs = {
            "baseline": EvalConfig(),
            "with_skill": EvalConfig(system_prompt="extra context"),
        }

        report = await runner.run_comparison(
            name="test",
            test_cases=test_cases,
            configs=configs,
            runs_per_case=2,
        )

        assert len(report.config_results) == 2
        assert report.config_results[0].config_name == "baseline"
        assert report.config_results[1].config_name == "with_skill"

    @pytest.mark.asyncio
    async def test_computes_metrics(self):
        """Runner computes correct metrics."""
        # First config: all activate (TP)
        # Second config: none activate (FN)
        responses = [
            RuntimeResult(response="", skills_activated=["target"]),  # TP
            RuntimeResult(response="", skills_activated=[]),  # FN
        ]
        adapter = MockAdapter(responses=responses)
        runner = ComparisonRunner(adapter)

        test_cases = [
            ComparisonTestCase(
                prompt="Should trigger",
                expectation=Expectation.MUST_PASS,
                target_skill="target",
            ),
        ]

        configs = {
            "good": EvalConfig(),
            "bad": EvalConfig(),
        }

        report = await runner.run_comparison(
            name="test",
            test_cases=test_cases,
            configs=configs,
            runs_per_case=1,
        )

        good_metrics = report.config_results[0].metrics()
        bad_metrics = report.config_results[1].metrics()

        assert good_metrics.tp == 1
        assert good_metrics.fn == 0
        assert bad_metrics.tp == 0
        assert bad_metrics.fn == 1


class TestComparisonReport:
    """Test comparison report summary."""

    def test_summary_computes_deltas(self):
        """Summary includes delta from baseline and previous."""
        report = ComparisonReport(
            name="test",
            test_cases=[],
            runs_per_case=1,
        )

        # Manually construct results with known metrics
        from evals_1337.core.models import EvalResult, TestCase

        # Config 1: F1 = 0.5 (1 TP, 1 FN)
        cr1 = ConfigResult(config_name="baseline", config=EvalConfig())
        cr1.results = [
            EvalResult(
                test_case=TestCase(prompt="p", expectation=Expectation.MUST_PASS),
                passed=True,
                outcome=Outcome.TP,
            ),
            EvalResult(
                test_case=TestCase(prompt="p", expectation=Expectation.MUST_PASS),
                passed=False,
                outcome=Outcome.FN,
            ),
        ]

        # Config 2: F1 = 1.0 (2 TP, 0 FN)
        cr2 = ConfigResult(config_name="with_skill", config=EvalConfig())
        cr2.results = [
            EvalResult(
                test_case=TestCase(prompt="p", expectation=Expectation.MUST_PASS),
                passed=True,
                outcome=Outcome.TP,
            ),
            EvalResult(
                test_case=TestCase(prompt="p", expectation=Expectation.MUST_PASS),
                passed=True,
                outcome=Outcome.TP,
            ),
        ]

        report.config_results = [cr1, cr2]
        summary = report.summary()

        assert len(summary) == 2
        assert summary[0]["config"] == "baseline"
        assert summary[0]["delta_baseline"] is None  # First has no baseline delta

        assert summary[1]["config"] == "with_skill"
        assert summary[1]["f1"] == 1.0
        # Delta should be positive (improvement over baseline)
        assert summary[1]["delta_baseline"] > 0
