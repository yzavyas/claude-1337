"""LEP (Lab Enhancement Proposal) management."""

import re
from datetime import date
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich.panel import Panel

from lab_1337.elc.models import LEP, EnhancementStatus, status_color
from lab_1337.elc.machine import LifecycleMachine

console = Console()

# Paths relative to package
ROOT_DIR = Path(__file__).parent.parent.parent.parent
PROPOSALS_DIR = ROOT_DIR / "proposals"
IMPLEMENTATIONS_DIR = ROOT_DIR / "implementations"
EXPERIMENTS_DIR = ROOT_DIR / "experiments"
TEMPLATE_PATH = PROPOSALS_DIR / "TEMPLATE.md"


def parse_lep_from_file(path: Path) -> Optional[LEP]:
    """Parse LEP metadata from markdown file."""
    content = path.read_text()

    # Parse number from filename
    match = re.search(r"lep-(\d+)", path.name)
    if not match:
        return None
    number = match.group(1)

    # Parse title
    title_match = re.search(r"^#\s+LEP-\d+:\s*(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "Untitled"

    # Parse status
    status_match = re.search(r"\*\*Status\*\*:\s*(\w+)", content, re.IGNORECASE)
    status_str = status_match.group(1).lower() if status_match else "draft"
    try:
        status = EnhancementStatus(status_str)
    except ValueError:
        status = EnhancementStatus.DRAFT

    # Parse created date
    created_match = re.search(r"\*\*Created\*\*:\s*([\d-]+)", content)
    created_str = created_match.group(1) if created_match else None
    created = date.fromisoformat(created_str) if created_str else date.today()

    # Parse authors
    authors_match = re.search(r"\*\*Authors\*\*:\s*(.+?)(?:\n|$)", content)
    authors_str = authors_match.group(1).strip() if authors_match else ""
    authors = [a.strip() for a in authors_str.split(",") if a.strip()]

    return LEP(
        number=number,
        title=title,
        status=status,
        created=created,
        authors=authors,
        path=path,
    )


def get_all_leps() -> list[LEP]:
    """Get all LEPs from proposals directory."""
    leps = []
    for path in sorted(PROPOSALS_DIR.glob("lep-*.md")):
        lep = parse_lep_from_file(path)
        if lep:
            leps.append(lep)
    return leps


def get_lep(number: str) -> Optional[LEP]:
    """Get a specific LEP by number."""
    number = f"{int(number.lstrip('0') or '0'):03d}"
    for lep in get_all_leps():
        if lep.number == number:
            return lep
    return None


def get_next_number() -> str:
    """Get the next available LEP number."""
    leps = get_all_leps()
    if not leps:
        return "001"
    max_num = max(int(lep.number) for lep in leps)
    return f"{max_num + 1:03d}"


def update_status_in_file(path: Path, new_status: EnhancementStatus) -> bool:
    """Update status in LEP file."""
    content = path.read_text()
    new_content = re.sub(
        r"(\*\*Status\*\*:\s*)\w+",
        f"\\1{new_status.value.capitalize()}",
        content,
        flags=re.IGNORECASE,
    )
    if new_content == content:
        return False
    path.write_text(new_content)
    return True


# CLI Commands
@click.group("proposal")
def proposal():
    """Manage Lab Enhancement Proposals (LEPs)."""
    pass


@proposal.command("new")
@click.argument("title")
@click.option("--author", "-a", help="Author name(s)")
def new_proposal(title: str, author: Optional[str]):
    """Create a new LEP from template."""
    if not TEMPLATE_PATH.exists():
        console.print("[red]Template not found at proposals/TEMPLATE.md[/red]")
        raise SystemExit(1)

    template = TEMPLATE_PATH.read_text()
    number = get_next_number()
    today = date.today().isoformat()

    # Create LEP to get slug
    lep = LEP(number=number, title=title, authors=[author] if author else [])

    # Fill in template
    content = template.replace("LEP-NNN", f"LEP-{number}")
    content = content.replace(": Title", f": {title}")
    content = content.replace("YYYY-MM-DD", today)
    if author:
        content = re.sub(r"(\*\*Authors\*\*:)\s*", f"\\1 {author}", content)

    # Write file
    filepath = PROPOSALS_DIR / lep.filename
    filepath.write_text(content)

    console.print(f"[green]Created:[/green] {filepath.name}")
    console.print(f"[dim]Experiment will be: experiments/{lep.experiment_dirname}/[/dim]")


@proposal.command("list")
@click.option("--status", "-s", type=click.Choice([s.value for s in EnhancementStatus]), help="Filter by status")
def list_proposals(status: Optional[str]):
    """List all LEPs."""
    leps = get_all_leps()

    if status:
        leps = [l for l in leps if l.status.value == status]

    if not leps:
        console.print("[yellow]No proposals found.[/yellow]")
        return

    table = Table(title="Lab Enhancement Proposals")
    table.add_column("LEP", style="cyan", width=6)
    table.add_column("Title", style="white")
    table.add_column("Status", width=12)
    table.add_column("IMP", width=4)
    table.add_column("Exp", width=4)

    for lep in leps:
        color = status_color(lep.status)
        has_imp = "[green]yes[/green]" if lep.has_imp(IMPLEMENTATIONS_DIR) else "[dim]no[/dim]"
        has_exp = "[green]yes[/green]" if lep.has_experiment(EXPERIMENTS_DIR) else "[dim]no[/dim]"

        table.add_row(
            lep.number,
            lep.title[:45],
            f"[{color}]{lep.status.value}[/{color}]",
            has_imp,
            has_exp,
        )

    console.print(table)


@proposal.command("show")
@click.argument("number")
def show_proposal(number: str):
    """Show a specific LEP."""
    lep = get_lep(number)
    if not lep:
        console.print(f"[red]LEP-{number} not found[/red]")
        raise SystemExit(1)

    content = lep.path.read_text()
    color = status_color(lep.status)

    # Header panel
    has_imp = "yes" if lep.has_imp(IMPLEMENTATIONS_DIR) else "no"
    has_exp = "yes" if lep.has_experiment(EXPERIMENTS_DIR) else "no"

    console.print(Panel(
        f"[bold]LEP-{lep.number}:[/bold] {lep.title}\n"
        f"[{color}]Status: {lep.status.value}[/{color}] | "
        f"IMP: {has_imp} | Experiment: {has_exp}",
        title="Proposal",
    ))

    console.print(Markdown(content))


@proposal.command("status")
@click.argument("number")
@click.argument("new_status", type=click.Choice([s.value for s in EnhancementStatus]))
def set_status(number: str, new_status: str):
    """Update LEP status (validates transitions)."""
    lep = get_lep(number)
    if not lep:
        console.print(f"[red]LEP-{number} not found[/red]")
        raise SystemExit(1)

    target_status = EnhancementStatus(new_status)

    # Use state machine to validate transition
    def on_accept(event):
        console.print("\n[cyan]LEP accepted! Create implementation plan:[/cyan]")
        console.print(f"  lab-1337 imp new {lep.number}")

    machine = LifecycleMachine(
        initial_state=lep.status.value,
        on_accept=on_accept,
    )

    console.print(f"[dim]LEP-{lep.number}: {lep.title}[/dim]")

    if machine.transition_to(target_status):
        update_status_in_file(lep.path, target_status)


@proposal.command("fcp")
@click.argument("number")
def final_comment_period(number: str):
    """Move LEP to Final Comment Period."""
    lep = get_lep(number)
    if not lep:
        console.print(f"[red]LEP-{number} not found[/red]")
        raise SystemExit(1)

    machine = LifecycleMachine(initial_state=lep.status.value)
    console.print(f"[dim]LEP-{lep.number}: {lep.title}[/dim]")

    if machine.transition_to(EnhancementStatus.FCP):
        update_status_in_file(lep.path, EnhancementStatus.FCP)
        console.print("[yellow]This is the last call for feedback before decision.[/yellow]")


@proposal.command("accept")
@click.argument("number")
def accept_proposal(number: str):
    """Accept a LEP."""
    lep = get_lep(number)
    if not lep:
        console.print(f"[red]LEP-{number} not found[/red]")
        raise SystemExit(1)

    def on_accept(event):
        console.print("\n[cyan]Create implementation plan:[/cyan]")
        console.print(f"  lab-1337 imp new {lep.number}")

    machine = LifecycleMachine(
        initial_state=lep.status.value,
        on_accept=on_accept,
    )
    console.print(f"[dim]LEP-{lep.number}: {lep.title}[/dim]")

    if machine.transition_to(EnhancementStatus.ACCEPTED):
        update_status_in_file(lep.path, EnhancementStatus.ACCEPTED)


@proposal.command("reject")
@click.argument("number")
def reject_proposal(number: str):
    """Reject a LEP."""
    lep = get_lep(number)
    if not lep:
        console.print(f"[red]LEP-{number} not found[/red]")
        raise SystemExit(1)

    machine = LifecycleMachine(initial_state=lep.status.value)
    console.print(f"[dim]LEP-{lep.number}: {lep.title}[/dim]")

    if machine.transition_to(EnhancementStatus.REJECTED):
        update_status_in_file(lep.path, EnhancementStatus.REJECTED)


@proposal.command("implemented")
@click.argument("number")
@click.option("--tracking", "-t", help="Link to implementation")
def mark_implemented(number: str, tracking: Optional[str]):
    """Mark LEP as implemented."""
    lep = get_lep(number)
    if not lep:
        console.print(f"[red]LEP-{number} not found[/red]")
        raise SystemExit(1)

    # Check if experiment exists
    if not lep.has_experiment(EXPERIMENTS_DIR):
        console.print(f"[yellow]Warning: No experiment found at experiments/{lep.experiment_dirname}/[/yellow]")

    machine = LifecycleMachine(initial_state=lep.status.value)
    console.print(f"[dim]LEP-{lep.number}: {lep.title}[/dim]")

    if machine.transition_to(EnhancementStatus.IMPLEMENTED):
        content = lep.path.read_text()
        content = re.sub(
            r"(\*\*Status\*\*:\s*)\w+",
            "\\1Implemented",
            content,
            flags=re.IGNORECASE,
        )
        if tracking:
            content = re.sub(
                r"(\*\*Tracking\*\*:).*?(?=\n)",
                f"\\1 {tracking}",
                content,
            )
        lep.path.write_text(content)

        if tracking:
            console.print(f"[dim]Tracking: {tracking}[/dim]")
