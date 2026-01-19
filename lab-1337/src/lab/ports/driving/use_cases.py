"""Use Cases - Application services that orchestrate the domain.

Use cases are the "API" of your application. They:
1. Take input from the driving adapter (CLI, API)
2. Coordinate domain objects
3. Call driven adapters (LLM, Storage, etc.)
4. Return results

Each use case is a single, complete action the application can perform.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import AsyncIterator

from lab.domain.models import Batch, RunResult, Run, BatchResults
from lab.domain.services import PromptBuilder, RunSelector
from lab.domain.statistics import PerConditionStatistics

from lab.ports.driven.llm import LLMPort, LLMConfig
from lab.ports.driven.grader import GraderPort
from lab.ports.driven.tracer import TracerPort
from lab.ports.driven.storage import StoragePort


@dataclass
class RunExperimentInput:
    """Input for RunExperimentUseCase."""
    batch_path: Path
    resume: bool = False  # Resume from previous partial run


class RunExperimentUseCase:
    """Execute an experiment batch, streaming results.

    This is the main use case - it coordinates:
    1. Loading the batch configuration
    2. Generating runs
    3. Executing each run (LLM + grading)
    4. Streaming results to storage
    5. Tracking online statistics

    Yields results as they complete (streaming).
    """

    def __init__(
        self,
        llm: LLMPort,
        grader: GraderPort,
        tracer: TracerPort,
        storage: StoragePort,
    ):
        self.llm = llm
        self.grader = grader
        self.tracer = tracer
        self.storage = storage
        self.prompt_builder = PromptBuilder()

    async def execute(
        self,
        input: RunExperimentInput,
    ) -> AsyncIterator[RunResult]:
        """Run the experiment, streaming results.

        Yields RunResult as each run completes.
        Results are also persisted to storage incrementally.
        """
        # Load batch configuration
        batch = self.storage.load_batch(input.batch_path)

        # Handle resumption
        completed = set()
        if input.resume:
            completed = self.storage.get_completed_runs(batch.name)

        # Track statistics
        stats = PerConditionStatistics()

        # Create overall tracing span
        with self.tracer.span("experiment_batch", {
            "batch_name": batch.name,
            "total_runs": batch.total_runs,
            "model": batch.model,
        }):
            # Stream through runs
            for run in batch.generate_runs():
                # Skip completed runs (resumption)
                if run.identity in completed:
                    continue

                # Execute single run
                result = await self._execute_run(run, batch)

                # Persist immediately (streaming)
                self.storage.append_result(batch.name, result)

                # Update statistics
                stats.update(result)

                # Yield for progress tracking
                yield result

            # Save final summary
            summary = BatchResults(batch_name=batch.name)
            for result in self.storage.stream_results(batch.name):
                summary.add_result(result)

            self.storage.save_summary(batch.name, summary)

    async def _execute_run(
        self,
        run: Run,
        batch: Batch,
    ) -> RunResult:
        """Execute a single run."""
        run.start()

        with self.tracer.span("experiment_run", {
            "task_id": run.task_id,
            "condition": run.condition_name,
            "attempt": run.attempt,
        }) as span:
            try:
                # Get task and condition
                task = batch.get_task(run.task_id)
                condition = batch.get_condition(run.condition_name)

                if not task or not condition:
                    raise ValueError(f"Missing task or condition for run: {run.identity}")

                # Build prompts separately for proper agent configuration
                # - condition.prompt → system_prompt (agent framing/personality)
                # - task_prompt → user prompt (what to solve)
                task_prompt = self.prompt_builder.build_task_prompt(task)

                # Call LLM with iteration
                config = LLMConfig(
                    model=batch.model,
                    system_prompt=condition.prompt,  # Condition becomes system prompt
                )
                response, iterations = await self.llm.generate_with_iteration(
                    prompt=task_prompt,  # Task is the user prompt
                    config=config,
                    max_iterations=batch.iteration.max_iterations,
                    review_prompt=batch.iteration.review_prompt,
                )

                # Setup grader for this task (clone repo, etc.)
                await self.grader.setup(task)

                # Grade the solution
                grade = await self.grader.grade(response.content, task)

                # Cleanup grader
                await self.grader.teardown(task)

                # Build result
                result = RunResult(
                    task_id=run.task_id,
                    condition_name=run.condition_name,
                    attempt=run.attempt,
                    passed=grade.passed,
                    score=grade.score,
                    iterations_used=iterations,
                    tokens_input=response.tokens_input,
                    tokens_output=response.tokens_output,
                    duration_ms=response.duration_ms,
                    trace_id=self.tracer.get_trace_id(),
                )

                span.set_attribute("passed", result.passed)
                span.set_attribute("iterations", iterations)
                span.set_attribute("tokens", result.total_tokens)

                run.complete(result)
                return result

            except Exception as e:
                span.record_exception(e)
                run.fail(str(e))
                return run.result  # type: ignore


class LoadBatchUseCase:
    """Load a batch configuration.

    Simple use case for CLI commands that just need to inspect a batch.
    """

    def __init__(self, storage: StoragePort):
        self.storage = storage

    def execute(self, batch_path: Path) -> Batch:
        """Load batch from path."""
        return self.storage.load_batch(batch_path)
