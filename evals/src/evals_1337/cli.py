"""CLI for evals-1337.

Extension testing framework using hexagonal architecture.
"""

import asyncio
import json
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from .adapters import create_default_registry
from .core.models import Expectation, TestCase
from .metrics.classification import format_confusion_matrix, metric_indicator
from .plugins import discover_plugins, validate_all, validate_plugin

console = Console()

# Default paths relative to repo root
DEFAULT_PLUGINS = Path(__file__).parent.parent.parent.parent / "plugins"


def load_skill_info(plugin_dir: Path) -> dict[str, str] | None:
    """Load skill name and description from SKILL.md frontmatter."""
    skill_file = plugin_dir / "SKILL.md"
    if not skill_file.exists():
        return None

    content = skill_file.read_text()
    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    frontmatter = parts[1]
    name = None
    description = None

    for line in frontmatter.strip().split("\n"):
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("description:"):
            description = line.split(":", 1)[1].strip().strip('"')

    if name and description:
        return {"name": name, "description": description}
    return None


def discover_skills(plugins_dir: Path) -> list[dict[str, str]]:
    """Discover all skills from plugins directory."""
    skills = []
    for plugin_dir in plugins_dir.iterdir():
        if plugin_dir.is_dir():
            skill = load_skill_info(plugin_dir)
            if skill:
                skills.append(skill)
    return skills


@click.group()
@click.version_option(version="0.3.0")
def main():
    """evals-1337: Extension testing for claude-1337 marketplace.

    Test skills, agents, MCP servers, commands, and hooks using
    rigorous precision/recall metrics.

    \b
    Examples:
        evals-1337 discover              # List available skills
        evals-1337 skills rust-1337      # Test skill activation
        evals-1337 validate              # Validate all plugins
    """
    pass


@main.command()
@click.argument("plugin_name")
@click.option(
    "--runtime", "-r",
    type=click.Choice(["simulation", "headless"]),
    default="simulation",
    help="Runtime: simulation (API) or headless (claude -p)",
)
@click.option(
    "--mode", "-m",
    type=click.Choice(["baseline", "smart", "forced"]),
    default="baseline",
    help="Prompting mode for skill activation",
)
@click.option("--runs", "-n", default=3, help="Runs per test case")
@click.option("--prompt", "-p", help="Single prompt to test")
@click.option(
    "--expect", "-e",
    type=click.Choice(["must", "must_not", "ok"]),
    default="must",
    help="Expected outcome for single prompt",
)
@click.option("--plugins-dir", type=click.Path(exists=True), help="Plugins directory")
def skills(
    plugin_name: str,
    runtime: str,
    mode: str,
    runs: int,
    prompt: str | None,
    expect: str,
    plugins_dir: str | None,
):
    """Test skill activation with precision/recall metrics.

    \b
    Examples:
        # Test with simulation (fast, uses API directly)
        evals-1337 skills rust-1337 -r simulation

        # Test with headless (realistic, uses claude -p)
        evals-1337 skills rust-1337 -r headless

        # Test single prompt
        evals-1337 skills rust-1337 -p "What crate for CLI args?"

        # Test negative case
        evals-1337 skills rust-1337 -p "Write a haiku" -e must_not
    """
    plugins_path = Path(plugins_dir) if plugins_dir else DEFAULT_PLUGINS
    plugin_path = plugins_path / plugin_name

    if not plugin_path.exists():
        # Try with -1337 suffix
        plugin_path = plugins_path / f"{plugin_name}-1337"
        if not plugin_path.exists():
            console.print(f"[red]Plugin not found: {plugin_name}[/red]")
            return

    # Load skill info
    skill_info = load_skill_info(plugin_path)
    if not skill_info:
        console.print(f"[red]No SKILL.md found in {plugin_path.name}[/red]")
        return

    # Discover all skills for context
    all_skills = discover_skills(plugins_path)

    console.print(f"[bold]Testing skill:[/bold] {skill_info['name']}")
    console.print(f"[dim]Runtime: {runtime}, Mode: {mode}, Runs: {runs}[/dim]\n")

    # Build test cases
    expectation_map = {
        "must": Expectation.MUST_PASS,
        "must_not": Expectation.MUST_FAIL,
        "ok": Expectation.ACCEPTABLE,
    }

    if prompt:
        test_cases = [
            TestCase(
                prompt=prompt,
                expectation=expectation_map[expect],
                rationale="CLI test",
            )
        ]
    else:
        # Default test cases
        test_cases = [
            TestCase(
                prompt=f"Help me with {skill_info['name'].replace('-1337', '')} tasks",
                expectation=Expectation.MUST_PASS,
                rationale="Direct domain reference",
            ),
            TestCase(
                prompt="Write me a haiku about programming",
                expectation=Expectation.MUST_FAIL,
                rationale="Creative task, unrelated to skill",
            ),
        ]

    # Get runner from registry
    registry = create_default_registry()

    if not registry.supports("skills", runtime):
        console.print(f"[red]Runtime '{runtime}' not available for skills[/red]")
        available = [f"{e}:{r}" for e, r in registry.list_runners() if e == "skills"]
        console.print(f"Available: {', '.join(available)}")
        return

    runner = registry.get("skills", runtime)

    # Run tests
    async def _run():
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(
                f"Testing {skill_info['name']} ({runtime}/{mode})...",
                total=len(test_cases) * runs,
            )

            report = await runner.run_batch(
                test_cases=test_cases,
                runs=runs,
                target_skill=skill_info["name"],
                available_skills=all_skills,
                mode=mode,
            )

            progress.update(task, completed=len(test_cases) * runs)
            return report

    report = asyncio.run(_run())
    metrics = report.metrics()

    # Results table
    table = Table(title=f"Results: {skill_info['name']}")
    table.add_column("Prompt", style="dim", max_width=50)
    table.add_column("Expected")
    table.add_column("Outcome")
    table.add_column("Skills Called")

    for r in report.results:
        prompt_preview = (
            r.test_case.prompt[:47] + "..."
            if len(r.test_case.prompt) > 50
            else r.test_case.prompt
        )
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

    console.print(f"[bold]Precision:[/bold] {metrics.precision:.1%} {metric_indicator(metrics.precision)}")
    console.print(f"[bold]Recall:[/bold] {metrics.recall:.1%} {metric_indicator(metrics.recall)}")
    console.print(f"[bold]F1:[/bold] {metrics.f1:.1%} {metric_indicator(metrics.f1)}")


@main.command()
@click.option("--plugins-dir", type=click.Path(exists=True), help="Plugins directory")
def discover(plugins_dir: str | None):
    """Discover skills in the marketplace."""
    plugins_path = Path(plugins_dir) if plugins_dir else DEFAULT_PLUGINS
    skills = discover_skills(plugins_path)

    if not skills:
        console.print("[yellow]No skills found[/yellow]")
        return

    table = Table(title="Discovered Skills")
    table.add_column("Name")
    table.add_column("Description", max_width=60)

    for s in skills:
        desc = s["description"]
        if len(desc) > 60:
            desc = desc[:57] + "..."
        table.add_row(s["name"], desc)

    console.print(table)
    console.print(f"\n[dim]Found {len(skills)} skills in {plugins_path}[/dim]")


@main.command()
@click.option("--plugins-dir", type=click.Path(exists=True), help="Plugins directory")
@click.option("--use-cli", is_flag=True, help="Use claude plugin validate")
def validate(plugins_dir: str | None, use_cli: bool):
    """Validate all plugin manifests and hooks."""
    plugins_path = Path(plugins_dir) if plugins_dir else DEFAULT_PLUGINS

    console.print(f"[bold]Validating plugins in:[/bold] {plugins_path}\n")

    results = validate_all(plugins_path, use_cli=use_cli)

    if not results:
        console.print("[yellow]No plugins found[/yellow]")
        return

    table = Table(title="Plugin Validation Results")
    table.add_column("Plugin")
    table.add_column("Status")
    table.add_column("Errors", max_width=60)

    passed = 0
    failed = 0

    for r in results:
        if r.valid:
            passed += 1
            table.add_row(r.plugin_name, "[green]✓ Valid[/green]", "")
        else:
            failed += 1
            errors = "; ".join(r.errors[:2])
            if len(r.errors) > 2:
                errors += f" (+{len(r.errors) - 2} more)"
            table.add_row(r.plugin_name, "[red]✗ Invalid[/red]", errors)

    console.print(table)
    console.print(f"\n[bold]Summary:[/bold] {passed} valid, {failed} invalid")

    if failed > 0:
        raise SystemExit(1)


@main.command()
def runtimes():
    """List available runtimes and extension types."""
    registry = create_default_registry()
    runners = registry.list_runners()

    table = Table(title="Available Runners")
    table.add_column("Extension Type")
    table.add_column("Runtime")

    for ext_type, runtime in sorted(runners):
        table.add_row(ext_type, runtime)

    console.print(table)

    console.print("\n[dim]Runtimes:[/dim]")
    console.print("  simulation - Direct API calls with mock tools (fast)")
    console.print("  headless   - Real claude -p execution (realistic)")


@main.command()
@click.argument("suite_file", type=click.Path(exists=True))
@click.option("--runtime", "-r", type=click.Choice(["simulation", "headless"]), default="simulation")
@click.option("--mode", "-m", type=click.Choice(["baseline", "smart", "forced"]), default="baseline")
@click.option("--output", "-o", type=click.Path(), help="Output JSON file")
def suite(suite_file: str, runtime: str, mode: str, output: str | None):
    """Run a test suite from JSON file.

    \b
    Suite format:
    {
      "name": "suite-name",
      "skills": [
        {
          "name": "skill-name",
          "test_cases": [
            {"prompt": "...", "expectation": "must_pass", "rationale": "..."}
          ]
        }
      ]
    }
    """
    with open(suite_file) as f:
        data = json.load(f)

    console.print(f"[bold]Running suite:[/bold] {data.get('name', suite_file)}")
    console.print(f"[dim]{data.get('description', '')}[/dim]\n")

    # TODO: Full suite runner
    console.print("[yellow]Full suite runner coming soon[/yellow]")
    console.print("Use 'evals-1337 skills <plugin>' for individual skill testing")


if __name__ == "__main__":
    main()
