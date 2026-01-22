"""Target port - installing packages to agent configurations."""

from pathlib import Path
from typing import Protocol

from ace.domain.models import Package


class TargetPort(Protocol):
    """Interface for installing packages to a target agent.

    Each target (Claude Code, Codex, Cursor, etc.) has its own
    configuration format and installation location.
    """

    @property
    def name(self) -> str:
        """Target identifier (e.g., 'claude-code', 'codex')."""
        ...

    def is_available(self) -> bool:
        """Check if this target is available on the system."""
        ...

    def install(self, package: Package, source_path: Path) -> None:
        """Install a package from source path to target config."""
        ...

    def uninstall(self, package: Package) -> None:
        """Remove a package from target config."""
        ...

    def is_installed(self, package: Package) -> bool:
        """Check if a package is installed in target."""
        ...

    def get_config_path(self) -> str:
        """Get the path to the target's configuration directory."""
        ...
