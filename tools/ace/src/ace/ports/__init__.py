"""Ports - interfaces between application and adapters.

out/ - driven ports (what the application uses)
     - SourcePort: fetching packages from sources
     - RegistryPort: tracking sources and installations
     - TargetPort: installing to targets

In hexagonal architecture:
- Application layer depends on these port interfaces
- Adapters implement these interfaces
- Composition root (CLI) wires adapters to ports
"""

from ace.ports.out import RegistryPort, SourcePort, TargetPort

__all__ = [
    "RegistryPort",
    "SourcePort",
    "TargetPort",
]
