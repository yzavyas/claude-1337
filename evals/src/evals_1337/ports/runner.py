"""ExtensionRunner port - how to invoke extensions and observe results.

This is the core abstraction. Adapters implement this for different runtimes:
- simulation: direct API calls with mock tools
- headless: claude -p with stream-json parsing
- sdk: Python/TypeScript SDK programmatic control
"""

from typing import Protocol, runtime_checkable
from abc import abstractmethod

from ..core.models import TestCase, EvalResult, EvalReport


@runtime_checkable
class ExtensionRunner(Protocol):
    """Port: How to run an extension and observe results.

    Each adapter implements this for a specific runtime (simulation, headless, sdk).
    Each extension type (skills, hooks, agents, etc.) has its own runner.
    """

    @property
    def extension_type(self) -> str:
        """Which extension type this runner handles (skills, hooks, agents, commands, mcp)."""
        ...

    @property
    def runtime(self) -> str:
        """Which runtime this uses (simulation, headless, sdk)."""
        ...

    async def run_single(self, test_case: TestCase, **kwargs) -> EvalResult:
        """Run a single test case and return result."""
        ...

    async def run_batch(self, test_cases: list[TestCase], runs: int = 1, **kwargs) -> EvalReport:
        """Run multiple test cases, optionally multiple times each."""
        ...


class RunnerRegistry:
    """Registry of available runners.

    Usage:
        registry = RunnerRegistry()
        registry.register(SkillSimulationRunner())
        registry.register(SkillHeadlessRunner())

        runner = registry.get("skills", runtime="headless")
    """

    def __init__(self):
        self._runners: dict[tuple[str, str], ExtensionRunner] = {}

    def register(self, runner: ExtensionRunner) -> None:
        """Register a runner."""
        key = (runner.extension_type, runner.runtime)
        self._runners[key] = runner

    def get(self, extension_type: str, runtime: str = "headless") -> ExtensionRunner:
        """Get a runner for extension type and runtime."""
        key = (extension_type, runtime)
        if key not in self._runners:
            available = [f"{e}:{r}" for e, r in self._runners.keys()]
            raise ValueError(
                f"No runner for {extension_type}:{runtime}. "
                f"Available: {available}"
            )
        return self._runners[key]

    def list_runners(self) -> list[tuple[str, str]]:
        """List all registered runners as (extension_type, runtime) tuples."""
        return list(self._runners.keys())

    def supports(self, extension_type: str, runtime: str = "headless") -> bool:
        """Check if a runner exists for this combination."""
        return (extension_type, runtime) in self._runners
