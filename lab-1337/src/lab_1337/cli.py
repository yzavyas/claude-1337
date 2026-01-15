"""CLI for 1337 Experiments Lab."""

import json
import subprocess
from datetime import date
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from lab_1337.elc.proposals import proposal, get_lep, EXPERIMENTS_DIR
from lab_1337.elc.implementations import imp, get_imp

console = Console()

ROOT_DIR = Path(__file__).parent.parent.parent


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
            name = exp_dir.name
            readme = exp_dir / "README.md"
            description = ""
            if readme.exists():
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


# Register ELC subcommand groups
main.add_command(proposal)
main.add_command(imp)


# Experiment commands
@click.group("experiment")
def experiment():
    """Manage experiments."""
    pass


main.add_command(experiment)


@experiment.command("new")
@click.argument("lep_number")
def new_experiment(lep_number: str):
    """Scaffold a new experiment from an accepted LEP."""
    lep = get_lep(lep_number)
    if not lep:
        console.print(f"[red]LEP-{lep_number} not found[/red]")
        raise SystemExit(1)

    # Check IMP exists
    imp_item = get_imp(lep.number)
    if not imp_item:
        console.print(f"[yellow]Warning: No IMP found for LEP-{lep.number}[/yellow]")
        console.print("[dim]Consider creating one: lab-1337 imp new {lep.number}[/dim]")

    # Check experiment doesn't already exist
    exp_dir = EXPERIMENTS_DIR / lep.experiment_dirname
    if exp_dir.exists():
        console.print(f"[yellow]Experiment already exists:[/yellow] {exp_dir}")
        raise SystemExit(1)

    # Scaffold experiment
    exp_dir.mkdir(parents=True)
    src_dir = exp_dir / "src" / lep.experiment_dirname.replace("-", "_")
    src_dir.mkdir(parents=True)

    # Create pyproject.toml
    pyproject_content = f'''[project]
name = "{lep.experiment_dirname}"
version = "0.1.0"
description = "{lep.title}"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "anthropic>=0.40.0",
    "pydantic>=2.0.0",
    "rich>=13.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/{lep.experiment_dirname.replace("-", "_")}"]
'''
    (exp_dir / "pyproject.toml").write_text(pyproject_content)

    # Create README
    readme_content = f'''# LEP-{lep.number}: {lep.title}

> From [LEP-{lep.number}](../../proposals/{lep.filename})

## Hypothesis

<!-- From the LEP -->

## Design

<!-- From the IMP -->

## Run

```bash
# From experiment directory
uv run python -m {lep.experiment_dirname.replace("-", "_")}

# Or via lab CLI
lab-1337 run {lep.experiment_dirname}
```

## Results

<!-- After running -->
'''
    (exp_dir / "README.md").write_text(readme_content)

    # Create __init__.py
    (src_dir / "__init__.py").write_text(f'"""{lep.title}"""\n\n__version__ = "0.1.0"\n')

    # Create __main__.py placeholder
    main_content = f'''"""Run the {lep.title} experiment."""

import click
from rich.console import Console

console = Console()


@click.command()
@click.option("--runs", default=5, help="Runs per condition")
@click.option("--dry-run", is_flag=True, help="Show config without running")
def main(runs: int, dry_run: bool):
    """Run the experiment."""
    console.print("[bold cyan]{lep.title}[/bold cyan]")
    console.print("[dim]LEP-{lep.number}[/dim]\\n")

    if dry_run:
        console.print("[yellow]Dry run - exiting[/yellow]")
        return

    # TODO: Implement experiment
    console.print("[yellow]Experiment not yet implemented[/yellow]")


if __name__ == "__main__":
    main()
'''
    (src_dir / "__main__.py").write_text(main_content)

    console.print(f"[green]Created experiment:[/green] {exp_dir.name}")
    console.print(f"[dim]Linked to: LEP-{lep.number}, IMP-{lep.number if imp_item else 'missing'}[/dim]")
    console.print(f"\n[cyan]Next steps:[/cyan]")
    console.print(f"  1. Edit {exp_dir / 'README.md'}")
    console.print(f"  2. Implement {src_dir / '__main__.py'}")
    console.print(f"  3. Run: lab-1337 run {lep.experiment_dirname}")


@experiment.command("list")
def list_experiments_cmd():
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
@click.argument("experiment_name")
@click.option("--config", "-c", help="Path to config file")
@click.option("--dry-run", is_flag=True, help="Show what would run without executing")
def run(experiment_name: str, config: str | None, dry_run: bool):
    """Run an experiment."""
    experiments = {e["name"]: e for e in get_experiments()}

    if experiment_name not in experiments:
        console.print(f"[red]Experiment not found: {experiment_name}[/red]")
        console.print(f"Available: {', '.join(experiments.keys())}")
        raise SystemExit(1)

    exp = experiments[experiment_name]
    exp_path = exp["path"]

    console.print(f"[cyan]Running experiment:[/cyan] {experiment_name}")
    console.print(f"[dim]Path: {exp_path}[/dim]")

    if dry_run:
        console.print("[yellow]Dry run - would execute experiment[/yellow]")
        return

    cmd = ["uv", "run", "python", "-m", exp_path.name.replace("-", "_")]
    if config:
        cmd.extend(["--config", config])

    try:
        subprocess.run(cmd, cwd=exp_path, check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Experiment failed with exit code {e.returncode}[/red]")
        raise SystemExit(e.returncode)


@main.command()
@click.argument("experiment_name")
def results(experiment_name: str):
    """View results for an experiment."""
    results_dir = ROOT_DIR / "results" / experiment_name

    if not results_dir.exists():
        console.print(f"[yellow]No results found for: {experiment_name}[/yellow]")
        console.print(f"Run the experiment first with: lab-1337 run {experiment_name}")
        return

    result_files = sorted(results_dir.glob("*.json"), reverse=True)
    if not result_files:
        console.print("[yellow]No result files found.[/yellow]")
        return

    console.print(f"[cyan]Results for:[/cyan] {experiment_name}")
    console.print(f"[dim]Found {len(result_files)} result file(s)[/dim]")

    latest = result_files[0]
    console.print(f"\n[bold]Latest: {latest.name}[/bold]")

    data = json.loads(latest.read_text())
    console.print_json(data=data)


# Status overview
@main.command("status")
def status_overview():
    """Show overall lab status."""
    from lab_1337.elc.proposals import get_all_leps
    from lab_1337.elc.implementations import get_all_imps
    from lab_1337.elc.models import EnhancementStatus, status_color

    leps = get_all_leps()
    imps = get_all_imps()
    experiments = get_experiments()

    console.print("\n[bold]1337 Experiments Lab Status[/bold]\n")

    # LEP summary
    lep_by_status = {}
    for lep in leps:
        lep_by_status.setdefault(lep.status, []).append(lep)

    console.print("[cyan]Proposals (LEPs)[/cyan]")
    for status in EnhancementStatus:
        count = len(lep_by_status.get(status, []))
        if count > 0:
            console.print(f"  [{status_color(status)}]{status.value}[/{status_color(status)}]: {count}")

    # IMP summary
    console.print(f"\n[cyan]Implementation Plans (IMPs)[/cyan]: {len(imps)}")

    # Experiment summary
    console.print(f"\n[cyan]Experiments[/cyan]: {len(experiments)}")

    # Show pending actions
    console.print("\n[bold]Pending Actions[/bold]")
    pending = []

    for lep in leps:
        if lep.status == EnhancementStatus.ACCEPTED and not lep.has_imp(ROOT_DIR / "implementations"):
            pending.append(f"  LEP-{lep.number} accepted → create IMP: lab-1337 imp new {lep.number}")
        if lep.status == EnhancementStatus.ACCEPTED and not lep.has_experiment(EXPERIMENTS_DIR):
            imp_exists = any(i.lep_ref == lep.number for i in imps)
            if imp_exists:
                pending.append(f"  LEP-{lep.number} has IMP → scaffold experiment: lab-1337 experiment new {lep.number}")

    if pending:
        for p in pending:
            console.print(p)
    else:
        console.print("  [dim]None[/dim]")


if __name__ == "__main__":
    main()
