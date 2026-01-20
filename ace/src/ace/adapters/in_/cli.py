"""ace CLI - Agentic Cognitive Extensions.

Discover, install, and manage cognitive extensions.

CLI Grammar:
- ace source add/rm/list  (noun-first subcommand group)
- ace install/uninstall/update/list/show  (verb-first actions)

This module is the COMPOSITION ROOT in hexagonal architecture:
- Creates concrete adapters
- Injects them into the application layer
- Handles CLI presentation
"""

import json
from importlib import resources
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ace import __version__
from ace.adapters.out.claude_code_target import ClaudeCodeTargetAdapter
from ace.adapters.out.filesystem_registry import FilesystemRegistryAdapter
from ace.adapters.out.git_repository import GitSourceAdapter
from ace.application.use_cases import Ace
from ace.domain.models import Source

console = Console()

# Default paths
DEFAULT_CONFIG_DIR = Path.home() / ".ace"
DEFAULT_CACHE_DIR = DEFAULT_CONFIG_DIR / "cache"


def create_ace(
    config_dir: Path | None = None,
    cache_dir: Path | None = None,
    skip_defaults: bool = False,
) -> Ace:
    """Create and configure the Ace application.

    This is the composition root - where adapters are created
    and injected into the application layer.
    """
    config_dir = config_dir or DEFAULT_CONFIG_DIR
    cache_dir = cache_dir or DEFAULT_CACHE_DIR

    # Ensure directories exist
    config_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Create adapters (concrete implementations)
    source_adapter = GitSourceAdapter(cache_dir)
    registry_adapter = FilesystemRegistryAdapter(config_dir)
    target_adapters = {
        "claude-code": ClaudeCodeTargetAdapter(global_config=True),
    }

    # Initialize default sources if needed
    if not skip_defaults:
        _initialize_defaults(registry_adapter)

    # Create application with injected ports
    return Ace(
        source_port=source_adapter,
        registry_port=registry_adapter,
        targets=target_adapters,
    )


def _initialize_defaults(registry: FilesystemRegistryAdapter) -> None:
    """Initialize default sources on first run."""
    if registry.list_sources():
        return

    try:
        defaults_file = resources.files("ace.assets").joinpath("default_sources.json")
        defaults = json.loads(defaults_file.read_text())

        for name, data in defaults.items():
            source = Source(
                name=name,
                url=data["url"],
                default=data.get("default", False),
                ref=data.get("ref"),
            )
            registry.add_source(source)
    except Exception:
        pass


def get_ace() -> Ace:
    """Get the ace application instance."""
    return create_ace()


def get_config_path() -> Path:
    """Get the config directory path."""
    return DEFAULT_CONFIG_DIR


def error_panel(msg: str, guidance: str | None = None) -> None:
    """Display error with optional guidance."""
    console.print(f"[red]Error:[/red] {msg}")
    if guidance:
        console.print(f"[dim]→ {guidance}[/dim]")


@click.group()
@click.version_option(version=__version__)
def main():
    """ace - Agentic Cognitive Extensions.

    Manage cognitive extensions for AI coding assistants.

    \b
    Sources: where packages come from
      ace source add <url>
      ace source list
      ace source rm <name>

    \b
    Packages: install and manage extensions
      ace install <package>
      ace uninstall <package>
      ace update [package]
      ace list [--available]
    """
    pass


# === Source Subcommand Group ===


@main.group("source")
def source_group():
    """Manage sources (marketplaces, repositories)."""
    pass


@source_group.command("add")
@click.argument("url")
@click.option("-n", "--name", help="Custom name for the source")
@click.option("--default", is_flag=True, help="Set as default source")
def source_add(url: str, name: str | None, default: bool):
    """Add a source.

    Example: ace source add https://github.com/yzavyas/claude-1337
    """
    try:
        ace = get_ace()
        source = ace.add_source(url, name, set_default=default)
        console.print(f"[green]✓[/green] Added [bold]{source.name}[/bold]")

        # Show what's available
        packages = ace.list_packages(source.name)
        if packages:
            console.print(f"  {len(packages)} package(s) available")
    except Exception as e:
        error_panel(str(e), "Check the URL and your network connection.")
        raise SystemExit(1)


@source_group.command("list")
def source_list():
    """List configured sources."""
    ace = get_ace()
    sources = ace.list_sources()

    if not sources:
        console.print("[dim]No sources configured.[/dim]")
        console.print("[dim]→ ace source add <url>[/dim]")
        return

    table = Table(show_header=True, header_style="bold", box=None)
    table.add_column("Name")
    table.add_column("URL")
    table.add_column("")

    for source in sources:
        default = "[dim](default)[/dim]" if source.default else ""
        table.add_row(source.name, source.url, default)

    console.print(table)


@source_group.command("rm")
@click.argument("name")
def source_rm(name: str):
    """Remove a source.

    Example: ace source rm claude-1337
    """
    try:
        ace = get_ace()
        ace.remove_source(name)
        console.print(f"[green]✓[/green] Removed [bold]{name}[/bold]")
    except Exception as e:
        error_panel(str(e))
        raise SystemExit(1)


@source_group.command("refresh")
@click.argument("name", required=False)
def source_refresh(name: str | None):
    """Refresh source cache.

    If NAME not specified, refreshes all sources.
    """
    try:
        ace = get_ace()
        ace.refresh_source(name)
        if name:
            console.print(f"[green]✓[/green] Refreshed [bold]{name}[/bold]")
        else:
            console.print("[green]✓[/green] Refreshed all sources")
    except Exception as e:
        error_panel(str(e))
        raise SystemExit(1)


# === Package Commands ===


@main.command("list")
@click.option("-a", "--available", is_flag=True, help="Show available packages")
@click.option("-v", "--verbose", is_flag=True, help="Show extension details")
def list_cmd(available: bool, verbose: bool):
    """List installed packages.

    Use -a/--available to see packages from sources.
    Use -v/--verbose to see extensions inside packages.
    """
    ace = get_ace()

    # Show installed first
    installations = ace.list_installed()
    if installations:
        console.print("\n[bold]Installed[/bold]")
        table = Table(show_header=True, header_style="bold", box=None)
        table.add_column("Package")
        table.add_column("Target")
        table.add_column("Installed")

        for inst in installations:
            table.add_row(
                inst.id,
                inst.target,
                inst.installed_at.strftime("%Y-%m-%d"),
            )

        console.print(table)
    elif not available:
        console.print("[dim]No packages installed.[/dim]")
        console.print("[dim]→ ace list --available[/dim]")

    # Show available if requested
    if available:
        results = ace.list_packages()
        if results:
            console.print("\n[bold]Available[/bold]")

            if verbose:
                # Detailed view with extensions
                for source, pkg in results:
                    console.print(
                        f"\n[bold cyan]{source.name}/{pkg.name}[/bold cyan] v{pkg.version}"
                    )
                    if pkg.description:
                        console.print(f"  [dim]{pkg.description[:80]}[/dim]")

                    # Extensions inside
                    contents = pkg.contents
                    if contents.skills:
                        console.print(
                            f"  [yellow]skills:[/yellow] {', '.join(contents.skills)}"
                        )
                    if contents.agents:
                        console.print(
                            f"  [magenta]agents:[/magenta] {', '.join(contents.agents)}"
                        )
                    if contents.hooks:
                        console.print(f"  [green]hooks:[/green] ✓")
                    if contents.mcp:
                        console.print(f"  [blue]mcp:[/blue] ✓")
            else:
                # Table view
                table = Table(show_header=True, header_style="bold", box=None)
                table.add_column("Package")
                table.add_column("Version")
                table.add_column("Contents")
                table.add_column("Description")

                for source, pkg in results:
                    desc = (
                        pkg.description[:50] + "..."
                        if len(pkg.description) > 50
                        else pkg.description
                    )
                    table.add_row(
                        f"{source.name}/{pkg.name}",
                        pkg.version,
                        pkg.contents.summary,
                        desc,
                    )

                console.print(table)
        else:
            console.print("[dim]No packages available.[/dim]")
            console.print("[dim]→ ace source add <url>[/dim]")

    console.print()


@main.command("install")
@click.argument("package")
@click.option(
    "-t", "--target", default="claude-code", help="Target agent (default: claude-code)"
)
def install(package: str, target: str):
    """Install a package.

    PACKAGE format: source/name or just name (uses default source)

    \b
    Examples:
      ace install core-1337
      ace install claude-1337/core-1337
    """
    try:
        ace = get_ace()
        installation = ace.install(package, target)

        console.print(
            f"[green]✓[/green] Installed [bold]{installation.package.name}[/bold] to {target}"
        )
        if installation.commit:
            console.print(f"  [dim]pinned to {installation.commit[:8]}[/dim]")

        # Show what was installed
        contents = installation.package.contents
        if contents.total > 0:
            console.print(f"  [dim]{contents.summary}[/dim]")

    except ValueError as e:
        error_panel(str(e), "Run 'ace list --available' to see available packages.")
        raise SystemExit(1)
    except Exception as e:
        error_panel(str(e))
        raise SystemExit(1)


@main.command("uninstall")
@click.argument("package")
def uninstall(package: str):
    """Uninstall a package.

    Example: ace uninstall core-1337
    """
    try:
        ace = get_ace()
        ace.uninstall(package)
        console.print(f"[green]✓[/green] Uninstalled [bold]{package}[/bold]")
    except ValueError as e:
        error_panel(str(e), "Run 'ace list' to see installed packages.")
        raise SystemExit(1)
    except Exception as e:
        error_panel(str(e))
        raise SystemExit(1)


@main.command("update")
@click.argument("package", required=False)
def update(package: str | None):
    """Update installed packages.

    If no PACKAGE specified, updates all.
    """
    try:
        ace = get_ace()
        updated = ace.update(package)

        if updated:
            for inst in updated:
                console.print(
                    f"[green]✓[/green] Updated [bold]{inst.id}[/bold] "
                    f"→ {inst.commit[:8] if inst.commit else 'latest'}"
                )
        else:
            console.print("[dim]Nothing to update.[/dim]")

    except Exception as e:
        error_panel(str(e))
        raise SystemExit(1)


@main.command("show")
@click.argument("package")
def show(package: str):
    """Show package details.

    PACKAGE format: source/name or just name

    Example: ace show core-1337
    """
    ace = get_ace()

    # Parse reference
    if "/" in package:
        source_name, package_name = package.split("/", 1)
    else:
        sources = ace.list_sources()
        default_sources = [s for s in sources if s.default]
        if not default_sources:
            error_panel(
                "No default source set.",
                "Use source/package format or set a default source.",
            )
            raise SystemExit(1)
        source_name = default_sources[0].name
        package_name = package

    result = ace.get_package(source_name, package_name)
    if not result:
        error_panel(f"Package not found: {package}")
        raise SystemExit(1)

    source, pkg = result

    # Header
    console.print(
        Panel.fit(
            f"[bold]{pkg.name}[/bold] v{pkg.version}\n"
            f"{pkg.description or '[dim]No description[/dim]'}",
            title=f"{source.name}/{pkg.name}",
        )
    )

    # Contents
    contents = pkg.contents
    console.print("\n[bold]Contents[/bold]")

    if contents.skills:
        console.print("  [yellow]Skills:[/yellow]")
        for skill in contents.skills:
            console.print(f"    • {skill}")

    if contents.agents:
        console.print("  [magenta]Agents:[/magenta]")
        for agent in contents.agents:
            console.print(f"    • {agent}")

    if contents.hooks:
        console.print("  [green]Hooks:[/green] ✓")

    if contents.mcp:
        console.print("  [blue]MCP:[/blue] ✓")

    if contents.total == 0:
        console.print("  [dim]No extensions[/dim]")

    # Installation status
    installations = ace.list_installed()
    installed = [i for i in installations if i.package.name == pkg.name]
    if installed:
        console.print("\n[bold]Installed[/bold]")
        for inst in installed:
            console.print(f"  Target: {inst.target}")
            console.print(f"  Date: {inst.installed_at.strftime('%Y-%m-%d %H:%M')}")
            if inst.commit:
                console.print(f"  Commit: {inst.commit[:8]}")

    console.print()


@main.command("info")
def info():
    """Show ace configuration."""
    ace = get_ace()

    console.print(
        Panel.fit(
            f"[bold]ace[/bold] v{__version__}\n" "Agentic Cognitive Extensions",
            title="About",
        )
    )

    console.print(f"\n[bold]Config:[/bold] {get_config_path()}")

    sources = ace.list_sources()
    console.print(f"[bold]Sources:[/bold] {len(sources)}")

    installations = ace.list_installed()
    console.print(f"[bold]Installed:[/bold] {len(installations)}")

    targets = ace.list_targets()
    console.print(f"[bold]Targets:[/bold] {', '.join(targets) or 'none detected'}")


if __name__ == "__main__":
    main()
