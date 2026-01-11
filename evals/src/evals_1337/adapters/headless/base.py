"""Base headless runner - shared logic for all extension types.

Runs Claude Code with -p flag and parses stream-json output.

Security note: This uses subprocess to run `claude` CLI. Inputs are not
user-provided - they come from test case definitions in the codebase.
"""

import asyncio
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from ...core.models import TestCase, EvalResult, EvalReport, Outcome
from .observer import HeadlessObserver, Observation


class HeadlessRunnerBase(ABC):
    """Base class for headless runners.

    Subclasses implement extension-specific logic:
    - How to construct the prompt/command
    - How to interpret observations
    - What counts as "passed"
    """

    def __init__(
        self,
        working_dir: Path | None = None,
        timeout: int = 60,
    ):
        self.working_dir = working_dir or Path.cwd()
        self.timeout = timeout
        self.observer = HeadlessObserver()

    @property
    @abstractmethod
    def extension_type(self) -> str:
        """Which extension type this runner handles."""
        ...

    @property
    def runtime(self) -> str:
        return "headless"

    @abstractmethod
    def build_command(self, test_case: TestCase, **kwargs) -> list[str]:
        """Build the claude command for this test case."""
        ...

    @abstractmethod
    def interpret_observations(
        self,
        observations: list[Observation],
        test_case: TestCase,
        **kwargs,
    ) -> tuple[bool, dict[str, Any]]:
        """Interpret observations to determine pass/fail and details."""
        ...

    async def run_claude(self, command: list[str]) -> tuple[str, int, int]:
        """Run claude command and capture output.

        Returns: (output, exit_code, duration_ms)

        Note: Uses asyncio.create_subprocess_exec with explicit argument list
        to avoid shell injection. Command args come from test definitions,
        not user input.
        """
        start = time.monotonic()

        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.working_dir,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.timeout,
            )
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            raise TimeoutError(f"Command timed out after {self.timeout}s")

        duration_ms = int((time.monotonic() - start) * 1000)
        output = stdout.decode("utf-8")

        return output, process.returncode or 0, duration_ms

    async def run_single(self, test_case: TestCase, **kwargs) -> EvalResult:
        """Run a single test case."""
        try:
            command = self.build_command(test_case, **kwargs)
            output, exit_code, duration_ms = await self.run_claude(command)

            # Get observations based on extension type
            observe_method = getattr(
                self.observer,
                f"observe_{self.extension_type}",
                None,
            )
            if observe_method:
                observations = observe_method(output)
            else:
                observations = []

            passed, details = self.interpret_observations(
                observations, test_case, **kwargs
            )
            details["exit_code"] = exit_code
            details["runtime"] = self.runtime

            from ...core.models import compute_outcome
            outcome = compute_outcome(test_case.expectation, passed)

            return EvalResult(
                test_case=test_case,
                passed=passed,
                outcome=outcome,
                duration_ms=duration_ms,
                details=details,
            )

        except Exception as e:
            return EvalResult(
                test_case=test_case,
                passed=False,
                outcome=Outcome.ERROR,
                error=str(e),
            )

    async def run_batch(
        self,
        test_cases: list[TestCase],
        runs: int = 1,
        **kwargs,
    ) -> EvalReport:
        """Run multiple test cases."""
        report = EvalReport(
            name=kwargs.get("name", self.extension_type),
            target_type=self.extension_type,
            config={
                "runs": runs,
                "runtime": self.runtime,
                "working_dir": str(self.working_dir),
                **kwargs,
            },
        )

        for test_case in test_cases:
            for _ in range(runs):
                result = await self.run_single(test_case, **kwargs)
                report.results.append(result)
                await asyncio.sleep(0.5)  # Rate limiting

        return report
