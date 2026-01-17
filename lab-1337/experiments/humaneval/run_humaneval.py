"""HumanEval benchmark runner for comparing single-shot vs ralph-style iteration.

This uses the official HumanEval benchmark (164 Python problems) to test whether
iteration with test feedback improves outcomes.

Key difference from broken lep-001 experiment:
- Claude has Bash access to run tests
- Ralph-style iteration shows Claude the test failures
- We measure actual pass@1 on a real benchmark
"""

import asyncio
import json
import tempfile
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from datasets import load_dataset
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

console = Console()


@dataclass
class ProblemResult:
    """Result for a single HumanEval problem."""
    task_id: str
    strategy: str
    passed: bool
    iterations: int
    tokens: int
    duration_ms: int
    error: str | None = None


@dataclass
class BenchmarkResults:
    """Aggregated benchmark results."""
    results: list[ProblemResult] = field(default_factory=list)
    
    def summary(self) -> dict[str, Any]:
        by_strategy: dict[str, list[ProblemResult]] = {}
        for r in self.results:
            by_strategy.setdefault(r.strategy, []).append(r)
        
        summary = {}
        for strategy, results in by_strategy.items():
            passed = sum(1 for r in results if r.passed)
            summary[strategy] = {
                "total": len(results),
                "passed": passed,
                "pass_rate": passed / len(results) if results else 0,
                "avg_tokens": sum(r.tokens for r in results) / len(results) if results else 0,
                "avg_iterations": sum(r.iterations for r in results) / len(results) if results else 0,
            }
        return summary


def run_tests(code: str, test_code: str, entry_point: str, timeout: int = 10) -> tuple[bool, str]:
    """Run HumanEval tests against code. Returns (passed, output)."""
    # Combine solution with test code
    full_code = f"{code}\n\n{test_code}\n\ncheck({entry_point})"
    
    try:
        result = subprocess.run(
            ["python", "-c", full_code],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            return True, "All tests passed"
        else:
            return False, result.stderr or result.stdout
    except subprocess.TimeoutExpired:
        return False, "Timeout: execution took too long"
    except Exception as e:
        return False, f"Execution error: {e}"


async def run_single_shot(
    problem: dict,
    model: str = "sonnet",
) -> ProblemResult:
    """Single shot - one attempt, no iteration."""
    task_id = problem["task_id"]
    prompt = problem["prompt"]
    entry_point = problem["entry_point"]
    test_code = problem["test"]
    
    system_prompt = """You are solving a Python coding problem.
Write ONLY the Python function - no explanations, no markdown, no tests.
Output the raw Python code that can be executed directly."""
    
    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        allowed_tools=[],
        model=model,
    )
    
    accumulated_text = ""
    result_message: ResultMessage | None = None
    
    async with ClaudeSDKClient(options=options) as client:
        await client.query(f"Implement this function:\n\n{prompt}")
        
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        accumulated_text += block.text
            elif isinstance(message, ResultMessage):
                result_message = message
    
    # Extract code (remove markdown if present)
    code = accumulated_text.strip()
    if code.startswith("```python"):
        code = code[9:]
    if code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]
    code = code.strip()
    
    passed, _ = run_tests(code, test_code, entry_point)
    
    return ProblemResult(
        task_id=task_id,
        strategy="single-shot",
        passed=passed,
        iterations=1,
        tokens=result_message.usage.get("input_tokens", 0) + result_message.usage.get("output_tokens", 0) if result_message and result_message.usage else 0,
        duration_ms=result_message.duration_ms if result_message else 0,
    )


async def run_ralph_style(
    problem: dict,
    model: str = "sonnet",
    max_iterations: int = 3,
) -> ProblemResult:
    """Ralph-style iteration with test feedback.

    CORRECT: One ClaudeSDKClient session, multiple queries.
    Claude maintains full context and sees test failures in conversation.
    """
    task_id = problem["task_id"]
    prompt = problem["prompt"]
    entry_point = problem["entry_point"]
    test_code = problem["test"]

    total_tokens = 0
    total_duration = 0
    iterations_used = 0
    last_error = ""

    with tempfile.TemporaryDirectory() as workspace:
        workspace_path = Path(workspace)
        solution_file = workspace_path / "solution.py"

        system_prompt = """You are solving a Python coding problem.
Write the function to solution.py. I'll run tests and tell you the result.
If tests fail, I'll show you the error - fix it."""

        options = ClaudeAgentOptions(
            system_prompt=system_prompt,
            allowed_tools=["Read", "Write"],
            model=model,
            cwd=str(workspace_path),
            permission_mode="acceptEdits",
        )

        initial_prompt = f"""Implement this Python function and save it to solution.py:

{prompt}

Write the function to solution.py. I will run the tests."""

        # ONE client - loop INSIDE the session
        async with ClaudeSDKClient(options=options) as client:
            for iteration in range(1, max_iterations + 1):
                iterations_used = iteration

                # First iteration: initial prompt. Later: show test failure
                if iteration == 1:
                    await client.query(initial_prompt)
                else:
                    await client.query(f"Tests failed:\n\n{last_error}\n\nFix solution.py and try again.")

                result_message: ResultMessage | None = None
                async for message in client.receive_response():
                    if isinstance(message, ResultMessage):
                        result_message = message

                if result_message:
                    total_tokens += (result_message.usage.get("input_tokens", 0) +
                                   result_message.usage.get("output_tokens", 0)) if result_message.usage else 0
                    total_duration += result_message.duration_ms

                # Run tests externally
                if solution_file.exists():
                    code = solution_file.read_text()
                    passed, last_error = run_tests(code, test_code, entry_point)

                    if passed:
                        return ProblemResult(
                            task_id=task_id,
                            strategy="ralph-style",
                            passed=True,
                            iterations=iterations_used,
                            tokens=total_tokens,
                            duration_ms=total_duration,
                        )
                else:
                    last_error = "No solution.py file created"

        # Max iterations reached
        passed = False
        if solution_file.exists():
            code = solution_file.read_text()
            passed, _ = run_tests(code, test_code, entry_point)

        return ProblemResult(
            task_id=task_id,
            strategy="ralph-style",
            passed=passed,
            iterations=iterations_used,
            tokens=total_tokens,
            duration_ms=total_duration,
        )


async def run_benchmark(
    num_problems: int = 10,
    model: str = "sonnet",
    max_iterations: int = 3,
    start_from: int = 0,
) -> BenchmarkResults:
    """Run HumanEval benchmark comparing strategies."""

    console.print("[cyan]Loading HumanEval dataset...[/cyan]")
    dataset = load_dataset("openai/openai_humaneval", split="test")

    # Take subset for testing (with optional offset for harder problems)
    all_problems = list(dataset)
    problems = all_problems[start_from:start_from + num_problems]
    console.print(f"[cyan]Running problems {start_from}-{start_from + len(problems)} with model={model}[/cyan]")
    
    results = BenchmarkResults()
    
    with Progress() as progress:
        task = progress.add_task("Running benchmark...", total=len(problems) * 2)
        
        for problem in problems:
            task_id = problem["task_id"]
            
            # Single shot
            progress.update(task, description=f"[yellow]single-shot: {task_id}[/yellow]")
            try:
                result = await run_single_shot(problem, model)
                results.results.append(result)
            except Exception as e:
                results.results.append(ProblemResult(
                    task_id=task_id, strategy="single-shot",
                    passed=False, iterations=1, tokens=0, duration_ms=0, error=str(e)
                ))
            progress.advance(task)
            
            # Ralph style
            progress.update(task, description=f"[green]ralph-style: {task_id}[/green]")
            try:
                result = await run_ralph_style(problem, model, max_iterations)
                results.results.append(result)
            except Exception as e:
                results.results.append(ProblemResult(
                    task_id=task_id, strategy="ralph-style",
                    passed=False, iterations=1, tokens=0, duration_ms=0, error=str(e)
                ))
            progress.advance(task)
    
    return results


def display_results(results: BenchmarkResults):
    """Display results in a table."""
    summary = results.summary()
    
    table = Table(title="HumanEval Results")
    table.add_column("Strategy")
    table.add_column("Pass Rate", justify="right")
    table.add_column("Avg Tokens", justify="right")
    table.add_column("Avg Iterations", justify="right")
    
    for strategy, stats in summary.items():
        table.add_row(
            strategy,
            f"{stats['pass_rate']:.1%} ({stats['passed']}/{stats['total']})",
            f"{stats['avg_tokens']:.0f}",
            f"{stats['avg_iterations']:.1f}",
        )
    
    console.print(table)


async def main():
    import argparse
    parser = argparse.ArgumentParser(description="HumanEval benchmark")
    parser.add_argument("-n", "--num-problems", type=int, default=10, help="Number of problems")
    parser.add_argument("-s", "--start-from", type=int, default=0, help="Start from problem N (0-163)")
    parser.add_argument("-m", "--model", default="sonnet", help="Model to use")
    parser.add_argument("-i", "--max-iterations", type=int, default=3, help="Max iterations for ralph")
    parser.add_argument("-o", "--output", help="Output JSON file")
    args = parser.parse_args()

    results = await run_benchmark(
        num_problems=args.num_problems,
        model=args.model,
        max_iterations=args.max_iterations,
        start_from=args.start_from,
    )
    
    display_results(results)
    
    if args.output:
        output = {
            "timestamp": datetime.now().isoformat(),
            "model": args.model,
            "num_problems": args.num_problems,
            "start_from": args.start_from,
            "problem_range": f"HumanEval/{args.start_from}-{args.start_from + args.num_problems - 1}",
            "max_iterations": args.max_iterations,
            "summary": results.summary(),
            "results": [
                {
                    "task_id": r.task_id,
                    "strategy": r.strategy,
                    "passed": r.passed,
                    "iterations": r.iterations,
                    "tokens": r.tokens,
                    "duration_ms": r.duration_ms,
                    "error": r.error,
                }
                for r in results.results
            ],
        }
        Path(args.output).write_text(json.dumps(output, indent=2))
        console.print(f"[green]Results saved to {args.output}[/green]")


if __name__ == "__main__":
    asyncio.run(main())
