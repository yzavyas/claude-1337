"""CLI for 1337 Experiments Lab."""

import importlib
import subprocess
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from lab_1337.proposals import proposal

console = Console()

EXPERIMENTS_DIR = Path(__file__).parent.parent.parent / "experiments"


def get_experiments() -> list[dict]:
    """Discover available experiments."""
    experiments = []
    if not EXPERIMENTS_DIR.exists():
        return experiments

    for exp_dir in EXPERIMENTS_DIR.iterdir():
        if not exp_dir.is_dir():
            continue
        pyproject = exp_dir / "pyproject.toml"
        if pyproject.exists():
            # Parse basic info from pyproject.toml
            name = exp_dir.name
            readme = exp_dir / "README.md"
            description = ""
            if readme.exists():
                # Get first non-empty, non-header line
                for line in readme.read_text().splitlines():
                    line = line.strip()
                    if line and not line.startswith("#"):
                        description = line[:80]
                        break
            experiments.append({"name": name, "path": exp_dir, "description": description})

    return experiments


@click.group()
@click.version_option()
def main():
    """1337 Experiments Lab - Rigorous experiments for the agentic era."""
    pass


# Register subcommand groups
main.add_command(proposal)


@main.command("experiments")
def list_experiments():
    """List available experiments."""
    experiments = get_experiments()

    if not experiments:
        console.print("[yellow]No experiments found.[/yellow]")
        console.print(f"Add experiments to: {EXPERIMENTS_DIR}")
        return

    table = Table(title="Available Experiments")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")

    for exp in experiments:
        table.add_row(exp["name"], exp["description"])

    console.print(table)


@main.command()
@click.argument("experiment")
@click.option("--config", "-c", help="Path to config file")
@click.option("--dry-run", is_flag=True, help="Show what would run without executing")
def run(experiment: str, config: str | None, dry_run: bool):
    """Run an experiment."""
    experiments = {e["name"]: e for e in get_experiments()}

    if experiment not in experiments:
        console.print(f"[red]Experiment not found: {experiment}[/red]")
        console.print(f"Available: {', '.join(experiments.keys())}")
        raise SystemExit(1)

    exp = experiments[experiment]
    exp_path = exp["path"]

    console.print(f"[cyan]Running experiment:[/cyan] {experiment}")
    console.print(f"[dim]Path: {exp_path}[/dim]")

    if dry_run:
        console.print("[yellow]Dry run - would execute experiment[/yellow]")
        return

    # Run the experiment using uv
    cmd = ["uv", "run", "python", "-m", exp_path.name.replace("-", "_")]
    if config:
        cmd.extend(["--config", config])

    try:
        subprocess.run(cmd, cwd=exp_path, check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Experiment failed with exit code {e.returncode}[/red]")
        raise SystemExit(e.returncode)


@main.command()
@click.argument("experiment")
def results(experiment: str):
    """View results for an experiment."""
    results_dir = Path(__file__).parent.parent.parent / "results" / experiment

    if not results_dir.exists():
        console.print(f"[yellow]No results found for: {experiment}[/yellow]")
        console.print("Run the experiment first with: lab-1337 run {experiment}")
        return

    # Find most recent results
    result_files = sorted(results_dir.glob("*.json"), reverse=True)
    if not result_files:
        console.print("[yellow]No result files found.[/yellow]")
        return

    console.print(f"[cyan]Results for:[/cyan] {experiment}")
    console.print(f"[dim]Found {len(result_files)} result file(s)[/dim]")

    # Display most recent
    import json

    latest = result_files[0]
    console.print(f"\n[bold]Latest: {latest.name}[/bold]")

    data = json.loads(latest.read_text())
    console.print_json(data=data)


if __name__ == "__main__":
    main()
