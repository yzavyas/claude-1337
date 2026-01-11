"""Universal plugin test harness.

Tests any Claude Code plugin type following eval-1337 best practices:
- Code-based graders first (deterministic)
- Labeled expectations (must_trigger, should_not_trigger, acceptable)
- Multiple runs (5+) for stochastic handling
- F1 metrics (precision + recall)
- Clean isolation between runs
"""

import asyncio
import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from ..adapters import create_default_registry
from ..core.models import TestCase, EvalReport, EvalMetrics, Expectation
from ..plugins import validate_plugin, ValidationResult


class PluginType(str, Enum):
    """Types of Claude Code plugin components."""

    SKILL = "skill"
    HOOK = "hook"
    AGENT = "agent"
    COMMAND = "command"
    MCP = "mcp"


@dataclass
class PluginTestResult:
    """Result of testing a single plugin."""

    plugin_name: str
    plugin_type: PluginType
    validation: ValidationResult
    eval_report: EvalReport | None = None
    pass_at_k: float | None = None  # Probability of at least 1 success in k trials
    pass_hat_k: float | None = None  # Probability of all k trials succeeding

    @property
    def passed(self) -> bool:
        """Did the plugin pass all checks?"""
        if not self.validation.valid:
            return False
        if self.eval_report:
            metrics = self.eval_report.metrics()
            return metrics.f1 >= 0.7  # Threshold from eval-1337
        return True


def discover_plugin_type(plugin_path: Path) -> list[PluginType]:
    """Discover what types of components a plugin has.

    Returns list of PluginTypes based on what files exist.
    """
    types = []

    # Check for SKILL.md
    if (plugin_path / "SKILL.md").exists():
        types.append(PluginType.SKILL)

    # Check for hooks/
    hooks_dir = plugin_path / "hooks"
    if hooks_dir.exists() and (hooks_dir / "hooks.json").exists():
        types.append(PluginType.HOOK)

    # Check for agents/
    agents_dir = plugin_path / "agents"
    if agents_dir.exists() and any(agents_dir.glob("*.md")):
        types.append(PluginType.AGENT)

    # Check for commands/
    commands_dir = plugin_path / "commands"
    if commands_dir.exists() and any(commands_dir.glob("*.md")):
        types.append(PluginType.COMMAND)

    # Check for .mcp.json
    if (plugin_path / ".mcp.json").exists():
        types.append(PluginType.MCP)

    return types


def load_test_cases(plugin_path: Path, plugin_type: PluginType) -> list[TestCase]:
    """Load test cases from plugin's tests/ directory.

    Looks for:
    - tests/skill.json for skills
    - tests/hooks.json for hooks
    - tests/agents.json for agents
    - etc.

    Falls back to default test cases if not found.
    """
    tests_dir = plugin_path / "tests"
    test_file = tests_dir / f"{plugin_type.value}.json"

    if test_file.exists():
        with open(test_file) as f:
            data = json.load(f)

        cases = []
        for item in data.get("test_cases", []):
            exp_str = item.get("expectation", "must_pass")
            if exp_str in ("must_trigger", "must_pass"):
                expectation = Expectation.MUST_PASS
            elif exp_str in ("should_not_trigger", "must_fail"):
                expectation = Expectation.MUST_FAIL
            else:
                expectation = Expectation.ACCEPTABLE

            cases.append(TestCase(
                prompt=item["prompt"],
                expectation=expectation,
                rationale=item.get("rationale", ""),
            ))
        return cases

    # Default test cases based on type
    return _default_test_cases(plugin_path, plugin_type)


def _default_test_cases(plugin_path: Path, plugin_type: PluginType) -> list[TestCase]:
    """Generate default test cases for a plugin."""
    plugin_name = plugin_path.name.replace("-1337", "")

    if plugin_type == PluginType.SKILL:
        return [
            TestCase(
                prompt=f"Help me with {plugin_name} tasks",
                expectation=Expectation.MUST_PASS,
                rationale="Direct domain reference should trigger",
            ),
            TestCase(
                prompt="Write me a haiku about programming",
                expectation=Expectation.MUST_FAIL,
                rationale="Creative task unrelated to skill",
            ),
        ]

    elif plugin_type == PluginType.HOOK:
        return [
            TestCase(
                prompt="Start a new session",
                expectation=Expectation.ACCEPTABLE,
                rationale="SessionStart hook may or may not fire visibly",
            ),
        ]

    elif plugin_type == PluginType.AGENT:
        return [
            TestCase(
                prompt=f"Use the {plugin_name} agent to help me",
                expectation=Expectation.MUST_PASS,
                rationale="Direct agent reference",
            ),
        ]

    elif plugin_type == PluginType.COMMAND:
        return [
            TestCase(
                prompt=f"Run /{plugin_name}",
                expectation=Expectation.MUST_PASS,
                rationale="Direct command invocation",
            ),
        ]

    elif plugin_type == PluginType.MCP:
        return [
            TestCase(
                prompt=f"Use the {plugin_name} MCP server",
                expectation=Expectation.ACCEPTABLE,
                rationale="MCP server usage depends on task",
            ),
        ]

    return []


def compute_pass_at_k(successes: int, total: int, k: int = 3) -> float:
    """Compute pass@k: probability of at least 1 success in k trials.

    Formula: 1 - C(n-c, k) / C(n, k)
    where n = total, c = successes
    """
    if total < k or successes == 0:
        return 0.0
    if successes >= total:
        return 1.0

    # Compute probability of k failures
    n = total
    c = successes
    prob_all_fail = 1.0
    for i in range(k):
        prob_all_fail *= (n - c - i) / (n - i)

    return 1.0 - prob_all_fail


def compute_pass_hat_k(successes: int, total: int, k: int = 3) -> float:
    """Compute pass^k: probability of all k trials succeeding.

    Simple: (successes/total)^k
    """
    if total == 0:
        return 0.0
    return (successes / total) ** k


class PluginHarness:
    """Universal harness for testing Claude Code plugins.

    Usage:
        harness = PluginHarness(plugins_dir)
        result = await harness.test_plugin("rust-1337")
        print(result.passed, result.eval_report.metrics())
    """

    def __init__(
        self,
        plugins_dir: Path,
        runtime: str = "simulation",
        runs: int = 5,
        mode: str = "baseline",
    ):
        self.plugins_dir = Path(plugins_dir)
        self.runtime = runtime
        self.runs = runs
        self.mode = mode
        self.registry = create_default_registry()

    async def test_plugin(
        self,
        plugin_name: str,
        plugin_types: list[PluginType] | None = None,
    ) -> PluginTestResult:
        """Test a plugin.

        Args:
            plugin_name: Name of the plugin directory
            plugin_types: Types to test (auto-discovers if None)

        Returns:
            PluginTestResult with validation and eval results
        """
        plugin_path = self.plugins_dir / plugin_name

        if not plugin_path.exists():
            # Try with -1337 suffix
            plugin_path = self.plugins_dir / f"{plugin_name}-1337"

        if not plugin_path.exists():
            return PluginTestResult(
                plugin_name=plugin_name,
                plugin_type=PluginType.SKILL,
                validation=ValidationResult(plugin_name, False, ["Plugin not found"]),
            )

        # Validate first (fast, deterministic)
        validation = validate_plugin(plugin_path)

        # Discover types
        types = plugin_types or discover_plugin_type(plugin_path)
        if not types:
            return PluginTestResult(
                plugin_name=plugin_name,
                plugin_type=PluginType.SKILL,
                validation=validation,
            )

        # Test primary type (usually skill)
        primary_type = types[0]
        test_cases = load_test_cases(plugin_path, primary_type)

        if not test_cases:
            return PluginTestResult(
                plugin_name=plugin_name,
                plugin_type=primary_type,
                validation=validation,
            )

        # Get runner for this type
        ext_type_map = {
            PluginType.SKILL: "skills",
            PluginType.HOOK: "hooks",
            PluginType.AGENT: "agents",
            PluginType.COMMAND: "commands",
            PluginType.MCP: "mcp",
        }
        ext_type = ext_type_map[primary_type]

        if not self.registry.supports(ext_type, self.runtime):
            return PluginTestResult(
                plugin_name=plugin_name,
                plugin_type=primary_type,
                validation=validation,
            )

        runner = self.registry.get(ext_type, self.runtime)

        # Load skill info for context
        skill_info = self._load_skill_info(plugin_path)
        all_skills = self._discover_all_skills()

        # Run tests
        report = await runner.run_batch(
            test_cases=test_cases,
            runs=self.runs,
            target_skill=skill_info.get("name") if skill_info else plugin_name,
            available_skills=all_skills,
            mode=self.mode,
        )

        # Compute pass@k metrics
        metrics = report.metrics()
        successes = metrics.tp + metrics.tn
        total = metrics.total
        pass_at_k = compute_pass_at_k(successes, total, k=3)
        pass_hat_k = compute_pass_hat_k(successes, total, k=3)

        return PluginTestResult(
            plugin_name=plugin_name,
            plugin_type=primary_type,
            validation=validation,
            eval_report=report,
            pass_at_k=pass_at_k,
            pass_hat_k=pass_hat_k,
        )

    async def test_all_plugins(self) -> list[PluginTestResult]:
        """Test all plugins in the directory."""
        results = []
        for plugin_dir in sorted(self.plugins_dir.iterdir()):
            if plugin_dir.is_dir() and not plugin_dir.name.startswith("."):
                result = await self.test_plugin(plugin_dir.name)
                results.append(result)
        return results

    def _load_skill_info(self, plugin_path: Path) -> dict[str, str] | None:
        """Load skill name and description from SKILL.md."""
        skill_file = plugin_path / "SKILL.md"
        if not skill_file.exists():
            return None

        content = skill_file.read_text()
        if not content.startswith("---"):
            return None

        parts = content.split("---", 2)
        if len(parts) < 3:
            return None

        frontmatter = parts[1]
        name = None
        description = None

        for line in frontmatter.strip().split("\n"):
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("description:"):
                description = line.split(":", 1)[1].strip().strip('"')

        if name and description:
            return {"name": name, "description": description}
        return None

    def _discover_all_skills(self) -> list[dict[str, str]]:
        """Discover all skills for context."""
        skills = []
        for plugin_dir in self.plugins_dir.iterdir():
            if plugin_dir.is_dir():
                info = self._load_skill_info(plugin_dir)
                if info:
                    skills.append(info)
        return skills


async def run_plugin_tests(
    plugins_dir: Path,
    plugin_name: str | None = None,
    runtime: str = "simulation",
    runs: int = 5,
    mode: str = "baseline",
) -> list[PluginTestResult]:
    """Convenience function to run plugin tests.

    Args:
        plugins_dir: Directory containing plugins
        plugin_name: Specific plugin to test (all if None)
        runtime: "simulation" or "headless"
        runs: Number of runs per test case
        mode: "baseline", "smart", or "forced"

    Returns:
        List of PluginTestResult
    """
    harness = PluginHarness(
        plugins_dir=plugins_dir,
        runtime=runtime,
        runs=runs,
        mode=mode,
    )

    if plugin_name:
        result = await harness.test_plugin(plugin_name)
        return [result]
    else:
        return await harness.test_all_plugins()
