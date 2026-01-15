"""Core experiment logic for Ralph Iteration Effect.

Uses Claude Agent SDK to run the experiment conditions:
- single: One API call, no iteration
- ralph-3: Up to 3 iterations with self-review
- ralph-5: Up to 5 iterations with self-review
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from claude_agent_sdk import query, ClaudeSDKClient, ClaudeAgentOptions
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock

from .evaluation import evaluate_code, EvaluationResult


class Condition(str, Enum):
    """Experimental conditions."""

    SINGLE = "single"
    RALPH_3 = "ralph-3"
    RALPH_5 = "ralph-5"


# The task prompt - same for all conditions
TASK_PROMPT = """Write a Python function that checks if a string is a valid palindrome, ignoring case and non-alphanumeric characters.

Requirements:
- Function name: is_palindrome
- Takes a single string argument
- Returns True if the string is a palindrome, False otherwise
- Ignores case (e.g., "Madam" is a palindrome)
- Ignores non-alphanumeric characters (e.g., "A man, a plan, a canal: Panama" is a palindrome)
- Empty string should return True

Provide ONLY the Python function, no tests or examples."""


RALPH_REVIEW_PROMPT = """Review your implementation above. Check for:
1. Does it correctly handle case insensitivity?
2. Does it correctly filter out non-alphanumeric characters?
3. Does it handle edge cases (empty string, single character)?

If you find any issues, provide a corrected implementation.
If the implementation is correct, respond with "IMPLEMENTATION CORRECT" and the final code."""


@dataclass
class RunResult:
    """Result of a single experimental run."""

    condition: str
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
        """Convert to dictionary for JSON serialization."""
        return {
            "condition": self.condition,
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
    summary: dict[str, Any] = field(default_factory=dict)

    def compute_summary(self) -> None:
        """Compute summary statistics per condition."""
        by_condition: dict[str, list[RunResult]] = {}
        for run in self.runs:
            by_condition.setdefault(run.condition, []).append(run)

        self.summary = {}
        for condition, runs in by_condition.items():
            successes = sum(1 for r in runs if r.correctness)
            total_tokens = sum(r.tokens_total for r in runs)
            total_iterations = sum(r.iterations_used for r in runs)

            self.summary[condition] = {
                "runs": len(runs),
                "successes": successes,
                "failures": len(runs) - successes,
                "success_rate": successes / len(runs) if runs else 0,
                "avg_tokens": total_tokens / len(runs) if runs else 0,
                "avg_iterations": total_iterations / len(runs) if runs else 0,
                "total_cost_usd": sum(r.cost_usd or 0 for r in runs),
            }

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "runs": [r.to_dict() for r in self.runs],
            "summary": self.summary,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_runs": len(self.runs),
                "conditions": list(set(r.condition for r in self.runs)),
            },
        }


def extract_code_from_response(text: str) -> str:
    """Extract code from Claude's response."""
    # The response might be just code or wrapped in explanation
    # Return the full text - evaluation.py handles extraction
    return text


async def run_single_condition(run_number: int) -> RunResult:
    """Run single-shot condition: one API call, no iteration."""
    options = ClaudeAgentOptions(
        system_prompt="You are a Python expert. Provide clean, correct code with no explanation.",
        allowed_tools=[],  # No tools - just code generation
    )

    accumulated_text = ""
    result_message: ResultMessage | None = None

    async for message in query(prompt=TASK_PROMPT, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    accumulated_text += block.text
        elif isinstance(message, ResultMessage):
            result_message = message

    # Evaluate the generated code
    evaluation = evaluate_code(accumulated_text)

    return RunResult(
        condition=Condition.SINGLE.value,
        run_number=run_number,
        correctness=evaluation.correctness,
        iterations_used=1,
        tokens_input=result_message.usage.get("input_tokens", 0) if result_message and result_message.usage else 0,
        tokens_output=result_message.usage.get("output_tokens", 0) if result_message and result_message.usage else 0,
        tokens_total=(result_message.usage.get("input_tokens", 0) + result_message.usage.get("output_tokens", 0)) if result_message and result_message.usage else 0,
        cost_usd=result_message.total_cost_usd if result_message else None,
        duration_ms=result_message.duration_ms if result_message else 0,
        evaluation=evaluation,
        final_code=accumulated_text,
    )


async def run_ralph_condition(run_number: int, max_iterations: int) -> RunResult:
    """Run ralph-style condition with self-review iterations.

    Args:
        run_number: Which run this is
        max_iterations: Maximum iterations (3 or 5)
    """
    condition_name = f"ralph-{max_iterations}"

    options = ClaudeAgentOptions(
        system_prompt="You are a Python expert. Provide clean, correct code. When asked to review, be thorough and fix any issues.",
        allowed_tools=[],
    )

    total_input_tokens = 0
    total_output_tokens = 0
    total_cost = 0.0
    total_duration = 0
    iterations_used = 0
    final_code = ""

    async with ClaudeSDKClient(options=options) as client:
        # Initial request
        await client.query(TASK_PROMPT)
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
            # Check if code is already correct
            evaluation = evaluate_code(final_code)
            if evaluation.correctness:
                break  # Early exit - code is correct

            # Request self-review
            await client.query(RALPH_REVIEW_PROMPT)
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

            # Check if Claude says implementation is correct
            if "IMPLEMENTATION CORRECT" in accumulated_text.upper():
                # Extract the code that follows
                parts = accumulated_text.upper().split("IMPLEMENTATION CORRECT")
                if len(parts) > 1:
                    # Use the code after the marker, or keep previous
                    remaining = accumulated_text[accumulated_text.upper().find("IMPLEMENTATION CORRECT") + len("IMPLEMENTATION CORRECT"):]
                    if remaining.strip():
                        final_code = remaining
                break

            # Update final code with the revision
            final_code = accumulated_text

            if result_message:
                total_input_tokens += result_message.usage.get("input_tokens", 0) if result_message.usage else 0
                total_output_tokens += result_message.usage.get("output_tokens", 0) if result_message.usage else 0
                total_cost += result_message.total_cost_usd or 0
                total_duration += result_message.duration_ms

    # Final evaluation
    evaluation = evaluate_code(final_code)

    return RunResult(
        condition=condition_name,
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
    conditions: list[Condition],
    runs_per_condition: int,
    progress_callback: Any | None = None,
) -> ExperimentResults:
    """Run the full experiment.

    Args:
        conditions: Which conditions to run
        runs_per_condition: How many runs per condition
        progress_callback: Optional callback for progress updates

    Returns:
        ExperimentResults with all runs and summary
    """
    results = ExperimentResults(runs=[])

    for condition in conditions:
        for run_num in range(1, runs_per_condition + 1):
            if progress_callback:
                progress_callback(condition.value, run_num, runs_per_condition)

            if condition == Condition.SINGLE:
                result = await run_single_condition(run_num)
            elif condition == Condition.RALPH_3:
                result = await run_ralph_condition(run_num, max_iterations=3)
            elif condition == Condition.RALPH_5:
                result = await run_ralph_condition(run_num, max_iterations=5)
            else:
                raise ValueError(f"Unknown condition: {condition}")

            results.runs.append(result)

    results.compute_summary()
    return results
