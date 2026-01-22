"""Domain models for ace.

Ontology:
- Source: Where packages come from (marketplaces, git repos)
- Package: The installable unit (core-1337, rust-1337)
- Extensions: What's inside (skills, agents, hooks, mcps)
"""

from ace.domain.models import (
    Extensions,
    ExtensionType,
    Installation,
    Package,
    Source,
)

__all__ = [
    "Extensions",
    "ExtensionType",
    "Installation",
    "Package",
    "Source",
]
