"""Domain services for lab-1337.

Pure functions that operate on domain models.
No external dependencies - just business logic.
"""

from .models import Task, Condition, Batch, Run, RunIdentity


class PromptBuilder:
    """Builds prompts for Claude Agent SDK.

    For proper agent configuration:
    - condition.prompt → system_prompt (agent framing)
    - build_task_prompt() → user prompt (what to solve)
    """

    @staticmethod
    def build_task_prompt(task: Task) -> str:
        """Build the task prompt (user message)."""
        parts = []

        parts.append("## Issue to Resolve\n")

        if task.repo:
            parts.append(f"**Repository:** {task.repo}\n")

        parts.append(f"**Issue ID:** {task.id}\n")
        parts.append("")
        parts.append(task.prompt)

        if task.hints:
            parts.append("\n\n## Additional Context\n")
            parts.append(task.hints)

        return "".join(parts)

    @staticmethod
    def build_review_prompt(iteration_config) -> str:
        """Build the self-review prompt for iteration."""
        return iteration_config.review_prompt


class RunSelector:
    """Selects which runs to execute from a batch.

    Handles filtering, ordering, and resumption logic.
    """

    @staticmethod
    def pending_runs(batch: Batch, completed: set[RunIdentity] | None = None) -> list[Run]:
        """Get all pending runs, optionally filtering out completed ones.

        Args:
            batch: The batch to get runs from
            completed: Set of already-completed run identities (for resumption)

        Returns:
            List of Run objects that still need to be executed
        """
        completed = completed or set()
        pending = []

        for run in batch.generate_runs():
            if run.identity not in completed:
                pending.append(run)

        return pending

    @staticmethod
    def next_run(batch: Batch, completed: set[RunIdentity] | None = None) -> Run | None:
        """Get the next pending run.

        Args:
            batch: The batch to get runs from
            completed: Set of already-completed run identities

        Returns:
            The next Run to execute, or None if all complete
        """
        completed = completed or set()

        for run in batch.generate_runs():
            if run.identity not in completed:
                return run

        return None

    @staticmethod
    def progress(batch: Batch, completed: set[RunIdentity]) -> tuple[int, int]:
        """Get progress as (completed, total).

        Args:
            batch: The batch
            completed: Set of completed run identities

        Returns:
            Tuple of (completed_count, total_count)
        """
        total = batch.total_runs
        done = len(completed)
        return (done, total)
