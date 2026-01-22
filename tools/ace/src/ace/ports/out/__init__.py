"""Outbound ports - interfaces the application uses.

These are the "driven" ports in hexagonal architecture - abstractions
that the application depends on, implemented by adapters.
"""

from ace.ports.out.registry import RegistryPort
from ace.ports.out.repository import SourcePort
from ace.ports.out.target import TargetPort

__all__ = [
    "RegistryPort",
    "SourcePort",
    "TargetPort",
]
