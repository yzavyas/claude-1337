"""Source port - fetching packages from remote sources."""

from pathlib import Path
from typing import Protocol

from ace.domain.models import Package, Source


class SourcePort(Protocol):
    """Interface for fetching packages from sources.

    A source is a git repository containing packages (plugins).
    This port abstracts the fetch/clone operations.
    """

    def fetch(self, source: Source) -> None:
        """Fetch/clone source to local cache."""
        ...

    def list_packages(self, source: Source) -> list[Package]:
        """List all packages in a source."""
        ...

    def get_package(self, source: Source, name: str) -> Package | None:
        """Get a specific package by name."""
        ...

    def get_package_path(self, source: Source, package: Package) -> Path:
        """Get local filesystem path to package content."""
        ...

    def get_commit(self, source: Source) -> str:
        """Get current commit hash of source."""
        ...
