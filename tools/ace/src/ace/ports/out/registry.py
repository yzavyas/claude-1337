"""Registry port - tracking sources and installations."""

from typing import Protocol

from ace.domain.models import Installation, Source


class RegistryPort(Protocol):
    """Interface for tracking sources and installed packages.

    The registry maintains state about:
    - Configured sources (where packages come from)
    - Installed packages (what's installed where)
    """

    # Source management

    def list_sources(self) -> list[Source]:
        """List all registered sources."""
        ...

    def add_source(self, source: Source) -> None:
        """Register a new source."""
        ...

    def remove_source(self, name: str) -> None:
        """Remove a source from registry."""
        ...

    def get_source(self, name: str) -> Source | None:
        """Get a source by name."""
        ...

    # Installation management

    def list_installations(self, target: str | None = None) -> list[Installation]:
        """List all installations, optionally filtered by target."""
        ...

    def add_installation(self, installation: Installation) -> None:
        """Record a new installation."""
        ...

    def remove_installation(self, installation_id: str) -> None:
        """Remove an installation record."""
        ...

    def get_installation(self, installation_id: str) -> Installation | None:
        """Get an installation by ID."""
        ...
