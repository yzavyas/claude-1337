"""Ports - abstract interfaces for the eval framework.

Hexagonal architecture: ports define WHAT we do, adapters define HOW.
"""

from .runner import ExtensionRunner, RunnerRegistry
from .observer import ResultObserver

__all__ = ["ExtensionRunner", "RunnerRegistry", "ResultObserver"]
