"""CLI for skill activation testing."""

import asyncio
import json
from pathlib import Path

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from .models import ActivationReport, SkillReference, TestSuite
from .report import generate_markdown_report
from .runner import run_single_test, run_test_suite

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Claude-1337 Skill Activation Tester.

    Tests whether skills activate correctly using the Claude Agent SDK.
    """
    pass


@cli.command()
@click.argument("prompt")
@click.option("--skill", "-s", required=True, help="Skill name to test")
@click.option("--runs", "-n", default=1, help="Number of runs")
def test(prompt: str, skill: str, runs: int):
    """Run a single activation test."""

    async def _run():
        results = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Testing {skill}...", total=runs)

            for i in range(runs):
                result = await run_single_test(skill_name=skill, prompt=prompt)
                results.append(result)
                progress.update(task, advance=1)

        table = Table(title=f"Activation Results: {skill}")
        table.add_column("Run", style="dim")
        table.add_column("Status")
        table.add_column("Skill Called")
        table.add_column("Tools Used")
        table.add_column("Duration")

        for i, r in enumerate(results, 1):
            status_style = "green" if r.status.value == "activated" else "red"
            table.add_row(
                str(i),
                f"[{status_style}]{r.status.value}[/{status_style}]",
                "Yes" if r.skill_called else "No",
                ", ".join(r.tool_calls[:3]) or "-",
                f"{r.duration_ms}ms",
            )

        console.print(table)

        activated = sum(1 for r in results if r.skill_called)
        rate = activated / len(results) * 100
        console.print(f"\nActivation Rate: [bold]{rate:.0f}%[/bold] ({activated}/{len(results)})")

    asyncio.run(_run())


@cli.command()
@click.argument("suite_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output markdown file")
@click.option("--json-output", type=click.Path(), help="Output JSON file")
def suite(suite_file: str, output: str | None, json_output: str | None):
    """Run a test suite from a JSON file."""
    with open(suite_file) as f:
        data = json.load(f)

    test_suite = TestSuite(**data)

    async def _run():
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            total_tests = sum(
                len(s.expected_triggers) * test_suite.runs_per_prompt
                for s in test_suite.skills
            )
            task = progress.add_task(f"Running {test_suite.name}...", total=total_tests)

            report = await run_test_suite(test_suite)
            progress.update(task, completed=total_tests)

        return report

    report = asyncio.run(_run())

    table = Table(title=f"Results: {report.suite_name}")
    table.add_column("Skill")
    table.add_column("Activated")
    table.add_column("Total")
    table.add_column("Rate")

    for skill_name, stats in report.skill_stats().items():
        rate = stats["rate"] * 100
        rate_style = "green" if rate >= 80 else "yellow" if rate >= 50 else "red"
        table.add_row(
            skill_name,
            str(stats["activated"]),
            str(stats["total"]),
            f"[{rate_style}]{rate:.0f}%[/{rate_style}]",
        )

    console.print(table)
    console.print(f"\n[bold]Overall: {report.activation_rate * 100:.0f}%[/bold]")

    if output:
        md = generate_markdown_report(report)
        Path(output).write_text(md)
        console.print(f"\nReport saved to: {output}")

    if json_output:
        Path(json_output).write_text(report.model_dump_json(indent=2))
        console.print(f"JSON saved to: {json_output}")


@cli.command()
@click.argument("output", type=click.Path())
def init_suite(output: str):
    """Create a sample test suite JSON file."""
    sample = TestSuite(
        name="claude-1337-skills",
        description="Test activation of claude-1337 marketplace skills",
        skills=[
            SkillReference(
                name="terminal-1337",
                plugin="terminal-1337",
                expected_triggers=[
                    "How do I search for a pattern in my codebase?",
                    "What's a fast way to find files by name?",
                    "Show me how to use ripgrep",
                ],
            ),
            SkillReference(
                name="rust-1337",
                plugin="rust-1337",
                expected_triggers=[
                    "What crate should I use for CLI argument parsing?",
                    "How do I structure a Rust backend with axum?",
                    "What's the best error handling crate for Rust?",
                ],
            ),
        ],
        runs_per_prompt=3,
    )

    Path(output).write_text(sample.model_dump_json(indent=2))
    console.print(f"Sample suite created: {output}")


def main():
    cli()


if __name__ == "__main__":
    main()
