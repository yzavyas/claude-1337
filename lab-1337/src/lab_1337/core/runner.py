"""Experiment runner with progress tracking."""

import asyncio
import json
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from lab_1337.core.experiment import Experiment, ExperimentResult

console = Console()


class Runner:
    """Runs experiments with progress tracking and result persistence."""

    def __init__(self, experiment: Experiment):
        self.experiment = experiment
        self.config = experiment.config

    async def run(self) -> ExperimentResult:
        """Run all conditions and aggregate results."""
        result = ExperimentResult(
            config=self.config,
            started_at=datetime.now(),
        )

        conditions = list(self.config.conditions.items())
        total_runs = len(conditions) * self.config.runs_per_condition

        console.print(f"\n[bold cyan]Experiment:[/bold cyan] {self.config.name}")
        console.print(f"[dim]{self.config.description}[/dim]\n")
        console.print(f"Conditions: {len(conditions)}")
        console.print(f"Runs per condition: {self.config.runs_per_condition}")
        console.print(f"Total runs: {total_runs}\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Running experiment...", total=total_runs)

            for condition_name, condition_config in conditions:
                for run_idx in range(self.config.runs_per_condition):
                    progress.update(
                        task,
                        description=f"[cyan]{condition_name}[/cyan] run {run_idx + 1}/{self.config.runs_per_condition}",
                    )

                    try:
                        condition_result = await self.experiment.run_condition(
                            condition_name, condition_config, run_idx
                        )
                        result.add_result(condition_result)

                        status = "[green]pass[/green]" if condition_result.success else "[red]fail[/red]"
                        console.print(
                            f"  {condition_name} #{run_idx + 1}: {status} "
                            f"[dim]({condition_result.tokens_used} tokens, {condition_result.duration_ms}ms)[/dim]"
                        )

                    except Exception as e:
                        console.print(f"  [red]Error in {condition_name} #{run_idx + 1}: {e}[/red]")
                        from lab_1337.core.experiment import ConditionResult
                        result.add_result(
                            ConditionResult(
                                condition=condition_name,
                                run_index=run_idx,
                                success=False,
                                metrics={},
                                error=str(e),
                            )
                        )

                    progress.advance(task)

        result.completed_at = datetime.now()

        # Save results
        self._save_results(result)

        # Print summary
        self._print_summary(result)

        return result

    def _save_results(self, result: ExperimentResult):
        """Save results to JSON file."""
        output_dir = self.config.output_dir
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            timestamp = result.started_at.strftime("%Y%m%d-%H%M%S")
            filename = f"{self.config.name}-{timestamp}.json"
            filepath = output_dir / filename

            filepath.write_text(json.dumps(result.to_dict(), indent=2))
            console.print(f"\n[dim]Results saved to: {filepath}[/dim]")

    def _print_summary(self, result: ExperimentResult):
        """Print summary table."""
        from rich.table import Table

        console.print("\n[bold]Summary[/bold]")

        table = Table()
        table.add_column("Condition", style="cyan")
        table.add_column("Success Rate", justify="right")
        table.add_column("Avg Tokens", justify="right")
        table.add_column("Avg Duration", justify="right")

        summary = result.summary()
        for condition, stats in summary.items():
            rate = f"{stats['success_rate']:.1%}"
            tokens = f"{stats['avg_tokens']:.0f}"
            duration = f"{stats['avg_duration_ms']:.0f}ms"
            table.add_row(condition, rate, tokens, duration)

        console.print(table)
