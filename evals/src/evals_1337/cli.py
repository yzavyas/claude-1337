"""CLI for evals-1337."""

import asyncio
import json
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from .core.models import Expectation
from .targets.skills import (
    SkillTestCase,
    SkillTestSpec,
    discover_skills,
    run_skill_test,
)
from .metrics.classification import format_confusion_matrix

console = Console()

# Default plugins directory (relative to repo root)
DEFAULT_PLUGINS = Path(__file__).parent.parent.parent.parent / "plugins"


@click.group()
@click.version_option(version="0.2.0")
def main():
    """evals-1337: Extension testing for claude-1337 marketplace.

    Test skills, agents, MCP servers, commands, and hooks.
    """
    pass


@main.command()
@click.argument("plugin_path", type=click.Path(exists=True))
@click.option("--mode", "-m", type=click.Choice(["baseline", "smart", "forced"]), default="baseline")
@click.option("--runs", "-n", default=3, help="Runs per test case")
@click.option("--prompt", "-p", help="Single prompt to test (instead of suite)")
@click.option("--expect", "-e", type=click.Choice(["must", "must_not", "ok"]), default="must")
def skills(plugin_path: str, mode: str, runs: int, prompt: str | None, expect: str):
    """Test skill activation.

    Examples:

        evals-1337 skills plugins/rust-1337

        evals-1337 skills plugins/rust-1337 -m forced -n 5

        evals-1337 skills plugins/rust-1337 -p "What crate for CLI args?"
    """
    plugin_dir = Path(plugin_path)
    plugins_root = plugin_dir.parent

    # Discover all skills for context
    all_skills = discover_skills(plugins_root)
    if not all_skills:
        console.print("[red]No skills found in plugins directory[/red]")
        return

    # Find the target skill
    target_skill = None
    for s in all_skills:
        if s["name"] == plugin_dir.name or plugin_dir.name in s["name"]:
            target_skill = s
            break

    if not target_skill:
        # Try loading directly
        from .targets.skills import load_skill_descriptions
        target_skill = load_skill_descriptions(plugin_dir)

    if not target_skill:
        console.print(f"[red]Could not find skill in {plugin_path}[/red]")
        return

    console.print(f"[bold]Testing skill:[/bold] {target_skill['name']}")
    console.print(f"[dim]Mode: {mode}, Runs: {runs}[/dim]\n")

    # Build test spec
    if prompt:
        # Single prompt mode
        expectation_map = {
            "must": Expectation.MUST_PASS,
            "must_not": Expectation.MUST_FAIL,
            "ok": Expectation.ACCEPTABLE,
        }
        test_cases = [SkillTestCase(
            prompt=prompt,
            expectation=expectation_map[expect],
            rationale="CLI test",
        )]
    else:
        # Default test cases
        test_cases = [
            SkillTestCase(
                prompt=f"What is {target_skill['name']} about?",
                expectation=Expectation.MUST_PASS,
                rationale="Direct mention of skill name",
            ),
            SkillTestCase(
                prompt="Write me a haiku about programming",
                expectation=Expectation.MUST_FAIL,
                rationale="Creative task, unrelated to skill",
            ),
        ]

    spec = SkillTestSpec(
        name=target_skill["name"],
        plugin=plugin_dir.name,
        test_cases=test_cases,
    )

    # Run tests
    async def _run():
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(
                f"Testing {spec.name} ({mode})...",
                total=len(test_cases) * runs,
            )

            report = await run_skill_test(
                skill_spec=spec,
                skills=all_skills,
                mode=mode,
                runs=runs,
            )

            progress.update(task, completed=len(test_cases) * runs)
            return report

    report = asyncio.run(_run())
    metrics = report.metrics()

    # Results table
    table = Table(title=f"Results: {spec.name}")
    table.add_column("Prompt", style="dim", max_width=50)
    table.add_column("Expected")
    table.add_column("Outcome")
    table.add_column("Skills Called")

    for r in report.results:
        prompt_preview = r.test_case.prompt[:47] + "..." if len(r.test_case.prompt) > 50 else r.test_case.prompt
        exp = "activate" if r.test_case.expectation == Expectation.MUST_PASS else "not activate"

        outcome_style = {
            "tp": "green", "tn": "green",
            "fp": "red", "fn": "red",
            "error": "red", "acceptable": "yellow",
        }.get(r.outcome.value, "white")

        skills_called = ", ".join(r.details.get("skills_activated", [])) or "-"

        table.add_row(
            prompt_preview,
            exp,
            f"[{outcome_style}]{r.outcome.value.upper()}[/{outcome_style}]",
            skills_called,
        )

    console.print(table)
    console.print()

    # Metrics
    console.print(format_confusion_matrix(metrics))

    f1_style = "green" if metrics.f1 >= 0.7 else "yellow" if metrics.f1 >= 0.5 else "red"
    console.print(f"[bold]Precision:[/bold] {metrics.precision:.1%}")
    console.print(f"[bold]Recall:[/bold] {metrics.recall:.1%}")
    console.print(f"[bold]F1:[/bold] [{f1_style}]{metrics.f1:.1%}[/{f1_style}]")


@main.command()
@click.argument("suite_file", type=click.Path(exists=True))
@click.option("--mode", "-m", type=click.Choice(["baseline", "smart", "forced"]), default="baseline")
@click.option("--output", "-o", type=click.Path(), help="Output JSON file")
def suite(suite_file: str, mode: str, output: str | None):
    """Run a test suite from JSON file.

    Example:

        evals-1337 suite suites/rigorous-v1.json -m baseline
    """
    with open(suite_file) as f:
        data = json.load(f)

    console.print(f"[bold]Running suite:[/bold] {data.get('name', suite_file)}")
    console.print(f"[dim]{data.get('description', '')}[/dim]\n")

    # TODO: Implement full suite runner
    console.print("[yellow]Full suite runner not yet implemented[/yellow]")
    console.print("Use 'evals-1337 skills <plugin>' for single skill testing")


@main.command()
def discover():
    """Discover skills in the marketplace."""
    skills = discover_skills(DEFAULT_PLUGINS)

    if not skills:
        console.print("[yellow]No skills found[/yellow]")
        return

    table = Table(title="Discovered Skills")
    table.add_column("Name")
    table.add_column("Description", max_width=60)

    for s in skills:
        table.add_row(s["name"], s["description"][:60] + "..." if len(s["description"]) > 60 else s["description"])

    console.print(table)
    console.print(f"\n[dim]Found {len(skills)} skills in {DEFAULT_PLUGINS}[/dim]")


if __name__ == "__main__":
    main()
