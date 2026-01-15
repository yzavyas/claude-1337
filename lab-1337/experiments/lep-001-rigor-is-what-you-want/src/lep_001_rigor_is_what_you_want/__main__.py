"""CLI entrypoint for LEP-001 Ralph Iteration Effect experiment."""

import asyncio
import json
from datetime import datetime
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from .experiment import Condition, run_experiment, ExperimentResults

console = Console()


def display_config(conditions: list[Condition], runs: int) -> None:
    """Display experiment configuration."""
    table = Table(title="Experiment Configuration")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Conditions", ", ".join(c.value for c in conditions))
    table.add_row("Runs per condition", str(runs))
    table.add_row("Total runs", str(len(conditions) * runs))

    console.print(table)


def display_results(results: ExperimentResults) -> None:
    """Display experiment results."""
    console.print("\n")

    # Summary table
    table = Table(title="Results Summary")
    table.add_column("Condition", style="cyan")
    table.add_column("Success Rate", justify="right")
    table.add_column("Avg Tokens", justify="right")
    table.add_column("Avg Iterations", justify="right")
    table.add_column("Total Cost", justify="right")

    for condition, stats in results.summary.items():
        success_rate = f"{stats['success_rate']:.0%}"
        success_style = "green" if stats['success_rate'] >= 0.8 else "yellow" if stats['success_rate'] >= 0.5 else "red"

        table.add_row(
            condition,
            f"[{success_style}]{success_rate}[/{success_style}] ({stats['successes']}/{stats['runs']})",
            f"{stats['avg_tokens']:.0f}",
            f"{stats['avg_iterations']:.1f}",
            f"${stats['total_cost_usd']:.4f}" if stats['total_cost_usd'] else "N/A",
        )

    console.print(table)

    # Individual runs
    runs_table = Table(title="Individual Runs")
    runs_table.add_column("Condition", style="cyan")
    runs_table.add_column("Run", justify="right")
    runs_table.add_column("Correct", justify="center")
    runs_table.add_column("Iterations", justify="right")
    runs_table.add_column("Tokens", justify="right")
    runs_table.add_column("Tests Passed", justify="right")

    for run in results.runs:
        correct_style = "green" if run.correctness else "red"
        correct_symbol = "[green]✓[/green]" if run.correctness else "[red]✗[/red]"

        runs_table.add_row(
            run.condition,
            str(run.run_number),
            correct_symbol,
            str(run.iterations_used),
            str(run.tokens_total),
            f"{run.evaluation.passed}/{run.evaluation.total}",
        )

    console.print(runs_table)


def save_results(results: ExperimentResults, output_path: Path) -> None:
    """Save results to JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results.to_dict(), indent=2))
    console.print(f"\n[dim]Results saved to: {output_path}[/dim]")


@click.command()
@click.option("--runs", "-r", default=5, help="Number of runs per condition")
@click.option("--condition", "-c", type=click.Choice(["single", "ralph-3", "ralph-5", "all"]), default="all", help="Which condition to run")
@click.option("--output", "-o", type=click.Path(), help="Output file path (default: results/<timestamp>.json)")
@click.option("--dry-run", is_flag=True, help="Show configuration without running")
def main(runs: int, condition: str, output: str | None, dry_run: bool) -> None:
    """Run the Ralph Iteration Effect experiment.

    LEP-001: Prove that methodology effectiveness can be measured.

    Tests whether iteration improves outcomes by comparing:
    - single: One API call, no iteration
    - ralph-3: Up to 3 iterations with self-review
    - ralph-5: Up to 5 iterations with self-review
    """
    console.print(Panel.fit(
        "[bold cyan]LEP-001: Rigor is What You Want[/bold cyan]\n"
        "[dim]Ralph Iteration Effect Experiment[/dim]",
        border_style="cyan"
    ))

    # Determine conditions
    if condition == "all":
        conditions = [Condition.SINGLE, Condition.RALPH_3, Condition.RALPH_5]
    else:
        conditions = [Condition(condition)]

    display_config(conditions, runs)

    if dry_run:
        console.print("\n[yellow]Dry run - exiting without running experiment[/yellow]")
        return

    # Output path
    if output:
        output_path = Path(output)
    else:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = Path(__file__).parent.parent.parent.parent / "results" / f"run-{timestamp}.json"

    # Run experiment
    console.print("\n[bold]Running experiment...[/bold]\n")

    def progress_callback(cond: str, run_num: int, total: int) -> None:
        console.print(f"  [cyan]{cond}[/cyan] run {run_num}/{total}...")

    try:
        results = asyncio.run(run_experiment(
            conditions=conditions,
            runs_per_condition=runs,
            progress_callback=progress_callback,
        ))

        display_results(results)
        save_results(results, output_path)

        # Final verdict
        console.print("\n")
        if results.summary:
            single_rate = results.summary.get("single", {}).get("success_rate", 0)
            ralph3_rate = results.summary.get("ralph-3", {}).get("success_rate", 0)
            ralph5_rate = results.summary.get("ralph-5", {}).get("success_rate", 0)

            if ralph3_rate > single_rate or ralph5_rate > single_rate:
                console.print("[green bold]Signal detected:[/green bold] Iteration appears to improve outcomes")
            elif ralph3_rate < single_rate or ralph5_rate < single_rate:
                console.print("[yellow bold]Signal detected:[/yellow bold] Iteration may not help (or hurts)")
            else:
                console.print("[dim]No clear signal between conditions[/dim]")

    except KeyboardInterrupt:
        console.print("\n[yellow]Experiment interrupted by user[/yellow]")
        raise SystemExit(1)
    except Exception as e:
        console.print(f"\n[red]Error running experiment: {e}[/red]")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
