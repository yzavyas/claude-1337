"""CLI for evals-1337."""

import asyncio
import json
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
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


@main.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option("--skill", "-s", help="Target skill for activation testing")
@click.option("--runs", "-n", default=3, help="Runs per test case")
@click.option("--output", "-o", type=click.Path(), help="Output JSON file")
@click.option(
    "--runtime", "-r",
    type=click.Choice(["agent-sdk", "anthropic-api", "agent-sdk-skill"]),
    default="agent-sdk",
    help="Runtime to use (default: agent-sdk)"
)
@click.option("--verbose", "-v", is_flag=True, help="Show detailed output")
@click.option("--traces", "-t", type=click.Path(), help="Save traces to directory")
def compare(config_file: str, skill: str | None, runs: int, output: str | None, runtime: str, verbose: bool, traces: str | None):
    """Compare configs for baseline analysis.

    Run same prompts against different context configurations to measure
    what value an extension adds over baseline Claude.

    Runtimes:
      - agent-sdk: Claude Agent SDK (recommended, full Claude Code experience)
      - anthropic-api: Raw Anthropic API (faster, simpler)
      - agent-sdk-skill: Agent SDK with custom Skill tool for activation testing

    Examples:

        evals-1337 compare configs/baseline-comparison.yaml -s core-1337

        evals-1337 compare configs/rust-comparison.yaml -s rust-1337 -n 5 -r anthropic-api
    """
    from .core.comparison import (
        ComparisonTestCase,
        ComparisonRunner,
        load_configs_from_yaml,
    )
    from .ports.runtime import EvalConfig

    config_path = Path(config_file)
    configs = load_configs_from_yaml(config_path)

    if not configs:
        console.print("[red]No configs found in file[/red]")
        return

    console.print(f"[bold]Baseline Comparison[/bold]")
    console.print(f"[dim]Config file: {config_file}[/dim]")
    console.print(f"[dim]Runtime: {runtime}[/dim]")
    console.print(f"[dim]Configs: {', '.join(configs.keys())}[/dim]")
    console.print(f"[dim]Runs per case: {runs}[/dim]\n")

    # Build test cases
    # For now, use a simple default set; later can load from config
    test_cases = [
        ComparisonTestCase(
            prompt="What crate should I use for CLI argument parsing in Rust?",
            expectation=Expectation.MUST_PASS if skill else Expectation.ACCEPTABLE,
            target_skill=skill,
            rationale="Domain-specific question",
        ),
        ComparisonTestCase(
            prompt="Write me a haiku about programming",
            expectation=Expectation.MUST_FAIL if skill else Expectation.ACCEPTABLE,
            target_skill=skill,
            rationale="Creative task, should not trigger domain skill",
        ),
        ComparisonTestCase(
            prompt="Help me debug this error: thread 'main' panicked at 'called Option::unwrap() on a None value'",
            expectation=Expectation.MUST_PASS if skill else Expectation.ACCEPTABLE,
            target_skill=skill,
            rationale="Technical question in domain",
        ),
    ]

    # If skill specified, add it to available_skills in each config
    if skill:
        skill_info = {"name": skill, "description": f"Skill: {skill}"}
        for cfg in configs.values():
            cfg.available_skills = [skill_info]

    # Select adapter based on runtime
    def get_adapter():
        if runtime == "agent-sdk":
            from .adapters.claude_agent_sdk import ClaudeAgentSDKAdapter
            return ClaudeAgentSDKAdapter()
        elif runtime == "agent-sdk-skill":
            from .adapters.claude_agent_sdk import ClaudeAgentSDKWithSkillToolAdapter
            return ClaudeAgentSDKWithSkillToolAdapter()
        else:  # anthropic-api
            from .adapters.anthropic_api import AnthropicAdapter
            return AnthropicAdapter()

    # Run comparison
    async def _run():
        adapter = get_adapter()
        runner = ComparisonRunner(adapter)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(
                "Running comparison...",
                total=len(test_cases) * len(configs) * runs,
            )

            report = await runner.run_comparison(
                name=f"Comparison: {config_path.stem}",
                test_cases=test_cases,
                configs=configs,
                runs_per_case=runs,
            )

            progress.update(task, completed=len(test_cases) * len(configs) * runs)
            return report

    report = asyncio.run(_run())

    # Display results
    table = Table(title="Comparison Results")
    table.add_column("Config")
    table.add_column("Precision", justify="right")
    table.add_column("Recall", justify="right")
    table.add_column("F1", justify="right")
    table.add_column("Δ Baseline", justify="right")
    table.add_column("Δ Previous", justify="right")

    for row in report.summary():
        delta_b = row["delta_baseline"]
        delta_p = row["delta_previous"]

        delta_b_str = f"{delta_b:+.3f}" if delta_b is not None else "-"
        delta_p_str = f"{delta_p:+.3f}" if delta_p is not None else "-"

        # Color deltas
        if delta_b is not None:
            if delta_b > 0.05:
                delta_b_str = f"[green]{delta_b_str}[/green]"
            elif delta_b < -0.05:
                delta_b_str = f"[red]{delta_b_str}[/red]"

        f1_style = "green" if row["f1"] >= 0.7 else "yellow" if row["f1"] >= 0.5 else "red"

        table.add_row(
            row["config"],
            f"{row['precision']:.3f}",
            f"{row['recall']:.3f}",
            f"[{f1_style}]{row['f1']:.3f}[/{f1_style}]",
            delta_b_str,
            delta_p_str,
        )

    console.print(table)

    # Save if output specified
    if output:
        import json
        with open(output, "w") as f:
            json.dump({
                "name": report.name,
                "runs_per_case": report.runs_per_case,
                "summary": report.summary(),
            }, f, indent=2)
        console.print(f"\n[dim]Results saved to {output}[/dim]")


@main.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option("--verbose", "-v", is_flag=True, help="Show detailed output")
@click.option("--output", "-o", type=click.Path(), help="Output JSON file")
def benchmark(config_file: str, verbose: bool, output: str | None):
    """Run A/B benchmark from config.

    Compare baseline Claude vs Claude with skill loaded.
    Everything is defined in the config file - no CLI flags needed.

    Example:

        evals-1337 benchmark configs/rust-skill-benchmark.yaml
    """
    from .core.benchmark import BenchmarkRunner
    from .adapters.claude_agent_sdk import ClaudeAgentSDKAdapter

    config_path = Path(config_file)

    console.print(f"[bold]A/B Benchmark[/bold]")
    console.print(f"[dim]Config: {config_file}[/dim]\n")

    async def _run():
        adapter = ClaudeAgentSDKAdapter()
        runner = BenchmarkRunner(adapter)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Running benchmark...", total=None)
            report = await runner.run(config_path)
            progress.update(task, completed=True)
            return report

    report = asyncio.run(_run())

    # Display results
    console.print(f"\n[bold]{report.name}[/bold]")
    console.print(f"[dim]{report.description}[/dim]\n")

    # Results table
    table = Table(title="A/B Comparison Results")
    table.add_column("Prompt", max_width=40)
    table.add_column("Category")
    table.add_column("A Keywords")
    table.add_column("B Keywords")
    table.add_column("B Better?")
    table.add_column("Met Expect?")

    for r in report.results:
        prompt_preview = r.case.prompt[:37] + "..." if len(r.case.prompt) > 40 else r.case.prompt

        b_better = "[green]Yes[/green]" if r.b_is_better else "[dim]No[/dim]"
        met_exp = "[green]Yes[/green]" if r.meets_expectation else "[red]No[/red]"

        table.add_row(
            prompt_preview,
            r.case.category,
            str(r.a_keyword_count),
            str(r.b_keyword_count),
            b_better,
            met_exp,
        )

    console.print(table)

    # Summary
    console.print(f"\n[bold]Summary[/bold]")
    console.print(f"  Improvement rate: [cyan]{report.improvement_rate:.1%}[/cyan]")
    console.print(f"  Expectations met: [cyan]{report.expectation_met_rate:.1%}[/cyan]")

    # By category
    summary = report.summary()
    if summary["by_category"]:
        console.print(f"\n[bold]By Category[/bold]")
        for cat, stats in summary["by_category"].items():
            console.print(f"  {cat}: {stats['improved']}/{stats['total']} improved")

    # Verbose: show response comparisons
    if verbose:
        console.print(f"\n[bold]Response Comparisons[/bold]")
        for r in report.results:
            console.print(f"\n[dim]Prompt:[/dim] {r.case.prompt}")
            console.print(Panel(
                r.response_a[:300] + "..." if len(r.response_a) > 300 else r.response_a,
                title="A (baseline)",
                border_style="dim",
            ))
            console.print(Panel(
                r.response_b[:300] + "..." if len(r.response_b) > 300 else r.response_b,
                title="B (with skill)",
                border_style="blue",
            ))

    # Save output
    if output:
        import json
        with open(output, "w") as f:
            json.dump(summary, f, indent=2)
        console.print(f"\n[dim]Saved to {output}[/dim]")


@main.command()
def runtimes():
    """List available runtimes."""
    table = Table(title="Available Runtimes")
    table.add_column("Name")
    table.add_column("Description")
    table.add_column("Status")

    # Check if Agent SDK is available
    try:
        from claude_agent_sdk import query
        sdk_status = "[green]Available[/green]"
    except ImportError:
        sdk_status = "[yellow]Not installed (pip install claude-agent-sdk)[/yellow]"

    table.add_row(
        "agent-sdk",
        "Claude Agent SDK - full Claude Code experience (recommended)",
        sdk_status,
    )
    table.add_row(
        "agent-sdk-skill",
        "Agent SDK with custom Skill tool for activation testing",
        sdk_status,
    )
    table.add_row(
        "anthropic-api",
        "Direct Anthropic API calls (faster, simpler)",
        "[green]Available[/green]",
    )
    table.add_row(
        "mock",
        "Mock adapter for unit testing",
        "[green]Available[/green]",
    )

    console.print(table)
    console.print("\n[dim]Use --runtime / -r flag in compare command to select runtime[/dim]")


if __name__ == "__main__":
    main()
