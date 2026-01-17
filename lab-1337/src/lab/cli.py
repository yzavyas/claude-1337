"""Lab 1337 CLI - Config-driven experiment runner."""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path

import click
import yaml
from rich.console import Console
from rich.table import Table
from rich.logging import RichHandler

from .config import load_task, load_agent
from .experiment import run_experiment

console = Console()
log = logging.getLogger("lab-1337")


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def main(verbose: bool):
    """Lab 1337 - Rigorous experiments."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(console=console, show_path=False)],
    )


@main.command()
@click.option("-c", "--config", "config_path", required=True, type=click.Path(exists=True))
def run(config_path: str):
    """Run experiment from config file."""
    config_file = Path(config_path)
    exp_dir = config_file.parent.parent  # scenarios/ -> experiment/

    with open(config_file) as f:
        config = yaml.safe_load(f)

    log.info(f"Running: {config.get('name', config_file.stem)}")
    log.debug(f"Config: {config_file}")

    # Load tasks and agents
    tasks_dir = exp_dir / "tasks"
    agents_dir = exp_dir / "agents"
    results_dir = exp_dir / config.get("results_dir", "results")

    task_names = config.get("tasks", [])
    agent_names = config.get("agents", [])
    model = config.get("model", "sonnet")
    runs = config.get("runs_per_agent", 3)

    # Run each task
    for task_name in task_names:
        task_config = load_task(tasks_dir / f"{task_name}.yaml")
        agents = [load_agent(agents_dir / f"{a}.md") for a in agent_names]

        log.info(f"Task: {task_name} | Model: {model} | Agents: {agent_names}")

        results = asyncio.run(
            run_experiment(
                agents=agents,
                task=task_config,
                runs_per_agent=runs,
                model=model,
                progress_callback=lambda a, r, t: log.debug(f"  {a} run {r}/{t}"),
            )
        )

        # Display results
        table = Table(title=f"{task_name} Results")
        table.add_column("Agent")
        table.add_column("Success", justify="right")
        table.add_column("Tokens", justify="right")

        for agent, stats in results.summary.items():
            rate = f"{stats['success_rate']:.0%}"
            table.add_row(agent, f"{rate} ({stats['successes']}/{stats['runs']})", f"{stats['avg_tokens']:.0f}")

        console.print(table)

        # Save results
        results_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = results_dir / f"{task_name}-{model}-{timestamp}.json"
        output_path.write_text(json.dumps(results.to_dict(), indent=2))
        log.info(f"Saved: {output_path}")


@main.command()
@click.argument("results_file", type=click.Path(exists=True))
@click.option("--model", default="gpt-4o-mini", help="Verifier model")
def verify(results_file: str, model: str):
    """Verify experiment claims with Strawberry.

    Extracts claims from results, verifies each against evidence.
    Produces analysis.md with verified/uncertain claims and citations.
    """
    from .analyst import analyze_results

    results_path = Path(results_file)
    log.info(f"Verifying: {results_path}")

    report = analyze_results(
        results_path=results_path,
        verify=True,
        verifier_model=model,
    )

    # Summary
    verified = sum(1 for c in report.claims if c.verified)
    total = len(report.claims)
    console.print(f"\n[green]Verification complete:[/green] {verified}/{total} claims verified")
    console.print(f"[dim]Run 'lab-1337 report {results_path.stem}-analysis.md' to generate HTML[/dim]")


@main.command()
@click.argument("analysis_file", type=click.Path(exists=True))
@click.option("-o", "--output", "output_path", type=click.Path(), help="Output HTML path")
def report(analysis_file: str, output_path: str | None):
    """Generate HTML report from analysis markdown.

    Takes the analysis.md produced by 'analyze' and generates a
    polished HTML report using experience-designer principles.
    """
    from .reporter import generate_report

    analysis_path = Path(analysis_file)
    out = Path(output_path) if output_path else None

    log.info(f"Generating report from: {analysis_path}")

    html_path = generate_report(
        analysis_path=analysis_path,
        output_path=out,
    )

    console.print(f"\n[green]Report ready:[/green] {html_path}")


@main.command()
def ls():
    """List experiments."""
    lab_root = Path(__file__).parent.parent.parent
    exp_dir = lab_root / "experiments"

    if not exp_dir.exists():
        console.print("[yellow]No experiments found.[/yellow]")
        return

    for exp in sorted(exp_dir.iterdir()):
        if exp.is_dir() and not exp.name.startswith("."):
            scenarios = list((exp / "scenarios").glob("*.yaml")) if (exp / "scenarios").exists() else []
            console.print(f"[cyan]{exp.name}[/cyan]: {len(scenarios)} scenarios")
            for s in scenarios:
                console.print(f"  - {s.name}")


if __name__ == "__main__":
    main()
