"""Grader Port - Interface for solution evaluation.

Why a Protocol?
--------------
Different experiments need different evaluation strategies:
- SWE-bench: Run test suite in Docker
- HumanEval: Execute code, check output
- Custom: LLM-as-judge, exact match, etc.

The domain doesn't care HOW solutions are graded,
just that they return a GradeResult.
"""

from typing import Protocol, Any

from pydantic import BaseModel, ConfigDict, Field, computed_field

from lab.domain.models import Task


class GradeResult(BaseModel):
    """Result of grading a solution.

    Value object - immutable after creation.
    """
    model_config = ConfigDict(frozen=True)

    passed: bool
    score: float | None = Field(default=None, ge=0.0, le=1.0)

    # Details
    message: str = ""
    error: str | None = None

    # Test details (for test-suite grading)
    tests_passed: int = Field(default=0, ge=0)
    tests_failed: int = Field(default=0, ge=0)
    tests_total: int = Field(default=0, ge=0)

    # Raw output for debugging
    details: dict[str, Any] = Field(default_factory=dict)

    @computed_field
    @property
    def is_error(self) -> bool:
        """True if grading itself failed (not just the solution)."""
        return self.error is not None


class GraderPort(Protocol):
    """Port for solution evaluation.

    The domain needs to:
    1. Submit a solution for a task
    2. Get back pass/fail with optional score

    Implementations:
    - FunctionGraderAdapter: Custom function-based grading
    - MockGraderAdapter: For testing
    """

    async def grade(
        self,
        solution: str,
        task: Task,
    ) -> GradeResult:
        """Grade a solution against a task.

        Args:
            solution: The generated solution (code, patch, etc.)
            task: The task being solved (contains expected results)

        Returns:
            GradeResult with pass/fail and optional score
        """
        ...

    async def setup(self, task: Task) -> str | None:
        """Setup environment for grading a task.

        Some graders need setup (clone repo, create container, etc.)
        Returns the working directory where Claude should execute,
        or None if no special directory is needed.
        """
        ...

    async def get_solution(self, task: Task) -> str:
        """Get the solution (git diff) after Claude has made changes.

        For SWE-bench, this captures `git diff` from the working directory.
        """
        ...

    async def teardown(self, task: Task) -> None:
        """Cleanup after grading a task.

        Optional cleanup (remove containers, temp files, etc.)
        """
        ...
