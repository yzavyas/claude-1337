"""Filesystem Storage Adapter - JSONL streaming + JSON summaries.

Implements StoragePort with a streaming-friendly file layout:
- Results are appended to JSONL as they complete (crash-safe)
- Summaries are written as JSON at the end
- Supports resumption by reading completed runs from JSONL
"""

import json
from pathlib import Path
from typing import Iterator

import yaml

from lab.domain.models import (
    Batch,
    RunResult,
    BatchResults,
    RunIdentity,
    Task,
    Condition,
    ConditionType,
    IterationConfig,
    IterationStrategy,
)
from lab.ports.driven.storage import StoragePort


class StreamingFileAdapter:
    """Storage adapter using JSONL for streaming results.

    File layout:
        results/
            {batch_name}/
                results.jsonl    # Append-only run results
                summary.json     # Final aggregated summary

    Implements crash-safe streaming:
    - Each result is immediately flushed to disk
    - Resumption reads existing results and skips completed runs
    """

    def __init__(self, results_dir: Path | None = None):
        """Initialize the adapter.

        Args:
            results_dir: Directory for results. Defaults to ./results
        """
        self.results_dir = results_dir or Path("results")
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def append_result(
        self,
        batch_name: str,
        result: RunResult,
    ) -> None:
        """Append a single result to JSONL.

        Immediately flushes to disk for crash safety.
        """
        batch_dir = self.results_dir / batch_name
        batch_dir.mkdir(parents=True, exist_ok=True)

        results_file = batch_dir / "results.jsonl"
        with open(results_file, "a") as f:
            f.write(result.model_dump_json() + "\n")
            f.flush()

    def stream_results(
        self,
        batch_name: str,
    ) -> Iterator[RunResult]:
        """Stream results from JSONL.

        Yields results one at a time for memory efficiency.
        """
        results_file = self.results_dir / batch_name / "results.jsonl"
        if not results_file.exists():
            return

        with open(results_file, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    data = json.loads(line)
                    yield RunResult.model_validate(data)

    def get_completed_runs(
        self,
        batch_name: str,
    ) -> set[RunIdentity]:
        """Get identities of completed runs for resumption."""
        completed = set()
        for result in self.stream_results(batch_name):
            completed.add(result.identity)
        return completed

    def save_summary(
        self,
        batch_name: str,
        summary: BatchResults,
    ) -> Path:
        """Save final summary as JSON."""
        batch_dir = self.results_dir / batch_name
        batch_dir.mkdir(parents=True, exist_ok=True)

        summary_file = batch_dir / "summary.json"
        with open(summary_file, "w") as f:
            f.write(summary.model_dump_json(indent=2))

        return summary_file

    def load_batch(
        self,
        batch_path: Path,
    ) -> Batch:
        """Load a batch configuration from YAML.

        Loads the batch YAML and resolves referenced conditions and tasks.
        """
        with open(batch_path, "r") as f:
            data = yaml.safe_load(f)

        # Resolve base directory for relative paths
        # The experiment root is typically the parent of batches/ or scenarios/
        # batch_path: experiments/rep-002/scenarios/pilot.yaml
        # base_dir should be: experiments/rep-002/
        batch_dir = batch_path.parent
        if batch_dir.name in ("batches", "scenarios"):
            base_dir = batch_dir.parent  # Go up to experiment root
        else:
            base_dir = batch_dir

        # Load conditions
        conditions: list[Condition] = []
        for cond_ref in data.get("conditions", []):
            cond_path = base_dir / cond_ref
            conditions.append(self._load_condition(cond_path))

        # Load tasks
        tasks: list[Task] = []
        for task_ref in data.get("tasks", []):
            task_path = base_dir / task_ref
            tasks.append(self._load_task(task_path))

        # Build iteration config
        iteration_data = data.get("iteration", {})
        iteration = IterationConfig(
            strategy=IterationStrategy(iteration_data.get("strategy", "none")),
            max_iterations=iteration_data.get("max_iterations", 1),
            review_prompt=iteration_data.get("review_prompt", ""),
        )

        return Batch(
            name=data.get("name", batch_path.stem),
            tasks=tasks,
            conditions=conditions,
            runs_per_condition=data.get("runs_per_condition", 5),
            model=data.get("model", "sonnet"),
            iteration=iteration,
            description=data.get("description", ""),
            hypothesis=data.get("hypothesis", ""),
        )

    def _load_condition(self, path: Path) -> Condition:
        """Load a condition from a markdown file.

        Expected format:
        ---
        name: condition-name
        type: motivation|mandate|baseline
        style: optional style tag
        ---
        Prompt content here...
        """
        content = path.read_text()

        # Parse YAML frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                prompt = parts[2].strip()
            else:
                frontmatter = {}
                prompt = content
        else:
            frontmatter = {}
            prompt = content

        return Condition(
            name=frontmatter.get("name", path.stem),
            type=ConditionType(frontmatter.get("type", "baseline")),
            prompt=prompt,
            description=frontmatter.get("description", ""),
            style=frontmatter.get("style"),
        )

    def _load_task(self, path: Path) -> Task:
        """Load a task from a YAML or markdown file.

        YAML format:
            id: task-id
            prompt: Task prompt text
            difficulty: easy|medium|hard
            fail_to_pass:
              - test_1
              - test_2

        Markdown format with frontmatter also supported.
        """
        content = path.read_text()

        if path.suffix in (".yaml", ".yml"):
            data = yaml.safe_load(content)
            # Support both SWE-bench format (problem_statement) and our format (prompt)
            prompt = data.get("prompt") or data.get("problem_statement", "")
            hints = data.get("hints") or data.get("hints_text", "")
            task_id = data.get("id") or data.get("instance_id", path.stem)
            return Task(
                id=task_id,
                prompt=prompt,
                repo=data.get("repo", ""),
                base_commit=data.get("base_commit", ""),
                fail_to_pass=tuple(data.get("fail_to_pass", [])),
                pass_to_pass=tuple(data.get("pass_to_pass", [])),
                difficulty=data.get("difficulty", "medium"),
                hints=hints,
            )
        else:
            # Markdown with YAML frontmatter
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    prompt = parts[2].strip()
                else:
                    frontmatter = {}
                    prompt = content
            else:
                frontmatter = {}
                prompt = content

            return Task(
                id=frontmatter.get("id", path.stem),
                prompt=prompt,
                repo=frontmatter.get("repo", ""),
                base_commit=frontmatter.get("base_commit", ""),
                fail_to_pass=tuple(frontmatter.get("fail_to_pass", [])),
                pass_to_pass=tuple(frontmatter.get("pass_to_pass", [])),
                difficulty=frontmatter.get("difficulty", "medium"),
                hints=frontmatter.get("hints", ""),
            )

    def batch_exists(
        self,
        batch_name: str,
    ) -> bool:
        """Check if results exist for a batch."""
        results_file = self.results_dir / batch_name / "results.jsonl"
        return results_file.exists()
