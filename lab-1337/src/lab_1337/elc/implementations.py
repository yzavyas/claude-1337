"""IMP (Implementation Plan) management."""

import re
from datetime import date
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich.panel import Panel

from lab_1337.elc.models import IMP, EnhancementStatus, status_color
from lab_1337.elc.proposals import get_lep, PROPOSALS_DIR, EXPERIMENTS_DIR

console = Console()

ROOT_DIR = Path(__file__).parent.parent.parent.parent
IMPLEMENTATIONS_DIR = ROOT_DIR / "implementations"
TEMPLATE_PATH = IMPLEMENTATIONS_DIR / "TEMPLATE.md"


def parse_imp_from_file(path: Path) -> Optional[IMP]:
    """Parse IMP metadata from markdown file."""
    content = path.read_text()

    # Parse number from filename
    match = re.search(r"imp-(\d+)", path.name)
    if not match:
        return None
    number = match.group(1)

    # Parse title
    title_match = re.search(r"^#\s+IMP-\d+:\s*(.+)$", content, re.MULTILINE)
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

    # Parse LEP reference
    lep_match = re.search(r"\*\*LEP\*\*:.*?LEP-(\d+)", content)
    lep_ref = lep_match.group(1) if lep_match else number

    return IMP(
        number=number,
        title=title,
        status=status,
        created=created,
        lep_ref=lep_ref,
        path=path,
    )


def get_all_imps() -> list[IMP]:
    """Get all IMPs from implementations directory."""
    imps = []
    if not IMPLEMENTATIONS_DIR.exists():
        return imps
    for path in sorted(IMPLEMENTATIONS_DIR.glob("imp-*.md")):
        imp = parse_imp_from_file(path)
        if imp:
            imps.append(imp)
    return imps


def get_imp(number: str) -> Optional[IMP]:
    """Get a specific IMP by number."""
    number = f"{int(number.lstrip('0') or '0'):03d}"
    for imp in get_all_imps():
        if imp.number == number:
            return imp
    return None


def update_status_in_file(path: Path, new_status: EnhancementStatus) -> bool:
    """Update status in IMP file."""
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
@click.group("imp")
def imp():
    """Manage Implementation Plans (IMPs)."""
    pass


@imp.command("new")
@click.argument("lep_number")
@click.option("--author", "-a", help="Author name(s)")
def new_imp(lep_number: str, author: Optional[str]):
    """Create a new IMP for an accepted LEP."""
    lep = get_lep(lep_number)
    if not lep:
        console.print(f"[red]LEP-{lep_number} not found[/red]")
        raise SystemExit(1)

    if lep.status != EnhancementStatus.ACCEPTED:
        console.print(f"[yellow]Warning: LEP-{lep.number} is {lep.status.value}, not accepted[/yellow]")
        console.print("[dim]IMPs are typically created for accepted LEPs[/dim]")

    # Check if IMP already exists
    existing = get_imp(lep.number)
    if existing:
        console.print(f"[yellow]IMP-{lep.number} already exists[/yellow]")
        console.print(f"[dim]{existing.path}[/dim]")
        raise SystemExit(1)

    if not TEMPLATE_PATH.exists():
        console.print("[red]Template not found at implementations/TEMPLATE.md[/red]")
        raise SystemExit(1)

    template = TEMPLATE_PATH.read_text()
    today = date.today().isoformat()

    # Create IMP with same number as LEP
    imp_model = IMP(
        number=lep.number,
        title=lep.title,
        lep_ref=lep.number,
        authors=[author] if author else [],
    )

    # Fill in template
    content = template.replace("IMP-NNN", f"IMP-{lep.number}")
    content = content.replace(": Title", f": {lep.title}")
    content = content.replace("YYYY-MM-DD", today)
    content = content.replace(
        "[LEP-NNN](../proposals/lep-nnn-slug.md)",
        f"[LEP-{lep.number}](../proposals/{lep.filename})"
    )
    if author:
        content = re.sub(r"(\*\*Authors\*\*:)\s*", f"\\1 {author}", content)

    # Write file
    IMPLEMENTATIONS_DIR.mkdir(exist_ok=True)
    filepath = IMPLEMENTATIONS_DIR / imp_model.filename
    filepath.write_text(content)

    console.print(f"[green]Created:[/green] {filepath.name}")
    console.print(f"[dim]Linked to: LEP-{lep.number} ({lep.title})[/dim]")
    console.print(f"\n[cyan]When ready, scaffold experiment:[/cyan]")
    console.print(f"  lab-1337 experiment new {lep.number}")


@imp.command("list")
@click.option("--status", "-s", type=click.Choice([s.value for s in EnhancementStatus]), help="Filter by status")
def list_imps(status: Optional[str]):
    """List all IMPs."""
    imps = get_all_imps()

    if status:
        imps = [i for i in imps if i.status.value == status]

    if not imps:
        console.print("[yellow]No implementation plans found.[/yellow]")
        return

    table = Table(title="Implementation Plans")
    table.add_column("IMP", style="cyan", width=6)
    table.add_column("Title", style="white")
    table.add_column("Status", width=12)
    table.add_column("LEP", width=6)

    for imp_item in imps:
        color = status_color(imp_item.status)
        table.add_row(
            imp_item.number,
            imp_item.title[:45],
            f"[{color}]{imp_item.status.value}[/{color}]",
            imp_item.lep_ref,
        )

    console.print(table)


@imp.command("show")
@click.argument("number")
def show_imp(number: str):
    """Show a specific IMP."""
    imp_item = get_imp(number)
    if not imp_item:
        console.print(f"[red]IMP-{number} not found[/red]")
        raise SystemExit(1)

    content = imp_item.path.read_text()
    color = status_color(imp_item.status)

    # Get linked LEP
    lep = get_lep(imp_item.lep_ref)
    lep_status = f"[{status_color(lep.status)}]{lep.status.value}[/{status_color(lep.status)}]" if lep else "missing"

    console.print(Panel(
        f"[bold]IMP-{imp_item.number}:[/bold] {imp_item.title}\n"
        f"[{color}]Status: {imp_item.status.value}[/{color}] | "
        f"LEP-{imp_item.lep_ref}: {lep_status}",
        title="Implementation Plan",
    ))

    console.print(Markdown(content))


@imp.command("status")
@click.argument("number")
@click.argument("new_status", type=click.Choice([s.value for s in EnhancementStatus]))
def set_status(number: str, new_status: str):
    """Update IMP status."""
    imp_item = get_imp(number)
    if not imp_item:
        console.print(f"[red]IMP-{number} not found[/red]")
        raise SystemExit(1)

    target_status = EnhancementStatus(new_status)
    old_status = imp_item.status

    if old_status == target_status:
        console.print(f"[yellow]IMP-{number} is already {target_status.value}[/yellow]")
        return

    if update_status_in_file(imp_item.path, target_status):
        console.print(
            f"[dim]IMP-{imp_item.number}: {imp_item.title}[/dim]\n"
            f"[{status_color(old_status)}]{old_status.value}[/{status_color(old_status)}] → "
            f"[{status_color(target_status)}]{target_status.value}[/{status_color(target_status)}]"
        )
