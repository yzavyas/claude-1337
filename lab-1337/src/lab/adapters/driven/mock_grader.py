"""Mock Grader Adapter - For testing without real evaluation.

A simple grader that passes or fails based on configurable patterns.
Useful for testing the experiment harness without running actual evals.
"""

import random
import re
from typing import Callable

from lab.domain.models import Task
from lab.ports.driven.grader import GraderPort, GradeResult


class MockGraderAdapter:
    """Mock grader for testing.

    Can be configured with different grading strategies:
    - always_pass: All solutions pass
    - always_fail: All solutions fail
    - random: Random pass/fail with configurable rate
    - pattern: Pass if solution matches a regex pattern
    - callback: Use a custom grading function
    """

    def __init__(
        self,
        strategy: str = "random",
        pass_rate: float = 0.5,
        pattern: str | None = None,
        callback: Callable[[str, Task], bool] | None = None,
    ):
        """Initialize the mock grader.

        Args:
            strategy: One of "always_pass", "always_fail", "random", "pattern", "callback"
            pass_rate: Probability of passing (for random strategy)
            pattern: Regex pattern to match (for pattern strategy)
            callback: Custom grading function (for callback strategy)
        """
        self.strategy = strategy
        self.pass_rate = pass_rate
        self.pattern = re.compile(pattern) if pattern else None
        self.callback = callback

    async def grade(
        self,
        solution: str,
        task: Task,
    ) -> GradeResult:
        """Grade a solution using the configured strategy."""
        if self.strategy == "always_pass":
            return GradeResult(
                passed=True,
                score=1.0,
                message="Mock grader: always_pass strategy",
            )

        elif self.strategy == "always_fail":
            return GradeResult(
                passed=False,
                score=0.0,
                message="Mock grader: always_fail strategy",
            )

        elif self.strategy == "random":
            passed = random.random() < self.pass_rate
            return GradeResult(
                passed=passed,
                score=1.0 if passed else 0.0,
                message=f"Mock grader: random strategy (rate={self.pass_rate})",
            )

        elif self.strategy == "pattern":
            if not self.pattern:
                return GradeResult(
                    passed=False,
                    error="Pattern strategy requires a pattern",
                )
            passed = bool(self.pattern.search(solution))
            return GradeResult(
                passed=passed,
                score=1.0 if passed else 0.0,
                message=f"Mock grader: pattern strategy (pattern={self.pattern.pattern})",
            )

        elif self.strategy == "callback":
            if not self.callback:
                return GradeResult(
                    passed=False,
                    error="Callback strategy requires a callback function",
                )
            try:
                passed = self.callback(solution, task)
                return GradeResult(
                    passed=passed,
                    score=1.0 if passed else 0.0,
                    message="Mock grader: callback strategy",
                )
            except Exception as e:
                return GradeResult(
                    passed=False,
                    error=f"Callback raised exception: {e}",
                )

        else:
            return GradeResult(
                passed=False,
                error=f"Unknown strategy: {self.strategy}",
            )

    async def setup(self, task: Task) -> str | None:
        """No setup needed for mock grader."""
        return None

    async def get_solution(self, task: Task) -> str:
        """Mock grader doesn't capture solutions."""
        return ""

    async def teardown(self, task: Task) -> None:
        """No teardown needed for mock grader."""
        pass
