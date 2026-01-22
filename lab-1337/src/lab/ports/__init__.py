"""Lab-1337 Ports Layer.

Ports define the interfaces between the domain and external systems.
Using Python's Protocol for structural typing (duck typing with type hints).

Terminology:
- Driven ports: Interfaces for things the domain USES (LLM, Storage, Grader)
- Driving ports: Interfaces for things that USE the domain (CLI, API)
"""

from .driven.llm import LLMPort, LLMResponse, LLMConfig
from .driven.grader import GraderPort, GradeResult
from .driven.tracer import TracerPort, Span
from .driven.storage import StoragePort

__all__ = [
    # Driven ports
    "LLMPort",
    "LLMResponse",
    "LLMConfig",
    "GraderPort",
    "GradeResult",
    "TracerPort",
    "Span",
    "StoragePort",
]
