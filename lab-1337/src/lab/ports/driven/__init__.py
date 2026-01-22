"""Driven Ports - Interfaces for external systems the domain uses.

These are the "secondary" ports in hexagonal architecture terminology.
The domain defines what it needs; adapters provide implementations.
"""

from .llm import LLMPort, LLMResponse, LLMConfig
from .grader import GraderPort, GradeResult
from .tracer import TracerPort, Span
from .storage import StoragePort

__all__ = [
    "LLMPort",
    "LLMResponse",
    "LLMConfig",
    "GraderPort",
    "GradeResult",
    "TracerPort",
    "Span",
    "StoragePort",
]
