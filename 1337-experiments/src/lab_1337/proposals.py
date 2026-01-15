"""Proposal lifecycle management."""

import re
from datetime import date
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

PROPOSALS_DIR = Path(__file__).parent.parent.parent / "proposals"
TEMPLATE_PATH = PROPOSALS_DIR / "TEMPLATE.md"

STATUSES = ["draft", "discussion", "fcp", "accepted", "rejected", "postponed", "implemented"]

STATUS_COLORS = {
    "draft": "dim",
    "discussion": "cyan",
    "fcp": "yellow",
    "accepted": "green",
    "rejected": "red",
    "postponed": "dim yellow",
    "implemented": "bold green",
}


def get_proposals() -> list[dict]:
    """Get all proposals with parsed metadata."""
    proposals = []

    for path in sorted(PROPOSALS_DIR.glob("lep-*.md")):
        content = path.read_text()

        # Parse LEP number from filename
        match = re.search(r"lep-(\d+)", path.name)
        if not match:
            continue
        lep_num = match.group(1)

        # Parse title from first heading
        title_match = re.search(r"^#\s+LEP-\d+:\s*(.+)$", content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else "Untitled"

        # Parse status
        status_match = re.search(r"\*\*Status\*\*:\s*(\w+)", content)
        status = status_match.group(1).lower() if status_match else "draft"

        # Parse created date
        created_match = re.search(r"\*\*Created\*\*:\s*([\d-]+)", content)
        created = created_match.group(1) if created_match else "unknown"

        # Parse authors
        authors_match = re.search(r"\*\*Authors\*\*:\s*(.+?)(?:\n|$)", content)
        authors = authors_match.group(1).strip() if authors_match else ""

        proposals.append({
            "number": lep_num,
            "title": title,
            "status": status,
            "created": created,
            "authors": authors,
            "path": path,
        })

    return proposals


def get_next_number() -> str:
    """Get the next available LEP number."""
    proposals = get_proposals()
    if not proposals:
        return "001"

    max_num = max(int(p["number"]) for p in proposals)
    return f"{max_num + 1:03d}"


def update_status(path: Path, new_status: str) -> bool:
    """Update the status in a proposal file."""
    content = path.read_text()

    # Replace status line
    new_content = re.sub(
        r"(\*\*Status\*\*:\s*)\w+",
        f"\\1{new_status.capitalize()}",
        content
    )

    if new_content == content:
        return False

    path.write_text(new_content)
    return True


@click.group()
def proposal():
    """Manage Lab Enhancement Proposals (LEPs)."""
    pass


@proposal.command("new")
@click.argument("title")
@click.option("--author", "-a", help="Author name(s)")
def new_proposal(title: str, author: Optional[str]):
    """Create a new proposal from template."""
    if not TEMPLATE_PATH.exists():
        console.print("[red]Template not found at proposals/TEMPLATE.md[/red]")
        raise SystemExit(1)

    template = TEMPLATE_PATH.read_text()
    lep_num = get_next_number()
    today = date.today().isoformat()

    # Fill in template
    content = template.replace("LEP-NNN", f"LEP-{lep_num}")
    content = content.replace("Title", title)
    content = content.replace("YYYY-MM-DD", today)
    if author:
        content = re.sub(r"(\*\*Authors\*\*:)\s*", f"\\1 {author}", content)

    # Write file
    filename = f"lep-{lep_num}-{title.lower().replace(' ', '-')[:40]}.md"
    filepath = PROPOSALS_DIR / filename
    filepath.write_text(content)

    console.print(f"[green]Created:[/green] {filepath.name}")
    console.print(f"[dim]Edit the file to complete your proposal[/dim]")


@proposal.command("list")
@click.option("--status", "-s", type=click.Choice(STATUSES), help="Filter by status")
def list_proposals(status: Optional[str]):
    """List all proposals."""
    proposals = get_proposals()

    if status:
        proposals = [p for p in proposals if p["status"] == status]

    if not proposals:
        console.print("[yellow]No proposals found.[/yellow]")
        return

    table = Table(title="Lab Enhancement Proposals")
    table.add_column("LEP", style="cyan", width=6)
    table.add_column("Title", style="white")
    table.add_column("Status", width=12)
    table.add_column("Created", style="dim", width=12)

    for p in proposals:
        status_style = STATUS_COLORS.get(p["status"], "white")
        table.add_row(
            p["number"],
            p["title"][:50],
            f"[{status_style}]{p['status']}[/{status_style}]",
            p["created"],
        )

    console.print(table)


@proposal.command("show")
@click.argument("lep_number")
def show_proposal(lep_number: str):
    """Show a specific proposal."""
    # Normalize number
    lep_number = lep_number.lstrip("0") or "0"
    lep_number = f"{int(lep_number):03d}"

    proposals = get_proposals()
    proposal = next((p for p in proposals if p["number"] == lep_number), None)

    if not proposal:
        console.print(f"[red]LEP-{lep_number} not found[/red]")
        raise SystemExit(1)

    content = proposal["path"].read_text()

    # Show header with status
    status_style = STATUS_COLORS.get(proposal["status"], "white")
    console.print(Panel(
        f"[bold]LEP-{lep_number}:[/bold] {proposal['title']}\n"
        f"[{status_style}]Status: {proposal['status']}[/{status_style}] | "
        f"Created: {proposal['created']}",
        title="Proposal",
    ))

    # Show content
    console.print(Markdown(content))


@proposal.command("status")
@click.argument("lep_number")
@click.argument("new_status", type=click.Choice(STATUSES))
def set_status(lep_number: str, new_status: str):
    """Update proposal status."""
    lep_number = f"{int(lep_number.lstrip('0') or '0'):03d}"

    proposals = get_proposals()
    proposal = next((p for p in proposals if p["number"] == lep_number), None)

    if not proposal:
        console.print(f"[red]LEP-{lep_number} not found[/red]")
        raise SystemExit(1)

    old_status = proposal["status"]
    if old_status == new_status:
        console.print(f"[yellow]LEP-{lep_number} is already {new_status}[/yellow]")
        return

    if update_status(proposal["path"], new_status):
        console.print(
            f"[green]LEP-{lep_number}:[/green] "
            f"[{STATUS_COLORS[old_status]}]{old_status}[/{STATUS_COLORS[old_status]}] → "
            f"[{STATUS_COLORS[new_status]}]{new_status}[/{STATUS_COLORS[new_status]}]"
        )
    else:
        console.print("[red]Failed to update status[/red]")


@proposal.command("fcp")
@click.argument("lep_number")
def final_comment_period(lep_number: str):
    """Move proposal to Final Comment Period."""
    lep_number = f"{int(lep_number.lstrip('0') or '0'):03d}"

    proposals = get_proposals()
    proposal = next((p for p in proposals if p["number"] == lep_number), None)

    if not proposal:
        console.print(f"[red]LEP-{lep_number} not found[/red]")
        raise SystemExit(1)

    if proposal["status"] not in ["draft", "discussion"]:
        console.print(f"[yellow]LEP-{lep_number} cannot move to FCP from {proposal['status']}[/yellow]")
        return

    if update_status(proposal["path"], "fcp"):
        console.print(f"[yellow]LEP-{lep_number} is now in Final Comment Period[/yellow]")
        console.print("[dim]This is the last call for feedback before decision.[/dim]")


@proposal.command("accept")
@click.argument("lep_number")
def accept_proposal(lep_number: str):
    """Accept a proposal."""
    lep_number = f"{int(lep_number.lstrip('0') or '0'):03d}"

    proposals = get_proposals()
    proposal = next((p for p in proposals if p["number"] == lep_number), None)

    if not proposal:
        console.print(f"[red]LEP-{lep_number} not found[/red]")
        raise SystemExit(1)

    if update_status(proposal["path"], "accepted"):
        console.print(f"[green]LEP-{lep_number} accepted![/green]")
        console.print("[dim]Ready for implementation.[/dim]")


@proposal.command("reject")
@click.argument("lep_number")
def reject_proposal(lep_number: str):
    """Reject a proposal."""
    lep_number = f"{int(lep_number.lstrip('0') or '0'):03d}"

    proposals = get_proposals()
    proposal = next((p for p in proposals if p["number"] == lep_number), None)

    if not proposal:
        console.print(f"[red]LEP-{lep_number} not found[/red]")
        raise SystemExit(1)

    if update_status(proposal["path"], "rejected"):
        console.print(f"[red]LEP-{lep_number} rejected[/red]")


@proposal.command("implemented")
@click.argument("lep_number")
@click.option("--tracking", "-t", help="Link to implementation (experiment, PR, etc)")
def mark_implemented(lep_number: str, tracking: Optional[str]):
    """Mark a proposal as implemented."""
    lep_number = f"{int(lep_number.lstrip('0') or '0'):03d}"

    proposals = get_proposals()
    proposal = next((p for p in proposals if p["number"] == lep_number), None)

    if not proposal:
        console.print(f"[red]LEP-{lep_number} not found[/red]")
        raise SystemExit(1)

    if proposal["status"] != "accepted":
        console.print(f"[yellow]Warning: LEP-{lep_number} was not accepted (was {proposal['status']})[/yellow]")

    # Update status
    content = proposal["path"].read_text()
    content = re.sub(r"(\*\*Status\*\*:\s*)\w+", "\\1Implemented", content)

    # Add tracking link if provided
    if tracking:
        content = re.sub(
            r"(\*\*Tracking\*\*:).*?(?=\n)",
            f"\\1 {tracking}",
            content
        )

    proposal["path"].write_text(content)
    console.print(f"[bold green]LEP-{lep_number} implemented![/bold green]")
    if tracking:
        console.print(f"[dim]Tracking: {tracking}[/dim]")
