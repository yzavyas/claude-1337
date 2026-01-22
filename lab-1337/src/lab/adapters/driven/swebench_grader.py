"""SWE-bench Grader Adapter - Subprocess-based evaluation.

Runs pytest directly without Docker for faster iteration.
For production, use the full swebench harness with Docker isolation.

Security note: Uses asyncio.create_subprocess_exec (not shell) with
argument lists - no command injection risk.
"""

import asyncio
import shutil
import tempfile
from pathlib import Path

from lab.domain.models import Task
from lab.ports.driven.grader import GraderPort, GradeResult


class SWEBenchGraderAdapter:
    """Grader for SWE-bench tasks using subprocess.

    Lighter-weight than Docker-based evaluation:
    1. Clone repo at base_commit
    2. Apply patch from solution
    3. Run fail_to_pass tests (should pass after fix)
    4. Run pass_to_pass tests (should still pass)
    """

    def __init__(
        self,
        workspace_dir: Path | None = None,
        timeout: int = 300,  # 5 min default
        keep_workspace: bool = False,
    ):
        """Initialize the grader.

        Args:
            workspace_dir: Where to clone repos. Defaults to temp dir.
            timeout: Test execution timeout in seconds.
            keep_workspace: Keep workspace after grading (for debugging).
        """
        self.workspace_dir = workspace_dir or Path(tempfile.mkdtemp(prefix="swebench_"))
        self.timeout = timeout
        self.keep_workspace = keep_workspace
        self._task_dirs: dict[str, Path] = {}

    async def setup(self, task: Task) -> None:
        """Clone the repo at base_commit.

        Uses shallow clone + fetch for efficiency:
        1. Shallow clone (fast, gets recent refs)
        2. Fetch specific commit (only what we need)
        3. Checkout the commit

        This is faster than full clone for large repos like astropy.
        """
        if not task.repo or not task.base_commit:
            return  # Not a SWE-bench task

        task_dir = self.workspace_dir / task.id
        if task_dir.exists():
            shutil.rmtree(task_dir)
        task_dir.mkdir(parents=True)

        # Clone the repo (shallow for speed)
        repo_url = f"https://github.com/{task.repo}.git"
        clone_result = await self._run_command(
            ["git", "clone", "--depth", "1", repo_url, str(task_dir)],
            cwd=self.workspace_dir,
        )
        if clone_result.returncode != 0:
            raise RuntimeError(f"Failed to clone {repo_url}: {clone_result.stderr}")

        # Fetch the specific commit we need (works for any depth)
        fetch_result = await self._run_command(
            ["git", "fetch", "--depth", "1", "origin", task.base_commit],
            cwd=task_dir,
        )
        if fetch_result.returncode != 0:
            # Fallback: full fetch if specific commit fetch fails
            fetch_result = await self._run_command(
                ["git", "fetch", "--unshallow"],
                cwd=task_dir,
                timeout=600,  # Full fetch can take a while
            )
            if fetch_result.returncode != 0:
                raise RuntimeError(f"Failed to fetch {task.base_commit}: {fetch_result.stderr}")

        # Checkout base commit
        checkout_result = await self._run_command(
            ["git", "checkout", task.base_commit],
            cwd=task_dir,
        )
        if checkout_result.returncode != 0:
            raise RuntimeError(f"Failed to checkout {task.base_commit}: {checkout_result.stderr}")

        # Install dependencies (best effort)
        await self._install_deps(task_dir)

        self._task_dirs[task.id] = task_dir

    async def _install_deps(self, repo_dir: Path) -> None:
        """Install Python dependencies (best effort)."""
        # Try pyproject.toml first
        if (repo_dir / "pyproject.toml").exists():
            await self._run_command(
                ["uv", "pip", "install", "-e", "."],
                cwd=repo_dir,
                check=False,
            )
        # Try setup.py
        elif (repo_dir / "setup.py").exists():
            await self._run_command(
                ["uv", "pip", "install", "-e", "."],
                cwd=repo_dir,
                check=False,
            )
        # Try requirements.txt
        elif (repo_dir / "requirements.txt").exists():
            await self._run_command(
                ["uv", "pip", "install", "-r", "requirements.txt"],
                cwd=repo_dir,
                check=False,
            )

    async def grade(
        self,
        solution: str,
        task: Task,
    ) -> GradeResult:
        """Grade a solution against the task.

        Args:
            solution: The patch or code changes to apply.
            task: The task being solved.

        Returns:
            GradeResult with pass/fail and test details.
        """
        task_dir = self._task_dirs.get(task.id)
        if not task_dir:
            return GradeResult(
                passed=False,
                error="Task not set up. Call setup() first.",
            )

        # Apply the patch/solution
        apply_result = await self._apply_solution(solution, task_dir)
        if not apply_result.success:
            return GradeResult(
                passed=False,
                error=f"Failed to apply solution: {apply_result.error}",
                message="Patch application failed",
            )

        # Run fail_to_pass tests (should pass after fix)
        fail_to_pass_result = await self._run_tests(
            task.fail_to_pass,
            task_dir,
            "fail_to_pass",
        )

        # Run pass_to_pass tests (should still pass)
        pass_to_pass_result = await self._run_tests(
            task.pass_to_pass,
            task_dir,
            "pass_to_pass",
        )

        # Determine overall result
        fail_to_pass_ok = fail_to_pass_result.all_passed
        pass_to_pass_ok = pass_to_pass_result.all_passed

        passed = fail_to_pass_ok and pass_to_pass_ok

        # Build message
        messages = []
        if fail_to_pass_ok:
            messages.append(f"fail_to_pass: {fail_to_pass_result.passed}/{fail_to_pass_result.total} passed ✓")
        else:
            messages.append(f"fail_to_pass: {fail_to_pass_result.passed}/{fail_to_pass_result.total} passed ✗")

        if pass_to_pass_ok:
            messages.append(f"pass_to_pass: {pass_to_pass_result.passed}/{pass_to_pass_result.total} passed ✓")
        else:
            messages.append(f"pass_to_pass: {pass_to_pass_result.passed}/{pass_to_pass_result.total} passed ✗")

        total_tests = fail_to_pass_result.total + pass_to_pass_result.total
        total_passed = fail_to_pass_result.passed + pass_to_pass_result.passed

        return GradeResult(
            passed=passed,
            score=total_passed / total_tests if total_tests > 0 else 0.0,
            message="; ".join(messages),
            tests_passed=total_passed,
            tests_failed=total_tests - total_passed,
            tests_total=total_tests,
            details={
                "fail_to_pass": fail_to_pass_result.to_dict(),
                "pass_to_pass": pass_to_pass_result.to_dict(),
            },
        )

    async def teardown(self, task: Task) -> None:
        """Cleanup task workspace."""
        if self.keep_workspace:
            return

        task_dir = self._task_dirs.pop(task.id, None)
        if task_dir and task_dir.exists():
            shutil.rmtree(task_dir)

    async def _apply_solution(self, solution: str, repo_dir: Path) -> "ApplyResult":
        """Apply the solution to the repo.

        Tries multiple methods:
        1. git apply (if it looks like a patch)
        2. Direct file write (if it looks like code)
        """
        # Try as git patch first
        if solution.strip().startswith("diff ") or solution.strip().startswith("---"):
            patch_file = repo_dir / "solution.patch"
            patch_file.write_text(solution)

            result = await self._run_command(
                ["git", "apply", "--check", str(patch_file)],
                cwd=repo_dir,
            )

            if result.returncode == 0:
                # Patch is valid, apply it
                result = await self._run_command(
                    ["git", "apply", str(patch_file)],
                    cwd=repo_dir,
                )
                if result.returncode == 0:
                    return ApplyResult(success=True)
                return ApplyResult(success=False, error=result.stderr)

        # If not a patch or patch failed, try to detect file path and content
        # This is a fallback - real solutions should be patches
        return ApplyResult(
            success=False,
            error="Solution does not appear to be a valid git patch. Expected 'diff' or '---' header.",
        )

    async def _run_tests(
        self,
        test_specs: tuple[str, ...],
        repo_dir: Path,
        category: str,
    ) -> "TestResult":
        """Run specified tests."""
        if not test_specs:
            return TestResult(total=0, passed=0, failed=0, all_passed=True)

        passed = 0
        failed = 0
        failures = []

        for test_spec in test_specs:
            result = await self._run_command(
                ["uv", "run", "pytest", "-xvs", test_spec],
                cwd=repo_dir,
                timeout=self.timeout,
            )

            if result.returncode == 0:
                passed += 1
            else:
                failed += 1
                failures.append({
                    "test": test_spec,
                    "returncode": result.returncode,
                    "stdout": result.stdout[-2000:] if result.stdout else "",
                    "stderr": result.stderr[-2000:] if result.stderr else "",
                })

        return TestResult(
            total=len(test_specs),
            passed=passed,
            failed=failed,
            all_passed=failed == 0,
            failures=failures,
        )

    async def _run_command(
        self,
        cmd: list[str],
        cwd: Path,
        timeout: int | None = None,
        check: bool = True,
    ) -> "CommandResult":
        """Run a command asynchronously using subprocess_exec (safe, no shell)."""
        timeout = timeout or self.timeout

        try:
            # Using create_subprocess_exec with argument list - no shell injection
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=timeout,
            )

            return CommandResult(
                returncode=proc.returncode or 0,
                stdout=stdout.decode() if stdout else "",
                stderr=stderr.decode() if stderr else "",
            )

        except asyncio.TimeoutError:
            proc.kill()
            return CommandResult(
                returncode=-1,
                stdout="",
                stderr=f"Command timed out after {timeout}s",
            )
        except Exception as e:
            return CommandResult(
                returncode=-1,
                stdout="",
                stderr=str(e),
            )


# --- Helper dataclasses ---

class CommandResult:
    """Result of a shell command."""
    def __init__(self, returncode: int, stdout: str, stderr: str):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class ApplyResult:
    """Result of applying a solution."""
    def __init__(self, success: bool, error: str = ""):
        self.success = success
        self.error = error


class TestResult:
    """Result of running tests."""
    def __init__(
        self,
        total: int,
        passed: int,
        failed: int,
        all_passed: bool,
        failures: list | None = None,
    ):
        self.total = total
        self.passed = passed
        self.failed = failed
        self.all_passed = all_passed
        self.failures = failures or []

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "all_passed": self.all_passed,
            "failures": self.failures,
        }
