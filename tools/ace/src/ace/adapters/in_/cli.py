"""ace CLI - Agentic Capability Extensions.

Discover, install, and manage extension packages for AI agents.
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

DEFAULT_CONFIG_DIR = Path.home() / ".ace"
DEFAULT_CACHE_DIR = DEFAULT_CONFIG_DIR / "cache"


def create_ace(
    config_dir: Path | None = None,
    cache_dir: Path | None = None,
    skip_defaults: bool = False,
) -> Ace:
    """Composition root - creates adapters and injects into application."""
    config_dir = config_dir or DEFAULT_CONFIG_DIR
    cache_dir = cache_dir or DEFAULT_CACHE_DIR

    config_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    source_adapter = GitSourceAdapter(cache_dir)
    registry_adapter = FilesystemRegistryAdapter(config_dir)
    target_adapters = {
        "claude-code": ClaudeCodeTargetAdapter(global_config=True),
    }

    if not skip_defaults:
        _initialize_defaults(registry_adapter)

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
    """ace - drop extensions into your AI agent.

    \b
    Sources:
      ace source add <url>
      ace source list

    \b
    Packages:
      ace add <package>
      ace rm <package>
      ace list [-a]
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
@click.option("-v", "--verbose", is_flag=True, help="Show extensions")
def list_cmd(available: bool, verbose: bool):
    """List packages."""
    ace = get_ace()

    installations = ace.list_installed()
    if installations:
        console.print("\n[bold]Installed[/bold]")
        table = Table(show_header=True, header_style="bold", box=None)
        table.add_column("Package")
        table.add_column("Target")
        table.add_column("Date")

        for inst in installations:
            table.add_row(
                inst.id,
                inst.target,
                inst.installed_at.strftime("%Y-%m-%d"),
            )

        console.print(table)
    elif not available:
        console.print("[dim]Nothing installed.[/dim]")
        console.print("[dim]→ ace list -a[/dim]")

    if available:
        results = ace.list_packages()
        if results:
            console.print("\n[bold]Available[/bold]")

            if verbose:
                for source, pkg in results:
                    console.print(
                        f"\n[bold cyan]{source.name}/{pkg.name}[/bold cyan] v{pkg.version}"
                    )
                    if pkg.description:
                        console.print(f"  [dim]{pkg.description[:80]}[/dim]")

                    ext = pkg.extensions
                    if ext.skills:
                        console.print(f"  [yellow]skills:[/yellow] {', '.join(ext.skills)}")
                    if ext.agents:
                        console.print(f"  [magenta]agents:[/magenta] {', '.join(ext.agents)}")
                    if ext.hooks:
                        console.print(f"  [green]hooks:[/green] ✓")
                    if ext.mcps:
                        console.print(f"  [blue]mcps:[/blue] ✓")
            else:
                table = Table(show_header=True, header_style="bold", box=None)
                table.add_column("Package")
                table.add_column("Version")
                table.add_column("Extensions")
                table.add_column("Description")

                for source, pkg in results:
                    desc = pkg.description[:50] + "..." if len(pkg.description) > 50 else pkg.description
                    table.add_row(
                        f"{source.name}/{pkg.name}",
                        pkg.version,
                        pkg.extensions.summary,
                        desc,
                    )

                console.print(table)
        else:
            console.print("[dim]No packages available.[/dim]")
            console.print("[dim]→ ace source add <url>[/dim]")

    console.print()


@main.command("add")
@click.argument("package")
@click.option("-t", "--target", default="claude-code", help="Target agent")
def add_cmd(package: str, target: str):
    """Add a package.

    \b
    Examples:
      ace add core-1337
      ace add claude-1337/core-1337
    """
    try:
        ace = get_ace()
        installation = ace.install(package, target)

        console.print(f"[green]✓[/green] added [bold]{installation.package.name}[/bold] → {target}")
        if installation.commit:
            console.print(f"  [dim]({installation.commit[:8]})[/dim]")

        ext = installation.package.extensions
        if ext.total > 0:
            console.print(f"  [dim]{ext.summary}[/dim]")

    except ValueError as e:
        error_panel(str(e), "Run 'ace list -a' to see available packages.")
        raise SystemExit(1)
    except Exception as e:
        error_panel(str(e))
        raise SystemExit(1)


@main.command("rm")
@click.argument("package")
def rm_cmd(package: str):
    """Remove a package."""
    try:
        ace = get_ace()
        ace.uninstall(package)
        console.print(f"[green]✓[/green] removed [bold]{package}[/bold]")
    except ValueError as e:
        error_panel(str(e), "Run 'ace list' to see installed packages.")
        raise SystemExit(1)
    except Exception as e:
        error_panel(str(e))
        raise SystemExit(1)


@main.command("update")
@click.argument("package", required=False)
def update(package: str | None):
    """Update packages."""
    try:
        ace = get_ace()
        updated = ace.update(package)

        if updated:
            for inst in updated:
                console.print(
                    f"[green]✓[/green] updated [bold]{inst.id}[/bold] → {inst.commit[:8] if inst.commit else 'latest'}"
                )
        else:
            console.print("[dim]Nothing to update.[/dim]")

    except Exception as e:
        error_panel(str(e))
        raise SystemExit(1)


@main.command("show")
@click.argument("package")
def show(package: str):
    """Show package details."""
    ace = get_ace()

    if "/" in package:
        source_name, package_name = package.split("/", 1)
    else:
        sources = ace.list_sources()
        default_sources = [s for s in sources if s.default]
        if not default_sources:
            error_panel("No default source.", "Use source/package format.")
            raise SystemExit(1)
        source_name = default_sources[0].name
        package_name = package

    result = ace.get_package(source_name, package_name)
    if not result:
        error_panel(f"Not found: {package}")
        raise SystemExit(1)

    source, pkg = result

    console.print(
        Panel.fit(
            f"[bold]{pkg.name}[/bold] v{pkg.version}\n"
            f"{pkg.description or '[dim]No description[/dim]'}",
            title=f"{source.name}/{pkg.name}",
        )
    )

    ext = pkg.extensions
    console.print("\n[bold]Extensions[/bold]")

    if ext.skills:
        console.print("  [yellow]Skills:[/yellow]")
        for skill in ext.skills:
            console.print(f"    • {skill}")

    if ext.agents:
        console.print("  [magenta]Agents:[/magenta]")
        for agent in ext.agents:
            console.print(f"    • {agent}")

    if ext.hooks:
        console.print("  [green]Hooks:[/green] ✓")

    if ext.mcps:
        console.print("  [blue]MCPs:[/blue] ✓")

    if ext.total == 0:
        console.print("  [dim]Empty[/dim]")

    installations = ace.list_installed()
    installed = [i for i in installations if i.package.name == pkg.name]
    if installed:
        console.print("\n[bold]Installed[/bold]")
        for inst in installed:
            console.print(f"  {inst.target} ({inst.installed_at.strftime('%Y-%m-%d')})")
            if inst.commit:
                console.print(f"  [dim]{inst.commit[:8]}[/dim]")

    console.print()


@main.command("info")
def info():
    """Show ace status."""
    ace = get_ace()

    console.print(Panel.fit(f"[bold]ace[/bold] v{__version__}", title=""))

    console.print(f"\n[bold]Config:[/bold] {get_config_path()}")
    console.print(f"[bold]Sources:[/bold] {len(ace.list_sources())}")
    console.print(f"[bold]Installed:[/bold] {len(ace.list_installed())}")
    console.print(f"[bold]Targets:[/bold] {', '.join(ace.list_targets()) or 'none'}")


if __name__ == "__main__":
    main()
