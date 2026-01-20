"""Lab 1337 CLI - Domain-driven experiment runner.

CLI Structure (noun-verb pattern):
    lab experiment list|show|init|validate
    lab batch list|show|run|validate|new
    lab condition list|show|validate
    lab task list|show|validate
    lab result list|show|analyze|verify
    lab report generate
    lab observe phoenix

Based on Ace's DX analysis and Karman's domain ontology.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
import yaml
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from .config import parse_frontmatter

console = Console()
log = logging.getLogger("lab")


# --- Helpers ---


def get_lab_root() -> Path:
    """Get the lab root directory.

    Resolution order:
    1. LAB_ROOT environment variable (explicit override)
    2. Current directory if it has experiments/ (user's project)
    3. Walk up to find lab-1337/ (development mode)
    4. Fall back to cwd
    """
    import os

    # 1. Explicit env var
    if env_root := os.environ.get("LAB_ROOT"):
        return Path(env_root)

    # 2. Cwd has experiments/ - user is in their project root
    cwd = Path.cwd()
    if (cwd / "experiments").is_dir():
        return cwd

    # 3. Walk up from cwd looking for experiments/ (user is inside project)
    current = cwd
    while current.parent != current:
        if (current / "experiments").is_dir():
            return current
        current = current.parent

    # 4. Dev mode: walk up from source file to find lab-1337/
    current = Path(__file__).parent
    while current.name != "lab-1337" and current.parent != current:
        current = current.parent
    if current.name == "lab-1337":
        return current

    # 5. Last resort: cwd
    return cwd


def resolve_experiment(experiment: Optional[str]) -> Path:
    """Resolve experiment directory from name or context.

    Resolution order:
    1. Explicit -e/--experiment flag
    2. Current directory if inside an experiment
    3. Error with helpful message
    """
    lab_root = get_lab_root()
    experiments_dir = lab_root / "experiments"

    if experiment:
        exp_path = experiments_dir / experiment
        if not exp_path.exists():
            raise click.UsageError(
                f"Experiment '{experiment}' not found.\n"
                f"Available: {', '.join(e.name for e in experiments_dir.iterdir() if e.is_dir())}"
            )
        return exp_path

    # Check if cwd is inside an experiment
    cwd = Path.cwd().resolve()
    experiments_dir = experiments_dir.resolve()

    if cwd.is_relative_to(experiments_dir):
        # Get first directory after experiments/
        rel_path = cwd.relative_to(experiments_dir)
        exp_name = rel_path.parts[0] if rel_path.parts else None
        if exp_name:
            return experiments_dir / exp_name

    raise click.UsageError(
        "Specify experiment with -e/--experiment or cd into an experiment directory.\n"
        f"Available: {', '.join(e.name for e in experiments_dir.iterdir() if e.is_dir())}"
    )


def load_batch_config(batch_path: Path) -> dict:
    """Load and validate a batch configuration."""
    with open(batch_path) as f:
        return yaml.safe_load(f)


def load_condition(condition_path: Path) -> dict:
    """Load a condition from markdown file."""
    content = condition_path.read_text()
    frontmatter, body = parse_frontmatter(content)
    frontmatter["prompt"] = body.strip()
    return frontmatter


def count_tasks(tasks_dir: Path) -> int:
    """Count tasks recursively."""
    return sum(1 for _ in tasks_dir.rglob("*.yaml"))


def list_batches(exp_path: Path) -> list[Path]:
    """List batch configs in an experiment."""
    # Check both scenarios/ and batches/ (migration support)
    for dir_name in ["batches", "scenarios"]:
        batch_dir = exp_path / dir_name
        if batch_dir.exists():
            return sorted(batch_dir.glob("*.yaml"))
    return []


# --- Main CLI ---


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
@click.option("-q", "--quiet", is_flag=True, help="Suppress non-error output")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def cli(ctx: click.Context, verbose: bool, quiet: bool, as_json: bool):
    """Lab 1337 - Research, experimentation and design for effective collaborative intelligence through cognitive extensions.

    The CLI follows domain language:
    - experiment: A scientific investigation
    - batch: A specific execution configuration
    - condition: The independent variable (prompting style)
    - task: A problem to solve

    Examples:
        lab experiment list
        lab batch run pilot -e rep-002
        lab condition show motivation -e rep-002
    """
    ctx.ensure_object(dict)
    ctx.obj["json"] = as_json
    ctx.obj["quiet"] = quiet

    if quiet:
        level = logging.WARNING
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(console=console, show_path=False)],
    )


# --- Experiment Commands ---


@cli.group()
def experiment():
    """Manage experiments."""
    pass


@experiment.command("list")
@click.pass_context
def experiment_list(ctx: click.Context):
    """List all experiments."""
    lab_root = get_lab_root()
    experiments_dir = lab_root / "experiments"

    if not experiments_dir.exists():
        console.print("[yellow]No experiments directory found.[/yellow]")
        return

    experiments = sorted(
        [d for d in experiments_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
    )

    if ctx.obj.get("json"):
        data = []
        for exp_path in experiments:
            conditions = list((exp_path / "conditions").glob("*.md")) if (exp_path / "conditions").exists() else []
            tasks_dir = exp_path / "tasks"
            task_count = count_tasks(tasks_dir) if tasks_dir.exists() else 0
            batches = list_batches(exp_path)
            results_dir = exp_path / "results"
            results = list(results_dir.glob("*.json")) if results_dir.exists() else []

            data.append({
                "name": exp_path.name,
                "conditions": len(conditions),
                "tasks": task_count,
                "batches": len(batches),
                "results": len(results),
            })
        console.print(json.dumps(data, indent=2))
        return

    table = Table(title="Experiments")
    table.add_column("EXPERIMENT", style="cyan")
    table.add_column("CONDITIONS", justify="right")
    table.add_column("TASKS", justify="right")
    table.add_column("BATCHES", justify="right")
    table.add_column("RESULTS", justify="right")

    for exp_path in experiments:
        conditions = list((exp_path / "conditions").glob("*.md")) if (exp_path / "conditions").exists() else []
        tasks_dir = exp_path / "tasks"
        task_count = count_tasks(tasks_dir) if tasks_dir.exists() else 0
        batches = list_batches(exp_path)
        results_dir = exp_path / "results"
        results = list(results_dir.glob("*.json")) if results_dir.exists() else []

        table.add_row(
            exp_path.name,
            str(len(conditions)),
            str(task_count),
            str(len(batches)),
            str(len(results)),
        )

    console.print(table)


@experiment.command("show")
@click.argument("name")
@click.pass_context
def experiment_show(ctx: click.Context, name: str):
    """Show experiment details."""
    lab_root = get_lab_root()
    exp_path = lab_root / "experiments" / name

    if not exp_path.exists():
        raise click.UsageError(f"Experiment '{name}' not found.")

    # Load README if exists
    readme_path = exp_path / "README.md"
    readme_content = ""
    hypothesis = ""
    if readme_path.exists():
        readme_content = readme_path.read_text()
        # Try to extract hypothesis from markdown
        for line in readme_content.split("\n"):
            if "hypothesis" in line.lower() or "question" in line.lower():
                hypothesis = line.strip("# ").strip()
                break

    # Count resources
    conditions_dir = exp_path / "conditions"
    conditions = []
    if conditions_dir.exists():
        for cond_path in sorted(conditions_dir.glob("*.md")):
            cond = load_condition(cond_path)
            conditions.append({
                "name": cond_path.stem,
                "type": cond.get("type", "unknown"),
                "description": cond.get("description", ""),
            })

    tasks_dir = exp_path / "tasks"
    task_count = count_tasks(tasks_dir) if tasks_dir.exists() else 0

    batches = list_batches(exp_path)
    results_dir = exp_path / "results"
    results = list(results_dir.glob("*.json")) if results_dir.exists() else []

    if ctx.obj.get("json"):
        data = {
            "name": name,
            "hypothesis": hypothesis,
            "conditions": conditions,
            "task_count": task_count,
            "batches": [b.stem for b in batches],
            "result_count": len(results),
        }
        console.print(json.dumps(data, indent=2))
        return

    # Rich output
    console.print(f"\n[bold cyan]{name.upper()}[/bold cyan]")
    console.print("─" * 40)

    if hypothesis:
        console.print(f"\n[bold]Hypothesis:[/bold]\n  {hypothesis}\n")

    if conditions:
        console.print(f"[bold]Conditions ({len(conditions)}):[/bold]")
        for cond in conditions:
            type_badge = f"[dim]({cond['type']})[/dim]" if cond["type"] else ""
            console.print(f"  • {cond['name']} {type_badge}")
        console.print()

    console.print(f"[bold]Tasks:[/bold] {task_count}")
    console.print(f"[bold]Batches:[/bold] {len(batches)}")
    for b in batches:
        console.print(f"  • {b.stem}")
    console.print(f"[bold]Results:[/bold] {len(results)} files\n")


@experiment.command("init")
@click.argument("name")
@click.option("-n", "--dry-run", is_flag=True, help="Show what would be created")
def experiment_init(name: str, dry_run: bool):
    """Initialize a new experiment with scaffold."""
    lab_root = get_lab_root()
    exp_path = lab_root / "experiments" / name

    if exp_path.exists():
        raise click.UsageError(f"Experiment '{name}' already exists.")

    dirs_to_create = [
        exp_path,
        exp_path / "conditions",
        exp_path / "tasks",
        exp_path / "batches",
        exp_path / "results",
    ]

    files_to_create = {
        exp_path / "README.md": f"""# {name}

## Hypothesis

[What question are you testing?]

## Design

[How will you test it?]

## Conditions

| Condition | Type | Description |
|-----------|------|-------------|
| baseline | baseline | Control condition |

## Expected Outcomes

[What do you expect to find?]
""",
        exp_path / "conditions" / "baseline.md": """---
name: baseline
type: baseline
description: Control condition with no special prompting
---

# Baseline Condition

No special instructions. Raw task only.
""",
        exp_path / "batches" / "pilot.yaml": f"""# Pilot batch for {name}
name: {name}-pilot

# Reference tasks (create in tasks/ directory)
tasks:
  - example-task

# Reference conditions (create in conditions/ directory)
conditions:
  - baseline

# Execution settings
model: sonnet
runs_per_condition: 3

# Iteration strategy
iteration:
  strategy: none
  max_iterations: 1
""",
    }

    if dry_run:
        console.print("[bold]Would create:[/bold]")
        for d in dirs_to_create:
            console.print(f"  [cyan]📁 {d.relative_to(lab_root)}[/cyan]")
        for f in files_to_create:
            console.print(f"  [green]📄 {f.relative_to(lab_root)}[/green]")
        return

    # Create directories
    for d in dirs_to_create:
        d.mkdir(parents=True, exist_ok=True)
        console.print(f"[green]Created:[/green] {d.relative_to(lab_root)}")

    # Create files
    for f, content in files_to_create.items():
        f.write_text(content)
        console.print(f"[green]Created:[/green] {f.relative_to(lab_root)}")

    console.print(f"\n[bold green]✓[/bold green] Experiment '{name}' initialized.")
    console.print(f"\nNext steps:")
    console.print(f"  1. Edit {exp_path.relative_to(lab_root)}/conditions/*.md")
    console.print(f"  2. Add tasks to {exp_path.relative_to(lab_root)}/tasks/")
    console.print(f"  3. Validate: lab experiment validate {name}")
    console.print(f"  4. Run pilot: lab batch run pilot -e {name}")


@experiment.command("validate")
@click.argument("name")
@click.option("--strict", is_flag=True, help="Treat warnings as errors")
def experiment_validate(name: str, strict: bool):
    """Validate experiment structure and references."""
    lab_root = get_lab_root()
    exp_path = lab_root / "experiments" / name

    if not exp_path.exists():
        raise click.UsageError(f"Experiment '{name}' not found.")

    console.print(f"Validating [cyan]{name}[/cyan]...\n")

    errors = []
    warnings = []
    passes = []

    # Check directory structure
    required_dirs = ["conditions", "tasks"]
    for d in required_dirs:
        if (exp_path / d).exists():
            passes.append(f"Directory '{d}/' exists")
        else:
            errors.append(f"Missing required directory: {d}/")

    # Check for batches (scenarios or batches dir)
    batches = list_batches(exp_path)
    if batches:
        passes.append(f"Found {len(batches)} batch configuration(s)")
    else:
        warnings.append("No batch configurations found (batches/ or scenarios/)")

    # Validate conditions
    conditions_dir = exp_path / "conditions"
    if conditions_dir.exists():
        for cond_path in conditions_dir.glob("*.md"):
            try:
                cond = load_condition(cond_path)
                if "name" in cond:
                    passes.append(f"Condition '{cond_path.stem}' has valid frontmatter")
                else:
                    warnings.append(f"Condition '{cond_path.stem}' missing 'name' field")
            except Exception as e:
                errors.append(f"Condition '{cond_path.stem}' invalid: {e}")

    # Validate tasks
    tasks_dir = exp_path / "tasks"
    if tasks_dir.exists():
        for task_path in tasks_dir.rglob("*.yaml"):
            try:
                with open(task_path) as f:
                    task = yaml.safe_load(f)
                if task:
                    passes.append(f"Task '{task_path.stem}' is valid YAML")
                else:
                    warnings.append(f"Task '{task_path.stem}' is empty")
            except Exception as e:
                errors.append(f"Task '{task_path.stem}' invalid: {e}")

    # Validate batch references
    for batch_path in batches:
        try:
            batch = load_batch_config(batch_path)
            batch_conditions = batch.get("conditions", [])
            batch_tasks = batch.get("tasks", [])

            # Check conditions exist (handle both name and path formats)
            for cond_ref in batch_conditions:
                # Could be "motivation" or "conditions/motivation.md"
                cond_name = Path(cond_ref).stem
                cond_found = any([
                    (conditions_dir / f"{cond_name}.md").exists(),
                    (exp_path / cond_ref).exists(),  # Full relative path
                ])
                if cond_found:
                    passes.append(f"Batch '{batch_path.stem}' condition '{cond_name}' exists")
                else:
                    errors.append(f"Batch '{batch_path.stem}' references missing condition: {cond_ref}")

            # Check tasks exist (handle both name and path formats)
            for task_ref in batch_tasks:
                # Could be "astropy-13033" or "tasks/pilot/astropy-13033.yaml"
                task_name = Path(task_ref).stem
                task_found = any([
                    (tasks_dir / f"{task_name}.yaml").exists(),
                    (exp_path / task_ref).exists(),  # Full relative path
                    list(tasks_dir.rglob(f"*{task_name}*.yaml")),
                ])
                if task_found:
                    passes.append(f"Batch '{batch_path.stem}' task '{task_name}' exists")
                else:
                    errors.append(f"Batch '{batch_path.stem}' references missing task: {task_ref}")

        except Exception as e:
            errors.append(f"Batch '{batch_path.stem}' invalid: {e}")

    # Report
    for p in passes:
        console.print(f"[green][PASS][/green] {p}")
    for w in warnings:
        console.print(f"[yellow][WARN][/yellow] {w}")
    for e in errors:
        console.print(f"[red][FAIL][/red] {e}")

    console.print(f"\nValidation complete: {len(passes)} passed, {len(warnings)} warnings, {len(errors)} errors")

    if errors or (strict and warnings):
        raise click.ClickException("Validation failed.")


# --- Batch Commands ---


@cli.group()
def batch():
    """Manage experiment batches."""
    pass


@batch.command("list")
@click.option("-e", "--experiment", "exp_name", help="Experiment name")
@click.pass_context
def batch_list(ctx: click.Context, exp_name: Optional[str]):
    """List batches in an experiment."""
    exp_path = resolve_experiment(exp_name)
    batches = list_batches(exp_path)

    if not batches:
        console.print(f"[yellow]No batches found in {exp_path.name}[/yellow]")
        return

    if ctx.obj.get("json"):
        data = []
        for batch_path in batches:
            config = load_batch_config(batch_path)
            data.append({
                "name": batch_path.stem,
                "tasks": len(config.get("tasks", [])),
                "conditions": len(config.get("conditions", [])),
                "runs_per_condition": config.get("runs_per_condition", 3),
            })
        console.print(json.dumps(data, indent=2))
        return

    table = Table(title=f"Batches in {exp_path.name}")
    table.add_column("BATCH", style="cyan")
    table.add_column("TASKS", justify="right")
    table.add_column("CONDITIONS", justify="right")
    table.add_column("RUNS/COND", justify="right")
    table.add_column("TOTAL RUNS", justify="right")

    for batch_path in batches:
        config = load_batch_config(batch_path)
        tasks = len(config.get("tasks", []))
        conditions = len(config.get("conditions", []))
        runs = config.get("runs_per_condition", 3)
        total = tasks * conditions * runs

        table.add_row(
            batch_path.stem,
            str(tasks),
            str(conditions),
            str(runs),
            str(total),
        )

    console.print(table)


@batch.command("show")
@click.argument("name")
@click.option("-e", "--experiment", "exp_name", help="Experiment name")
@click.pass_context
def batch_show(ctx: click.Context, name: str, exp_name: Optional[str]):
    """Show batch configuration details."""
    exp_path = resolve_experiment(exp_name)

    # Find batch file
    batch_path = None
    for dir_name in ["batches", "scenarios"]:
        candidate = exp_path / dir_name / f"{name}.yaml"
        if candidate.exists():
            batch_path = candidate
            break

    if not batch_path:
        raise click.UsageError(f"Batch '{name}' not found in {exp_path.name}")

    config = load_batch_config(batch_path)

    if ctx.obj.get("json"):
        console.print(json.dumps(config, indent=2))
        return

    # Rich output
    batch_name = config.get("name", f"{exp_path.name}-{name}")
    console.print(f"\n[bold cyan]Batch: {batch_name}[/bold cyan]")
    console.print("─" * 40)

    tasks = config.get("tasks", [])
    console.print(f"\n[bold]Tasks ({len(tasks)}):[/bold]")
    for t in tasks:
        console.print(f"  • {t}")

    conditions = config.get("conditions", [])
    console.print(f"\n[bold]Conditions ({len(conditions)}):[/bold]")
    for c in conditions:
        console.print(f"  • {c}")

    console.print(f"\n[bold]Configuration:[/bold]")
    console.print(f"  runs_per_condition: {config.get('runs_per_condition', 3)}")
    console.print(f"  model: {config.get('model', 'sonnet')}")

    iteration = config.get("iteration", {})
    if iteration:
        console.print(f"  iteration_strategy: {iteration.get('strategy', 'none')}")
        console.print(f"  max_iterations: {iteration.get('max_iterations', 1)}")

    total = len(tasks) * len(conditions) * config.get("runs_per_condition", 3)
    console.print(f"\n[bold]Expected:[/bold] {total} total runs\n")


@batch.command("run")
@click.argument("name")
@click.option("-e", "--experiment", "exp_name", help="Experiment name")
@click.option("--model", help="Override model")
@click.option("--runs", type=int, help="Override runs_per_condition")
@click.option("-n", "--dry-run", is_flag=True, help="Show run plan without executing")
@click.option("--resume", is_flag=True, help="Resume from previous partial run")
@click.option("--tracer", type=click.Choice(["phoenix", "console", "noop"]), default="console", help="Tracing backend")
@click.option("--grader", type=click.Choice(["mock", "swebench", "function"]), default="swebench", help="Grading backend")
def batch_run(
    name: str,
    exp_name: Optional[str],
    model: Optional[str],
    runs: Optional[int],
    dry_run: bool,
    resume: bool,
    tracer: str,
    grader: str,
):
    """Execute a batch using the hexagonal architecture.

    Examples:
        lab batch run pilot -e rep-002
        lab batch run pilot -e rep-002 --tracer phoenix
        lab batch run pilot -e rep-002 --dry-run
    """
    exp_path = resolve_experiment(exp_name)

    # Find batch file
    batch_path = None
    for dir_name in ["batches", "scenarios"]:
        candidate = exp_path / dir_name / f"{name}.yaml"
        if candidate.exists():
            batch_path = candidate
            break

    if not batch_path:
        raise click.UsageError(f"Batch '{name}' not found in {exp_path.name}")

    log.info(f"Starting batch: {exp_path.name}/{name}")

    # Create container with adapters
    from .container import Container
    from .ports.driving.use_cases import RunExperimentInput

    container = Container.create(
        tracer=tracer,  # type: ignore
        grader=grader,  # type: ignore
        results_dir=exp_path / "results",
        working_dir=exp_path,
        verbose=True,
    )

    # Load batch to show dry-run info
    load_use_case = container.load_batch_use_case()
    batch = load_use_case.execute(batch_path)

    if dry_run:
        console.print(f"\n[bold cyan]Batch: {batch.name}[/bold cyan]")
        console.print(f"Tasks: {len(batch.tasks)}")
        console.print(f"Conditions: {len(batch.conditions)}")
        console.print(f"Runs per condition: {batch.runs_per_condition}")
        console.print(f"[bold]Total runs: {batch.total_runs}[/bold]")
        console.print(f"\n[dim]Add --no-dry-run to execute[/dim]")
        return

    # Execute the batch
    run_use_case = container.run_experiment_use_case()
    input_data = RunExperimentInput(
        batch_path=batch_path,
        resume=resume,
    )

    # Run asynchronously
    async def run():
        completed = 0
        passed = 0
        with console.status("[bold green]Running experiment...") as status:
            async for result in run_use_case.execute(input_data):
                completed += 1
                if result.passed:
                    passed += 1
                status.update(f"[bold green]Running... {completed}/{batch.total_runs} ({passed} passed)")
                log.debug(f"Run complete: {result.task_id}/{result.condition_name} - {'PASS' if result.passed else 'FAIL'}")

        console.print(f"\n[bold green]Batch complete![/bold green]")
        console.print(f"Completed: {completed}")
        console.print(f"Passed: {passed} ({passed/completed*100:.1f}%)" if completed > 0 else "")

    asyncio.run(run())


@batch.command("validate")
@click.argument("name")
@click.option("-e", "--experiment", "exp_name", help="Experiment name")
def batch_validate(name: str, exp_name: Optional[str]):
    """Validate batch configuration."""
    exp_path = resolve_experiment(exp_name)

    # Find batch file
    batch_path = None
    for dir_name in ["batches", "scenarios"]:
        candidate = exp_path / dir_name / f"{name}.yaml"
        if candidate.exists():
            batch_path = candidate
            break

    if not batch_path:
        raise click.UsageError(f"Batch '{name}' not found in {exp_path.name}")

    console.print(f"Validating batch: [cyan]{name}[/cyan]\n")

    errors = []
    passes = []

    try:
        config = load_batch_config(batch_path)
        passes.append("Batch config is valid YAML")
    except Exception as e:
        errors.append(f"Invalid YAML: {e}")
        for e_msg in errors:
            console.print(f"[red][FAIL][/red] {e_msg}")
        raise click.ClickException("Validation failed.")

    # Check conditions exist
    conditions_dir = exp_path / "conditions"
    for cond_name in config.get("conditions", []):
        cond_path = conditions_dir / f"{cond_name}.md"
        if cond_path.exists():
            passes.append(f"Condition '{cond_name}' exists")
        else:
            errors.append(f"Missing condition: {cond_name}")

    # Check tasks exist
    tasks_dir = exp_path / "tasks"
    for task_ref in config.get("tasks", []):
        task_found = any([
            (tasks_dir / f"{task_ref}.yaml").exists(),
            (tasks_dir / task_ref).exists(),
            list(tasks_dir.rglob(f"*{task_ref}*.yaml")),
        ])
        if task_found:
            passes.append(f"Task '{task_ref}' exists")
        else:
            errors.append(f"Missing task: {task_ref}")

    # Report
    for p in passes:
        console.print(f"[green][PASS][/green] {p}")
    for e_msg in errors:
        console.print(f"[red][FAIL][/red] {e_msg}")

    if errors:
        raise click.ClickException("Validation failed.")

    console.print(f"\n[green]Ready to run:[/green] lab batch run {name} -e {exp_path.name}")


@batch.command("new")
@click.argument("name")
@click.option("-e", "--experiment", "exp_name", help="Experiment name")
@click.option("--tasks", help="Task selection pattern")
@click.option("--conditions", help="Condition selection (all or comma-separated)")
@click.option("--runs", type=int, default=3, help="Runs per condition")
def batch_new(
    name: str,
    exp_name: Optional[str],
    tasks: Optional[str],
    conditions: Optional[str],
    runs: int,
):
    """Create a new batch configuration."""
    exp_path = resolve_experiment(exp_name)

    # Determine batch directory
    batch_dir = exp_path / "batches"
    if not batch_dir.exists():
        batch_dir = exp_path / "scenarios"
    batch_dir.mkdir(exist_ok=True)

    batch_path = batch_dir / f"{name}.yaml"
    if batch_path.exists():
        raise click.UsageError(f"Batch '{name}' already exists.")

    # Resolve conditions
    conditions_dir = exp_path / "conditions"
    if conditions == "all" or not conditions:
        cond_list = [c.stem for c in conditions_dir.glob("*.md")]
    else:
        cond_list = [c.strip() for c in conditions.split(",")]

    # Resolve tasks
    tasks_dir = exp_path / "tasks"
    if tasks:
        # Pattern matching (simple for now)
        if tasks == "all":
            task_list = [t.stem for t in tasks_dir.rglob("*.yaml")]
        elif "*" in tasks:
            # Glob pattern
            task_list = [t.stem for t in tasks_dir.glob(f"{tasks}.yaml")]
        else:
            task_list = [t.strip() for t in tasks.split(",")]
    else:
        task_list = [t.stem for t in tasks_dir.rglob("*.yaml")]

    config = {
        "name": f"{exp_path.name}-{name}",
        "tasks": task_list,
        "conditions": cond_list,
        "model": "sonnet",
        "runs_per_condition": runs,
        "iteration": {
            "strategy": "none",
            "max_iterations": 1,
        },
    }

    with open(batch_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    console.print(f"[green]Created:[/green] {batch_path.relative_to(get_lab_root())}")


# --- Condition Commands ---


@cli.group()
def condition():
    """Manage experimental conditions."""
    pass


@condition.command("list")
@click.option("-e", "--experiment", "exp_name", help="Experiment name")
@click.pass_context
def condition_list(ctx: click.Context, exp_name: Optional[str]):
    """List conditions in an experiment."""
    exp_path = resolve_experiment(exp_name)
    conditions_dir = exp_path / "conditions"

    if not conditions_dir.exists():
        console.print(f"[yellow]No conditions found in {exp_path.name}[/yellow]")
        return

    conditions = []
    for cond_path in sorted(conditions_dir.glob("*.md")):
        cond = load_condition(cond_path)
        conditions.append({
            "name": cond_path.stem,
            "type": cond.get("type", ""),
            "description": cond.get("description", ""),
        })

    if ctx.obj.get("json"):
        console.print(json.dumps(conditions, indent=2))
        return

    table = Table(title=f"Conditions in {exp_path.name}")
    table.add_column("CONDITION", style="cyan")
    table.add_column("TYPE")
    table.add_column("DESCRIPTION")

    for cond in conditions:
        table.add_row(
            cond["name"],
            cond["type"],
            cond["description"][:50] + "..." if len(cond["description"]) > 50 else cond["description"],
        )

    console.print(table)


@condition.command("show")
@click.argument("name")
@click.option("-e", "--experiment", "exp_name", help="Experiment name")
@click.pass_context
def condition_show(ctx: click.Context, name: str, exp_name: Optional[str]):
    """Show condition details including full prompt."""
    exp_path = resolve_experiment(exp_name)
    cond_path = exp_path / "conditions" / f"{name}.md"

    if not cond_path.exists():
        raise click.UsageError(f"Condition '{name}' not found in {exp_path.name}")

    cond = load_condition(cond_path)

    if ctx.obj.get("json"):
        console.print(json.dumps(cond, indent=2))
        return

    console.print(f"\n[bold cyan]Condition: {name}[/bold cyan]")
    console.print("─" * 40)
    console.print(f"[bold]Type:[/bold] {cond.get('type', 'unknown')}")

    if cond.get("description"):
        console.print(f"\n[bold]Description:[/bold]\n  {cond['description']}")

    if cond.get("prompt"):
        console.print(f"\n[bold]Prompt:[/bold]")
        console.print(Panel(cond["prompt"][:500] + ("..." if len(cond["prompt"]) > 500 else "")))


@condition.command("validate")
@click.argument("name", required=False)
@click.option("-e", "--experiment", "exp_name", help="Experiment name")
def condition_validate(name: Optional[str], exp_name: Optional[str]):
    """Validate condition(s)."""
    exp_path = resolve_experiment(exp_name)
    conditions_dir = exp_path / "conditions"

    if name:
        cond_paths = [conditions_dir / f"{name}.md"]
        if not cond_paths[0].exists():
            raise click.UsageError(f"Condition '{name}' not found")
    else:
        cond_paths = list(conditions_dir.glob("*.md"))

    console.print("Validating conditions...\n")

    errors = []
    passes = []

    for cond_path in cond_paths:
        try:
            cond = load_condition(cond_path)
            if cond.get("prompt"):
                passes.append(f"{cond_path.stem}: valid frontmatter, has prompt")
            else:
                errors.append(f"{cond_path.stem}: missing prompt content")
        except Exception as e:
            errors.append(f"{cond_path.stem}: {e}")

    for p in passes:
        console.print(f"[green][PASS][/green] {p}")
    for e_msg in errors:
        console.print(f"[red][FAIL][/red] {e_msg}")

    console.print(f"\nAll {len(passes)} conditions valid." if not errors else "")

    if errors:
        raise click.ClickException("Validation failed.")


# --- Task Commands ---


@cli.group()
def task():
    """Manage experiment tasks."""
    pass


@task.command("list")
@click.option("-e", "--experiment", "exp_name", help="Experiment name")
@click.pass_context
def task_list(ctx: click.Context, exp_name: Optional[str]):
    """List tasks in an experiment."""
    exp_path = resolve_experiment(exp_name)
    tasks_dir = exp_path / "tasks"

    if not tasks_dir.exists():
        console.print(f"[yellow]No tasks found in {exp_path.name}[/yellow]")
        return

    tasks = []
    for task_path in sorted(tasks_dir.rglob("*.yaml")):
        try:
            with open(task_path) as f:
                task_data = yaml.safe_load(f)
            tasks.append({
                "name": task_path.stem,
                "path": str(task_path.relative_to(tasks_dir)),
                "difficulty": task_data.get("difficulty", ""),
                "description": task_data.get("description", "")[:50],
            })
        except Exception:
            tasks.append({"name": task_path.stem, "path": str(task_path.relative_to(tasks_dir)), "difficulty": "", "description": "Error loading"})

    if ctx.obj.get("json"):
        console.print(json.dumps(tasks, indent=2))
        return

    table = Table(title=f"Tasks in {exp_path.name}")
    table.add_column("TASK", style="cyan")
    table.add_column("PATH")
    table.add_column("DIFFICULTY")
    table.add_column("DESCRIPTION")

    for t in tasks:
        table.add_row(t["name"], t["path"], t["difficulty"], t["description"])

    console.print(table)


@task.command("show")
@click.argument("name")
@click.option("-e", "--experiment", "exp_name", help="Experiment name")
@click.pass_context
def task_show(ctx: click.Context, name: str, exp_name: Optional[str]):
    """Show task details."""
    exp_path = resolve_experiment(exp_name)
    tasks_dir = exp_path / "tasks"

    # Find task (may be nested)
    task_path = None
    for candidate in tasks_dir.rglob(f"*{name}*.yaml"):
        task_path = candidate
        break

    if not task_path:
        raise click.UsageError(f"Task '{name}' not found in {exp_path.name}")

    with open(task_path) as f:
        task_data = yaml.safe_load(f)

    if ctx.obj.get("json"):
        console.print(json.dumps(task_data, indent=2))
        return

    console.print(f"\n[bold cyan]Task: {task_path.stem}[/bold cyan]")
    console.print("─" * 40)

    for key in ["repo", "repository", "difficulty", "description"]:
        if key in task_data:
            console.print(f"[bold]{key.title()}:[/bold] {task_data[key]}")

    if "problem_statement" in task_data:
        console.print(f"\n[bold]Problem:[/bold]")
        console.print(Panel(task_data["problem_statement"][:500] + ("..." if len(task_data.get("problem_statement", "")) > 500 else "")))

    if "hints" in task_data:
        console.print(f"\n[bold]Hints:[/bold]\n  {task_data['hints']}")


@task.command("validate")
@click.argument("name", required=False)
@click.option("-e", "--experiment", "exp_name", help="Experiment name")
def task_validate(name: Optional[str], exp_name: Optional[str]):
    """Validate task(s)."""
    exp_path = resolve_experiment(exp_name)
    tasks_dir = exp_path / "tasks"

    if name:
        task_paths = list(tasks_dir.rglob(f"*{name}*.yaml"))
        if not task_paths:
            raise click.UsageError(f"Task '{name}' not found")
    else:
        task_paths = list(tasks_dir.rglob("*.yaml"))

    console.print("Validating tasks...\n")

    errors = []
    passes = []

    for task_path in task_paths:
        try:
            with open(task_path) as f:
                task_data = yaml.safe_load(f)
            if task_data:
                passes.append(f"{task_path.stem}: valid YAML")
            else:
                errors.append(f"{task_path.stem}: empty file")
        except Exception as e:
            errors.append(f"{task_path.stem}: {e}")

    for p in passes:
        console.print(f"[green][PASS][/green] {p}")
    for e_msg in errors:
        console.print(f"[red][FAIL][/red] {e_msg}")

    console.print(f"\nAll {len(passes)} tasks valid." if not errors else "")

    if errors:
        raise click.ClickException("Validation failed.")


# --- Result Commands ---


@cli.group()
def result():
    """Manage experiment results."""
    pass


@result.command("list")
@click.option("-e", "--experiment", "exp_name", help="Experiment name")
@click.pass_context
def result_list(ctx: click.Context, exp_name: Optional[str]):
    """List result files."""
    exp_path = resolve_experiment(exp_name)
    results_dir = exp_path / "results"

    if not results_dir.exists() or not list(results_dir.glob("*.json")):
        console.print(f"[yellow]No results found in {exp_path.name}[/yellow]")
        return

    results = []
    for result_path in sorted(results_dir.glob("*.json"), reverse=True):
        try:
            with open(result_path) as f:
                data = json.load(f)
            results.append({
                "file": result_path.name,
                "date": result_path.stat().st_mtime,
            })
        except Exception:
            results.append({"file": result_path.name, "date": 0})

    if ctx.obj.get("json"):
        console.print(json.dumps(results, indent=2))
        return

    table = Table(title=f"Results in {exp_path.name}")
    table.add_column("FILE", style="cyan")
    table.add_column("DATE")

    for r in results:
        date_str = datetime.fromtimestamp(r["date"]).strftime("%Y-%m-%d %H:%M") if r["date"] else ""
        table.add_row(r["file"], date_str)

    console.print(table)


@result.command("show")
@click.argument("file")
@click.option("-e", "--experiment", "exp_name", help="Experiment name")
@click.pass_context
def result_show(ctx: click.Context, file: str, exp_name: Optional[str]):
    """Show result summary."""
    # Try to find file
    file_path = Path(file)
    if not file_path.exists():
        exp_path = resolve_experiment(exp_name)
        file_path = exp_path / "results" / file

    if not file_path.exists():
        raise click.UsageError(f"Result file not found: {file}")

    with open(file_path) as f:
        data = json.load(f)

    if ctx.obj.get("json"):
        console.print(json.dumps(data, indent=2))
        return

    console.print(f"\n[bold cyan]Results: {file_path.stem}[/bold cyan]")
    console.print("─" * 40)
    console.print(json.dumps(data, indent=2)[:1000])


@result.command("verify")
@click.argument("file", type=click.Path(exists=True))
@click.option("--model", default="gpt-4o-mini", help="Verifier model")
def result_verify(file: str, model: str):
    """Verify experiment claims with Strawberry."""
    from .analyst import analyze_results

    results_path = Path(file)
    log.info(f"Verifying: {results_path}")

    report = analyze_results(
        results_path=results_path,
        verify=True,
        verifier_model=model,
    )

    verified = sum(1 for c in report.claims if c.verified)
    total = len(report.claims)
    console.print(f"\n[green]Verification complete:[/green] {verified}/{total} claims verified")


# --- Report Commands ---


@cli.group()
def report():
    """Generate reports."""
    pass


@report.command("generate")
@click.argument("analysis_file", type=click.Path(exists=True))
@click.option("-o", "--output", "output_path", type=click.Path(), help="Output HTML path")
@click.option("--open", "open_browser", is_flag=True, help="Open in browser")
def report_generate(analysis_file: str, output_path: Optional[str], open_browser: bool):
    """Generate HTML report from analysis markdown."""
    from .reporter import generate_report

    analysis_path = Path(analysis_file)
    out = Path(output_path) if output_path else None

    log.info(f"Generating report from: {analysis_path}")

    html_path = generate_report(
        analysis_path=analysis_path,
        output_path=out,
    )

    console.print(f"\n[green]Report ready:[/green] {html_path}")

    if open_browser:
        import webbrowser
        webbrowser.open(f"file://{html_path.resolve()}")


# --- Observe Commands ---


@cli.group()
def observe():
    """Observability tools."""
    pass


@observe.command("phoenix")
@click.option("--port", default=6006, help="Port number")
@click.option("--no-browser", is_flag=True, help="Don't open browser")
def observe_phoenix(port: int, no_browser: bool):
    """Launch Phoenix UI for trace visualization."""
    try:
        import phoenix as px
        console.print("[cyan]Launching Phoenix UI...[/cyan]")
        px.launch_app(port=port)
        console.print(f"[green]Phoenix running at:[/green] http://localhost:{port}")
        console.print("[dim]Press Ctrl+C to stop[/dim]")

        import time
        while True:
            time.sleep(1)
    except ImportError:
        console.print("[red]Phoenix not installed.[/red] Run: uv add arize-phoenix")
    except KeyboardInterrupt:
        console.print("\n[yellow]Phoenix stopped.[/yellow]")


# --- Legacy Commands (backward compatibility) ---


@cli.command("ls", hidden=True)
def legacy_ls():
    """[Legacy] List experiments. Use 'lab experiment list' instead."""
    console.print("[yellow]Deprecated:[/yellow] Use 'lab experiment list'")
    ctx = click.Context(experiment_list)
    ctx.ensure_object(dict)
    ctx.obj["json"] = False
    ctx.invoke(experiment_list)


# --- Main Entry Point ---


def main():
    """Main entry point for the CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()
