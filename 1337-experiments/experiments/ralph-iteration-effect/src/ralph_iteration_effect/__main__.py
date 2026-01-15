"""Run the Ralph Iteration Effect experiment."""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table

from ralph_iteration_effect.experiment import RalphExperiment

console = Console()


@click.command()
@click.option("--runs", default=5, help="Runs per condition")
@click.option("--model", default="claude-sonnet-4-20250514", help="Model to use")
@click.option("--output", "-o", type=click.Path(), help="Output file for results")
@click.option("--dry-run", is_flag=True, help="Show config without running")
def main(runs: int, model: str, output: str | None, dry_run: bool):
    """Run the Ralph Iteration Effect experiment."""

    conditions = {
        "single": {"max_iterations": 1},
        "ralph-3": {"max_iterations": 3},
        "ralph-5": {"max_iterations": 5},
    }

    console.print("\n[bold cyan]Ralph Iteration Effect Experiment[/bold cyan]")
    console.print("Does iteration improve outcomes?\n")

    console.print(f"Model: {model}")
    console.print(f"Runs per condition: {runs}")
    console.print(f"Conditions: {', '.join(conditions.keys())}")
    console.print(f"Total runs: {len(conditions) * runs}\n")

    if dry_run:
        console.print("[yellow]Dry run - exiting[/yellow]")
        return

    experiment = RalphExperiment(model=model)
    results = []

    total = len(conditions) * runs

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Running...", total=total)

        for condition, config in conditions.items():
            for run_idx in range(runs):
                progress.update(task, description=f"[cyan]{condition}[/cyan] run {run_idx + 1}/{runs}")

                try:
                    if config["max_iterations"] == 1:
                        result = experiment.run_single()
                    else:
                        result = experiment.run_ralph(config["max_iterations"])

                    results.append({
                        "condition": condition,
                        "run": run_idx,
                        "completed": result.completed,
                        "iterations_used": result.iterations_used,
                        "tokens_total": result.tokens_total,
                        "duration_ms": result.duration_ms,
                    })

                    status = "[green]pass[/green]" if result.completed else "[red]fail[/red]"
                    console.print(
                        f"  {condition} #{run_idx + 1}: {status} "
                        f"[dim]({result.iterations_used} iter, {result.tokens_total} tok)[/dim]"
                    )

                except Exception as e:
                    console.print(f"  [red]Error: {e}[/red]")
                    results.append({
                        "condition": condition,
                        "run": run_idx,
                        "completed": False,
                        "error": str(e),
                    })

                progress.advance(task)

    # Summary
    console.print("\n[bold]Summary[/bold]")

    table = Table()
    table.add_column("Condition", style="cyan")
    table.add_column("Success Rate", justify="right")
    table.add_column("Avg Iterations", justify="right")
    table.add_column("Avg Tokens", justify="right")

    for condition in conditions:
        cond_results = [r for r in results if r["condition"] == condition]
        if not cond_results:
            continue

        successes = sum(1 for r in cond_results if r.get("completed", False))
        rate = successes / len(cond_results)

        avg_iter = sum(r.get("iterations_used", 0) for r in cond_results) / len(cond_results)
        avg_tokens = sum(r.get("tokens_total", 0) for r in cond_results) / len(cond_results)

        rate_str = f"{rate:.0%}"
        rate_style = "green" if rate >= 0.8 else "yellow" if rate >= 0.5 else "red"

        table.add_row(
            condition,
            f"[{rate_style}]{rate_str}[/{rate_style}]",
            f"{avg_iter:.1f}",
            f"{avg_tokens:.0f}",
        )

    console.print(table)

    # Save results
    output_data = {
        "experiment": "ralph-iteration-effect",
        "model": model,
        "runs_per_condition": runs,
        "timestamp": datetime.now().isoformat(),
        "results": results,
    }

    if output:
        output_path = Path(output)
    else:
        output_path = Path("results") / f"ralph-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output_data, indent=2))
    console.print(f"\n[dim]Results saved to: {output_path}[/dim]")


if __name__ == "__main__":
    main()
