"""Port interfaces for hexagonal architecture.

Ports define contracts that adapters implement.
Core domain depends only on ports, never on adapters.
"""

from .runtime import RuntimePort, RuntimeResult

__all__ = ["RuntimePort", "RuntimeResult"]
