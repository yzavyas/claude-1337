"""Scanner port - discovers packages in source directories."""

from pathlib import Path
from typing import Protocol

from ace.domain.models import Package


class ScannerPort(Protocol):
    """Finds packages in a directory tree."""

    def scan(self, root_path: Path) -> list[Package]:
        """Scan directory for packages."""
        ...

    def can_scan(self, root_path: Path) -> bool:
        """Check if this scanner understands the directory structure."""
        ...
