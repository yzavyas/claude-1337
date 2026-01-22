"""Domain models for ace.

Ontology:
- Source: Where packages come from
- Package: The installable bundle
- Extension: Individual capability (skill, agent, hook, mcp)
"""

from ace.domain.models import (
    Extension,
    ExtensionType,
    Installation,
    Package,
    PackageContents,
    Source,
)

__all__ = [
    "Extension",
    "ExtensionType",
    "Installation",
    "Package",
    "PackageContents",
    "Source",
]
