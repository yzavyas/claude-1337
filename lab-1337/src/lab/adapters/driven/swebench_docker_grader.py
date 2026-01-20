"""SWE-bench Docker Grader - Uses official SWE-bench harness with Docker.

This grader uses the official SWE-bench Docker-based evaluation pipeline
for accurate, reproducible results. It:
1. Sets up Claude to work in a cloned repo
2. Captures Claude's git diff as the "prediction"
3. Uses swebench.harness.run_evaluation to grade in Docker

Requires Docker to be running (e.g., via colima).

Security note: Uses asyncio.create_subprocess_exec (not shell) with
argument lists - no command injection risk.
"""

import asyncio
import shutil
import uuid
from pathlib import Path
from typing import Any

import docker
from datasets import load_dataset

from lab.domain.models import Task
from lab.ports.driven.grader import GraderPort, GradeResult


def get_cache_dir() -> Path:
    """Get cache directory for repo clones."""
    return Path.home() / ".cache" / "lab-1337" / "swebench"


class SWEBenchDockerGraderAdapter:
    """Grader using official SWE-bench Docker harness.

    Workflow:
    1. setup(): Clone repo, return working directory for Claude
    2. Claude edits files directly in the working directory
    3. get_solution(): Capture git diff
    4. grade(): Use SWE-bench Docker harness to evaluate
    """

    def __init__(
        self,
        workspace_dir: Path | None = None,
        timeout: int = 600,  # 10 min - Docker builds take time
        keep_workspace: bool = True,
        dataset_name: str = "princeton-nlp/SWE-bench_Verified",
    ):
        """Initialize the Docker grader.

        Args:
            workspace_dir: Where to clone repos
            timeout: Test timeout in seconds
            keep_workspace: Keep workspace after grading
            dataset_name: HuggingFace dataset for SWE-bench
        """
        self.workspace_dir = workspace_dir or get_cache_dir()
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.timeout = timeout
        self.keep_workspace = keep_workspace
        self.dataset_name = dataset_name

        # Task state
        self._task_dirs: dict[str, Path] = {}
        self._instances: dict[str, dict] = {}  # instance_id -> dataset row

        # Lazy-loaded dataset
        self._dataset = None

        # Run ID for this grader session
        self._run_id = f"lab-{uuid.uuid4().hex[:8]}"

    def _load_dataset(self) -> None:
        """Lazy load the SWE-bench dataset."""
        if self._dataset is None:
            self._dataset = load_dataset(self.dataset_name, split="test")
            # Index by instance_id for fast lookup
            self._instances = {item["instance_id"]: item for item in self._dataset}

    async def setup(self, task: Task) -> str | None:
        """Clone the repo at base_commit for Claude to work in.

        Returns:
            Path to the working directory, or None if not a SWE-bench task.
        """
        if not task.repo or not task.base_commit:
            return None

        # Load dataset to get full instance data
        self._load_dataset()

        task_dir = self.workspace_dir / task.id
        if task_dir.exists():
            shutil.rmtree(task_dir)
        task_dir.mkdir(parents=True)

        # Clone repo
        repo_url = f"https://github.com/{task.repo}.git"
        clone_result = await self._run_command(
            ["git", "clone", "--depth", "1", repo_url, str(task_dir)],
            cwd=self.workspace_dir,
        )
        if clone_result.returncode != 0:
            raise RuntimeError(f"Clone failed: {clone_result.stderr}")

        # Fetch and checkout base commit
        await self._run_command(
            ["git", "fetch", "--depth", "1", "origin", task.base_commit],
            cwd=task_dir,
        )
        checkout = await self._run_command(
            ["git", "checkout", task.base_commit],
            cwd=task_dir,
        )
        if checkout.returncode != 0:
            # Try full fetch if shallow fetch fails
            await self._run_command(
                ["git", "fetch", "--unshallow"],
                cwd=task_dir,
                timeout=600,
            )
            await self._run_command(
                ["git", "checkout", task.base_commit],
                cwd=task_dir,
            )

        self._task_dirs[task.id] = task_dir
        return str(task_dir)

    async def get_solution(self, task: Task) -> str:
        """Get git diff from workspace after Claude made changes."""
        task_dir = self._task_dirs.get(task.id)
        if not task_dir:
            return ""

        result = await self._run_command(
            ["git", "diff"],
            cwd=task_dir,
        )
        return result.stdout if result.returncode == 0 else ""

    async def grade(self, solution: str, task: Task) -> GradeResult:
        """Grade using official SWE-bench Docker harness.

        This runs the solution in a Docker container with proper environment.
        """
        if not solution or not solution.strip():
            return GradeResult(
                passed=False,
                error="No changes made (empty diff)",
            )

        # Import SWE-bench harness (delay import to avoid startup cost)
        from swebench.harness.run_evaluation import (
            make_test_spec,
            run_instance,
            KEY_MODEL,
            KEY_PREDICTION,
            KEY_INSTANCE_ID,
        )
        from swebench.harness.constants import SWEbenchInstance

        # Get instance data from dataset
        instance_data = self._instances.get(task.id)
        if not instance_data:
            return GradeResult(
                passed=False,
                error=f"Instance {task.id} not found in dataset",
            )

        # Convert to SWEbenchInstance
        swebench_instance = SWEbenchInstance(**instance_data)

        # Create test spec
        test_spec = make_test_spec(swebench_instance)

        # Create prediction
        pred = {
            KEY_INSTANCE_ID: task.id,
            KEY_MODEL: "lab-1337-claude",
            KEY_PREDICTION: solution,
        }

        # Connect to Docker
        try:
            client = docker.from_env()
        except Exception as e:
            return GradeResult(
                passed=False,
                error=f"Docker not available: {e}",
            )

        # Run evaluation in thread pool (Docker operations are blocking)
        try:
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: run_instance(
                    test_spec=test_spec,
                    pred=pred,
                    rm_image=False,  # Keep images for speed
                    force_rebuild=False,
                    client=client,
                    run_id=self._run_id,
                    timeout=self.timeout,
                ),
            )
        except Exception as e:
            return GradeResult(
                passed=False,
                error=f"Docker evaluation failed: {e}",
            )

        # Parse result
        completed = result.get("completed", False)
        resolved = result.get("resolved", False)

        return GradeResult(
            passed=resolved,
            score=1.0 if resolved else 0.0,
            message=f"Completed: {completed}, Resolved: {resolved}",
            details=result,
        )

    async def teardown(self, task: Task) -> None:
        """Cleanup workspace."""
        if self.keep_workspace:
            return

        task_dir = self._task_dirs.pop(task.id, None)
        if task_dir and task_dir.exists():
            shutil.rmtree(task_dir)

    async def _run_command(
        self,
        cmd: list[str],
        cwd: Path,
        timeout: int | None = None,
    ) -> Any:
        """Run a command asynchronously.

        Uses create_subprocess_exec with argument list (no shell injection).
        """
        timeout = timeout or 120

        try:
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
            return _CommandResult(
                returncode=proc.returncode or 0,
                stdout=stdout.decode() if stdout else "",
                stderr=stderr.decode() if stderr else "",
            )
        except asyncio.TimeoutError:
            return _CommandResult(
                returncode=-1,
                stdout="",
                stderr=f"Timed out after {timeout}s",
            )
        except Exception as e:
            return _CommandResult(
                returncode=-1,
                stdout="",
                stderr=str(e),
            )


class _CommandResult:
    """Simple command result holder."""
    def __init__(self, returncode: int, stdout: str, stderr: str):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
