"""CLI for skill activation testing with rigorous metrics."""

import asyncio
import json
from pathlib import Path

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from .models import (
    ActivationReport,
    Expectation,
    SkillTestSpec,
    TestCase,
    TestSuite,
)
from .report import generate_comparison_report, generate_markdown_report
from .runner import get_default_options, run_comparison, run_single_test, run_test_suite

console = Console()


@click.group()
@click.version_option(version="0.2.0")
def cli():
    """Claude-1337 Skill Activation Tester.

    Tests skill activation with rigorous metrics (precision, recall, F1).
    Uses labeled test cases with ground truth expectations.
    """
    pass


@cli.command()
@click.argument("prompt")
@click.option("--skill", "-s", required=True, help="Skill name to test")
@click.option("--runs", "-n", default=3, help="Number of runs")
@click.option(
    "--expect",
    "-e",
    type=click.Choice(["must", "should_not", "acceptable"]),
    default="must",
    help="Expected outcome",
)
@click.option(
    "--mode",
    "-m",
    type=click.Choice(["baseline", "smart", "forced"]),
    default="baseline",
    help="System prompt mode",
)
def test(prompt: str, skill: str, runs: int, expect: str, mode: str):
    """Run a single activation test with labeled expectation."""
    expectation_map = {
        "must": Expectation.MUST_ACTIVATE,
        "should_not": Expectation.SHOULD_NOT_ACTIVATE,
        "acceptable": Expectation.ACCEPTABLE,
    }
    expectation = expectation_map[expect]

    test_case = TestCase(prompt=prompt, expectation=expectation)
    options = get_default_options(mode=mode)

    async def _run():
        results = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Testing {skill} ({mode} mode)...", total=runs)

            for _ in range(runs):
                result = await run_single_test(
                    skill_name=skill,
                    test_case=test_case,
                    options=options,
                )
                results.append(result)
                progress.update(task, advance=1)

        table = Table(title=f"Activation Results: {skill}")
        table.add_column("Run", style="dim")
        table.add_column("Status")
        table.add_column("Outcome")
        table.add_column("Skills Activated")
        table.add_column("Duration")

        for i, r in enumerate(results, 1):
            status_style = "green" if r.status.value == "activated" else "red"
            outcome_style = {
                "tp": "green",
                "tn": "green",
                "fp": "red",
                "fn": "red",
                "acceptable": "yellow",
                "error": "red",
            }.get(r.outcome.value, "white")

            table.add_row(
                str(i),
                f"[{status_style}]{r.status.value}[/{status_style}]",
                f"[{outcome_style}]{r.outcome.value}[/{outcome_style}]",
                ", ".join(r.skills_activated) or "-",
                f"{r.duration_ms}ms",
            )

        console.print(table)

        # Compute metrics
        report = ActivationReport(suite_name="single_test", runs=results)
        metrics = report.compute_metrics()

        console.print()
        console.print(f"[bold]Expectation[/bold]: {expectation.value}")
        console.print(f"[bold]Precision[/bold]: {metrics.precision * 100:.0f}%")
        console.print(f"[bold]Recall[/bold]: {metrics.recall * 100:.0f}%")
        console.print(f"[bold]F1[/bold]: {metrics.f1_score * 100:.0f}%")

    asyncio.run(_run())


@cli.command()
@click.argument("suite_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output markdown file")
@click.option("--json-output", type=click.Path(), help="Output JSON file")
@click.option(
    "--mode",
    "-m",
    type=click.Choice(["baseline", "smart", "forced"]),
    default="baseline",
    help="System prompt mode",
)
def suite(suite_file: str, output: str | None, json_output: str | None, mode: str):
    """Run a rigorous test suite from a JSON file."""
    with open(suite_file) as f:
        data = json.load(f)

    test_suite = TestSuite(**data)
    options = get_default_options(mode=mode)

    async def _run():
        total_cases = sum(len(s.test_cases) for s in test_suite.skills)
        total_cases += len(test_suite.negative_cases)
        total_tests = total_cases * test_suite.runs_per_case

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(
                f"Running {test_suite.name} ({mode} mode)...",
                total=total_tests,
            )

            report = await run_test_suite(
                test_suite,
                options,
                config_description=mode,
            )
            progress.update(task, completed=total_tests)

        return report

    report = asyncio.run(_run())
    metrics = report.compute_metrics()

    # Summary table
    table = Table(title=f"Results: {report.suite_name} ({mode})")
    table.add_column("Skill")
    table.add_column("Precision")
    table.add_column("Recall")
    table.add_column("F1")
    table.add_column("TP/FP/TN/FN")

    for skill_name, sm in report.skill_metrics().items():
        display_name = "(negative)" if skill_name == "__none__" else skill_name
        f1_style = "green" if sm.f1_score >= 0.8 else "yellow" if sm.f1_score >= 0.5 else "red"
        table.add_row(
            display_name,
            f"{sm.precision * 100:.0f}%",
            f"{sm.recall * 100:.0f}%",
            f"[{f1_style}]{sm.f1_score * 100:.0f}%[/{f1_style}]",
            f"{sm.true_positives}/{sm.false_positives}/{sm.true_negatives}/{sm.false_negatives}",
        )

    console.print(table)
    console.print()
    console.print(f"[bold]Overall Precision[/bold]: {metrics.precision * 100:.0f}%")
    console.print(f"[bold]Overall Recall[/bold]: {metrics.recall * 100:.0f}%")
    console.print(f"[bold]Overall F1[/bold]: {metrics.f1_score * 100:.0f}%")

    if output:
        md = generate_markdown_report(report)
        Path(output).write_text(md)
        console.print(f"\nReport saved to: {output}")

    if json_output:
        Path(json_output).write_text(report.model_dump_json(indent=2))
        console.print(f"JSON saved to: {json_output}")


@cli.command()
@click.argument("suite_file", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output markdown file")
@click.option(
    "--modes",
    "-m",
    multiple=True,
    default=["baseline", "smart", "forced"],
    help="Modes to compare",
)
def compare(suite_file: str, output: str | None, modes: tuple[str, ...]):
    """Run a test suite across multiple configurations and compare."""
    with open(suite_file) as f:
        data = json.load(f)

    test_suite = TestSuite(**data)

    async def _run():
        return await run_comparison(test_suite, list(modes))

    console.print(f"[bold]Comparing modes: {', '.join(modes)}[/bold]")
    console.print()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Running comparison...", total=len(modes))
        reports = asyncio.run(_run())
        progress.update(task, completed=len(modes))

    # Comparison table
    table = Table(title="Comparison Results")
    table.add_column("Metric")
    for mode in modes:
        table.add_column(mode)

    all_metrics = {name: r.compute_metrics() for name, r in reports.items()}

    for metric_name, getter in [
        ("Precision", lambda m: m.precision),
        ("Recall", lambda m: m.recall),
        ("F1 Score", lambda m: m.f1_score),
        ("Accuracy", lambda m: m.accuracy),
    ]:
        row = [metric_name]
        for mode in modes:
            value = getter(all_metrics[mode])
            row.append(f"{value * 100:.0f}%")
        table.add_row(*row)

    console.print(table)

    # Find best
    best_mode = max(modes, key=lambda m: all_metrics[m].f1_score)
    console.print()
    console.print(f"[bold]Best configuration[/bold]: {best_mode}")

    if output:
        md = generate_comparison_report(reports)
        Path(output).write_text(md)
        console.print(f"\nReport saved to: {output}")


@cli.command()
@click.argument("output", type=click.Path())
def init_suite(output: str):
    """Create a sample rigorous test suite JSON file."""
    sample = TestSuite(
        name="sample-rigorous-suite",
        description="Sample test suite with labeled expectations for rigorous evaluation",
        runs_per_case=5,
        skills=[
            SkillTestSpec(
                name="terminal-1337",
                plugin="terminal-1337",
                test_cases=[
                    TestCase(
                        prompt="How do I use ripgrep to search for a pattern?",
                        expectation=Expectation.MUST_ACTIVATE,
                        rationale="Direct mention of ripgrep",
                    ),
                    TestCase(
                        prompt="Find all TODO comments in my codebase",
                        expectation=Expectation.MUST_ACTIVATE,
                        rationale="Code search task, rg is the answer",
                    ),
                    TestCase(
                        prompt="Help me write a Python web scraper",
                        expectation=Expectation.SHOULD_NOT_ACTIVATE,
                        rationale="Python task, not CLI tools",
                    ),
                    TestCase(
                        prompt="How do I grep for a pattern?",
                        expectation=Expectation.ACCEPTABLE,
                        rationale="Could use built-in grep or suggest rg",
                    ),
                ],
            ),
        ],
        negative_cases=[
            TestCase(
                prompt="Write me a haiku about programming",
                expectation=Expectation.SHOULD_NOT_ACTIVATE,
                rationale="Creative task, no skill needed",
            ),
            TestCase(
                prompt="What's the weather today?",
                expectation=Expectation.SHOULD_NOT_ACTIVATE,
                rationale="General question, no skill needed",
            ),
        ],
    )

    Path(output).write_text(sample.model_dump_json(indent=2))
    console.print(f"Sample rigorous suite created: {output}")
    console.print()
    console.print("Key differences from legacy format:")
    console.print("- Each test case has an 'expectation' (must_activate, should_not_activate, acceptable)")
    console.print("- 'negative_cases' test that skills DON'T activate incorrectly")
    console.print("- Metrics include precision, recall, and F1 (not just activation rate)")


def main():
    cli()


if __name__ == "__main__":
    main()
