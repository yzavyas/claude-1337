"""Function Grader Adapter - For function implementation tasks.

Used for tasks where Claude implements a function and we grade it
by running tests against the implementation.

Unlike SWE-bench (which needs git repos and patches), this grader:
1. Creates a temp file with a function stub
2. Claude fills in the implementation
3. We import and test the function
"""

import asyncio
import importlib.util
import tempfile
import shutil
from pathlib import Path
from typing import Callable

from lab.domain.models import Task
from lab.ports.driven.grader import GraderPort, GradeResult


class FunctionGraderAdapter:
    """Grader for function implementation tasks.

    Flow:
    1. setup() - Create temp dir with template file
    2. Claude edits the file
    3. get_solution() - Read the implementation
    4. grade() - Import and test the function
    """

    def __init__(
        self,
        timeout: int = 30,
        keep_workspace: bool = False,
    ):
        self.timeout = timeout
        self.keep_workspace = keep_workspace
        self._task_dirs: dict[str, Path] = {}
        self._graders: dict[str, Callable] = {}

    def register_grader(self, task_id: str, grader_fn: Callable[[Callable], dict]) -> None:
        """Register a grading function for a task.

        The grader function should accept the implemented function and return
        a dict with: basic, edge_cases, security scores.
        """
        self._graders[task_id] = grader_fn

    async def setup(self, task: Task) -> str | None:
        """Create temp directory with template file.

        Returns working directory for Claude.
        """
        # Create temp directory
        task_dir = Path(tempfile.mkdtemp(prefix=f"lab-fn-{task.id}-"))
        self._task_dirs[task.id] = task_dir

        # Create the template file from task.prompt
        # Task.prompt should contain the function stub
        solution_file = task_dir / "solution.py"
        solution_file.write_text(task.prompt)

        return str(task_dir)

    async def get_solution(self, task: Task) -> str:
        """Get the implementation from the solution file."""
        task_dir = self._task_dirs.get(task.id)
        if not task_dir:
            return ""

        solution_file = task_dir / "solution.py"
        if solution_file.exists():
            return solution_file.read_text()
        return ""

    async def grade(
        self,
        solution: str,
        task: Task,
    ) -> GradeResult:
        """Grade the solution by importing and testing it.

        Args:
            solution: The implementation code
            task: The task (contains ID for looking up grader)

        Returns:
            GradeResult with scores from the grader function
        """
        task_dir = self._task_dirs.get(task.id)
        if not task_dir:
            return GradeResult(
                passed=False,
                error="Task not set up. Call setup() first.",
            )

        if not solution or not solution.strip():
            return GradeResult(
                passed=False,
                error="No solution provided",
                message="Empty implementation",
            )

        # Write solution to file if not already there
        solution_file = task_dir / "solution.py"
        if not solution_file.exists() or solution_file.read_text() != solution:
            solution_file.write_text(solution)

        # Look up grader - try registered first, then auto-discover from task hints
        grader_fn = self._graders.get(task.id)
        if not grader_fn:
            grader_fn = self._discover_grader(task)
        if not grader_fn:
            # Try generic grading if no specific grader
            return await self._generic_grade(solution, task)

        try:
            # Import the solution module
            spec = importlib.util.spec_from_file_location("solution", solution_file)
            if not spec or not spec.loader:
                return GradeResult(
                    passed=False,
                    error="Could not load solution module",
                )

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find the function (assume it's named in the task)
            fn_name = self._extract_function_name(task.prompt)
            if not hasattr(module, fn_name):
                return GradeResult(
                    passed=False,
                    error=f"Function '{fn_name}' not found in solution",
                )

            impl_fn = getattr(module, fn_name)

            # Run the grader
            results = grader_fn(impl_fn)

            # Calculate overall score and pass/fail
            weighted_score = results.get("weighted_score", 0.0)
            verdict = results.get("verdict", "FAIL")

            # Count tests
            total = sum(r.get("total", 0) for r in [
                results.get("basic", {}),
                results.get("edge_cases", {}),
                results.get("security", {}),
            ])
            passed_count = sum(r.get("passed", 0) for r in [
                results.get("basic", {}),
                results.get("edge_cases", {}),
                results.get("security", {}),
            ])

            return GradeResult(
                passed=verdict == "PASS",
                score=weighted_score,
                message=f"Score: {weighted_score:.0%}",
                tests_passed=passed_count,
                tests_failed=total - passed_count,
                tests_total=total,
                details=results,
            )

        except SyntaxError as e:
            return GradeResult(
                passed=False,
                error=f"Syntax error in solution: {e}",
                message="Could not parse solution",
            )
        except Exception as e:
            return GradeResult(
                passed=False,
                error=f"Error grading solution: {e}",
                message=str(e),
            )

    async def _generic_grade(self, solution: str, task: Task) -> GradeResult:
        """Generic grading when no specific grader is registered.

        Just checks if the solution is valid Python.
        """
        try:
            compile(solution, "<solution>", "exec")
            return GradeResult(
                passed=True,
                score=0.5,
                message="Solution is valid Python (no specific grader)",
            )
        except SyntaxError as e:
            return GradeResult(
                passed=False,
                error=f"Syntax error: {e}",
            )

    def _extract_function_name(self, template: str) -> str:
        """Extract function name from template.

        Looks for 'def function_name(' pattern.
        """
        import re
        match = re.search(r"def\s+(\w+)\s*\(", template)
        if match:
            return match.group(1)
        return "solution"  # Default

    def _discover_grader(self, task: Task) -> Callable | None:
        """Try to discover a grader function for the task.

        Looks in task.hints for grader metadata like:
            grader_module: path.to.module
            grader_function: grade_implementation
        """
        import sys

        # Check if hints contain grader info
        hints = task.hints
        if not hints:
            return None

        # Parse hints for grader metadata (simple key: value format)
        grader_module = None
        grader_function = "grade_implementation"  # Default

        for line in hints.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                if key == "grader_module":
                    grader_module = value
                elif key == "grader_function":
                    grader_function = value

        if not grader_module:
            return None

        try:
            # Import the module
            module = importlib.import_module(grader_module)
            if hasattr(module, grader_function):
                return getattr(module, grader_function)
        except Exception:
            pass

        return None

    async def teardown(self, task: Task) -> None:
        """Cleanup task workspace."""
        if self.keep_workspace:
            return

        task_dir = self._task_dirs.pop(task.id, None)
        if task_dir and task_dir.exists():
            shutil.rmtree(task_dir)
