"""Core experiment harness for methodology comparison.

Uses ClaudeSDKClient for all strategies with proper tool support.
Real Ralph iteration uses file persistence, not conversation history.
"""

import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
from contextlib import contextmanager

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock

from .config import AgentConfig, TaskConfig
from .evaluation import evaluate_code, EvaluationResult


# OpenTelemetry instrumentation (optional)
try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
    from opentelemetry.sdk.resources import Resource

    resource = Resource.create({"service.name": "lep-001-experiment"})
    provider = TracerProvider(resource=resource)
    processor = SimpleSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer("lep-001")
    OTEL_ENABLED = True
except ImportError:
    OTEL_ENABLED = False
    tracer = None


@contextmanager
def span(name: str, attributes: dict[str, Any] | None = None):
    """Context manager for OTel spans."""
    if OTEL_ENABLED and tracer:
        with tracer.start_as_current_span(name) as s:
            if attributes:
                for k, v in attributes.items():
                    s.set_attribute(k, v)
            yield s
    else:
        yield None


@dataclass
class RunResult:
    """Result of a single experimental run."""

    agent: str
    run_number: int
    correctness: bool
    iterations_used: int
    tokens_input: int
    tokens_output: int
    tokens_total: int
    cost_usd: float | None
    duration_ms: int
    evaluation: EvaluationResult
    final_code: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent": self.agent,
            "run_number": self.run_number,
            "correctness": self.correctness,
            "iterations_used": self.iterations_used,
            "tokens_input": self.tokens_input,
            "tokens_output": self.tokens_output,
            "tokens_total": self.tokens_total,
            "cost_usd": self.cost_usd,
            "duration_ms": self.duration_ms,
            "evaluation": {
                "passed": self.evaluation.passed,
                "failed": self.evaluation.failed,
                "total": self.evaluation.total,
                "correctness": self.evaluation.correctness,
                "errors": self.evaluation.errors,
            },
            "timestamp": self.timestamp,
        }


@dataclass
class ExperimentResults:
    """Aggregated results across all runs."""

    runs: list[RunResult]
    task_name: str = ""
    model: str = ""
    summary: dict[str, Any] = field(default_factory=dict)

    def compute_summary(self) -> None:
        """Compute summary statistics per agent."""
        by_agent: dict[str, list[RunResult]] = {}
        for run in self.runs:
            by_agent.setdefault(run.agent, []).append(run)

        self.summary = {}
        for agent, runs in by_agent.items():
            successes = sum(1 for r in runs if r.correctness)
            total_tokens = sum(r.tokens_total for r in runs)
            total_iterations = sum(r.iterations_used for r in runs)

            self.summary[agent] = {
                "runs": len(runs),
                "successes": successes,
                "failures": len(runs) - successes,
                "success_rate": successes / len(runs) if runs else 0,
                "avg_tokens": total_tokens / len(runs) if runs else 0,
                "avg_iterations": total_iterations / len(runs) if runs else 0,
                "total_cost_usd": sum(r.cost_usd or 0 for r in runs),
            }

    def to_dict(self) -> dict[str, Any]:
        return {
            "runs": [r.to_dict() for r in self.runs],
            "summary": self.summary,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_runs": len(self.runs),
                "agents": list(set(r.agent for r in self.runs)),
                "task": self.task_name,
                "model": self.model,
            },
        }


async def run_agent(
    agent: AgentConfig,
    task: TaskConfig,
    run_number: int,
    model: str = "sonnet",
) -> RunResult:
    """Run a single agent on a task."""
    strategy = agent.iteration.strategy
    max_iterations = agent.iteration.max_iterations

    with span("experiment_run", {
        "agent": agent.name,
        "run_number": run_number,
        "model": model,
        "task": task.name,
        "strategy": strategy,
    }):
        if strategy == "none":
            return await _run_single_shot(agent, task, run_number, model)
        elif strategy == "ralph":
            return await _run_ralph(agent, task, run_number, model, max_iterations)
        elif strategy == "self-review":
            return await _run_self_review(agent, task, run_number, model, max_iterations)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")


async def _run_single_shot(
    agent: AgentConfig,
    task: TaskConfig,
    run_number: int,
    model: str,
) -> RunResult:
    """Single shot using ClaudeSDKClient."""
    options = ClaudeAgentOptions(
        system_prompt=agent.system_prompt,
        allowed_tools=[],
        model=model,
    )

    accumulated_text = ""
    result_message: ResultMessage | None = None

    with span("llm_call", {"iteration": 1}):
        async with ClaudeSDKClient(options=options) as client:
            await client.query(task.prompt)

            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            accumulated_text += block.text
                elif isinstance(message, ResultMessage):
                    result_message = message

    with span("evaluation"):
        evaluation = evaluate_code(accumulated_text, task)

    return RunResult(
        agent=agent.name,
        run_number=run_number,
        correctness=evaluation.correctness,
        iterations_used=1,
        tokens_input=result_message.usage.get("input_tokens", 0) if result_message and result_message.usage else 0,
        tokens_output=result_message.usage.get("output_tokens", 0) if result_message and result_message.usage else 0,
        tokens_total=(result_message.usage.get("input_tokens", 0) + result_message.usage.get("output_tokens", 0))
        if result_message and result_message.usage else 0,
        cost_usd=result_message.total_cost_usd if result_message else None,
        duration_ms=result_message.duration_ms if result_message else 0,
        evaluation=evaluation,
        final_code=accumulated_text,
    )


async def _run_ralph(
    agent: AgentConfig,
    task: TaskConfig,
    run_number: int,
    model: str,
    max_iterations: int,
) -> RunResult:
    """Real Ralph iteration with file persistence.

    Each iteration:
    1. New ClaudeSDKClient session (fresh context)
    2. Claude has file tools (Read, Write, Bash)
    3. Claude reads previous work from file, writes updated code
    4. Harness evaluates the file
    """
    total_input_tokens = 0
    total_output_tokens = 0
    total_cost = 0.0
    total_duration = 0
    final_evaluation = None

    # Create temp workspace for file persistence
    with tempfile.TemporaryDirectory() as workspace:
        workspace_path = Path(workspace)
        code_file = workspace_path / "solution.py"

        # Ralph prompt includes file instructions
        ralph_prompt = f"""Write a Python solution to this problem.

{task.prompt}

Write your solution to: {code_file}

If the file already exists, read it first to see your previous attempt, then improve it.
"""

        for iteration in range(1, max_iterations + 1):
            with span("llm_call", {"iteration": iteration, "type": "ralph"}):
                # Fresh session each iteration - THIS IS KEY
                options = ClaudeAgentOptions(
                    system_prompt=agent.system_prompt,
                    allowed_tools=["Read", "Write", "Bash"],
                    model=model,
                    cwd=str(workspace_path),
                    permission_mode="acceptEdits",
                )

                result_message: ResultMessage | None = None

                async with ClaudeSDKClient(options=options) as client:
                    await client.query(ralph_prompt)

                    async for message in client.receive_response():
                        if isinstance(message, ResultMessage):
                            result_message = message

                if result_message:
                    total_input_tokens += result_message.usage.get("input_tokens", 0) if result_message.usage else 0
                    total_output_tokens += result_message.usage.get("output_tokens", 0) if result_message.usage else 0
                    total_cost += result_message.total_cost_usd or 0
                    total_duration += result_message.duration_ms

            # Evaluate the file content
            with span("evaluation", {"iteration": iteration}):
                if code_file.exists():
                    file_content = code_file.read_text()
                    evaluation = evaluate_code(file_content, task)
                    final_evaluation = evaluation

                    if evaluation.correctness:
                        return RunResult(
                            agent=agent.name,
                            run_number=run_number,
                            correctness=True,
                            iterations_used=iteration,
                            tokens_input=total_input_tokens,
                            tokens_output=total_output_tokens,
                            tokens_total=total_input_tokens + total_output_tokens,
                            cost_usd=total_cost if total_cost > 0 else None,
                            duration_ms=total_duration,
                            evaluation=evaluation,
                            final_code=file_content,
                        )
                else:
                    final_evaluation = EvaluationResult(
                        passed=0, failed=0, total=0, correctness=False,
                        details=[], errors=["No file written"]
                    )

        # Return final result
        final_code = code_file.read_text() if code_file.exists() else ""

    return RunResult(
        agent=agent.name,
        run_number=run_number,
        correctness=final_evaluation.correctness if final_evaluation else False,
        iterations_used=max_iterations,
        tokens_input=total_input_tokens,
        tokens_output=total_output_tokens,
        tokens_total=total_input_tokens + total_output_tokens,
        cost_usd=total_cost if total_cost > 0 else None,
        duration_ms=total_duration,
        evaluation=final_evaluation or EvaluationResult(passed=0, failed=0, total=0, correctness=False, details=[], errors=["No evaluation"]),
        final_code=final_code,
    )


async def _run_self_review(
    agent: AgentConfig,
    task: TaskConfig,
    run_number: int,
    model: str,
    max_iterations: int,
) -> RunResult:
    """Self-review iteration using ClaudeSDKClient with conversation context."""
    options = ClaudeAgentOptions(
        system_prompt=agent.system_prompt,
        allowed_tools=[],
        model=model,
    )

    total_input_tokens = 0
    total_output_tokens = 0
    total_cost = 0.0
    total_duration = 0
    iterations_used = 0
    final_code = ""

    async with ClaudeSDKClient(options=options) as client:
        # Initial request
        with span("llm_call", {"iteration": 1, "type": "initial"}):
            await client.query(task.prompt)
            iterations_used = 1

            accumulated_text = ""
            result_message: ResultMessage | None = None

            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            accumulated_text += block.text
                elif isinstance(message, ResultMessage):
                    result_message = message

            final_code = accumulated_text

            if result_message:
                total_input_tokens += result_message.usage.get("input_tokens", 0) if result_message.usage else 0
                total_output_tokens += result_message.usage.get("output_tokens", 0) if result_message.usage else 0
                total_cost += result_message.total_cost_usd or 0
                total_duration += result_message.duration_ms

        # Iterate with self-review
        for iteration in range(2, max_iterations + 1):
            with span("mid_evaluation", {"iteration": iteration - 1}):
                evaluation = evaluate_code(final_code, task)
                if evaluation.correctness:
                    break

            review_prompt = agent.iteration.review_template or task.review_prompt

            with span("llm_call", {"iteration": iteration, "type": "review"}):
                await client.query(review_prompt)
                iterations_used = iteration

                accumulated_text = ""
                result_message = None

                async for message in client.receive_response():
                    if isinstance(message, AssistantMessage):
                        for block in message.content:
                            if isinstance(block, TextBlock):
                                accumulated_text += block.text
                    elif isinstance(message, ResultMessage):
                        result_message = message

            if "IMPLEMENTATION VERIFIED" in accumulated_text.upper():
                break

            final_code = accumulated_text

            if result_message:
                total_input_tokens += result_message.usage.get("input_tokens", 0) if result_message.usage else 0
                total_output_tokens += result_message.usage.get("output_tokens", 0) if result_message.usage else 0
                total_cost += result_message.total_cost_usd or 0
                total_duration += result_message.duration_ms

    with span("evaluation"):
        evaluation = evaluate_code(final_code, task)

    return RunResult(
        agent=agent.name,
        run_number=run_number,
        correctness=evaluation.correctness,
        iterations_used=iterations_used,
        tokens_input=total_input_tokens,
        tokens_output=total_output_tokens,
        tokens_total=total_input_tokens + total_output_tokens,
        cost_usd=total_cost if total_cost > 0 else None,
        duration_ms=total_duration,
        evaluation=evaluation,
        final_code=final_code,
    )


async def run_experiment(
    agents: list[AgentConfig],
    task: TaskConfig,
    runs_per_agent: int,
    model: str = "sonnet",
    progress_callback: Any | None = None,
) -> ExperimentResults:
    """Run the experiment across all agents."""
    results = ExperimentResults(runs=[], task_name=task.name, model=model)

    for agent in agents:
        for run_num in range(1, runs_per_agent + 1):
            if progress_callback:
                progress_callback(agent.name, run_num, runs_per_agent)

            result = await run_agent(agent, task, run_num, model)
            results.runs.append(result)

    results.compute_summary()
    return results
