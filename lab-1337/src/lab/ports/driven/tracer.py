"""Tracer Port - Interface for observability and tracing.

Why a Protocol?
--------------
Different environments need different tracing:
- Development: Phoenix local UI
- Production: Honeycomb, Datadog, etc.
- Testing: NoOp (silent)
- Debug: Console output

The domain creates spans and sets attributes.
Adapters decide where the traces go.
"""

from contextlib import contextmanager
from typing import Protocol, Any, Iterator

from pydantic import BaseModel, ConfigDict, Field


class Span(BaseModel):
    """A trace span for a unit of work.

    Simplified interface over OTel spans.
    """
    model_config = ConfigDict(validate_assignment=True)

    name: str
    trace_id: str = ""
    span_id: str = ""
    attributes: dict[str, Any] = Field(default_factory=dict)

    def set_attribute(self, key: str, value: Any) -> None:
        """Set an attribute on this span."""
        self.attributes[key] = value

    def set_attributes(self, attrs: dict[str, Any]) -> None:
        """Set multiple attributes."""
        self.attributes.update(attrs)

    def record_exception(self, exc: Exception) -> None:
        """Record an exception on this span."""
        self.attributes["error"] = True
        self.attributes["error.type"] = type(exc).__name__
        self.attributes["error.message"] = str(exc)


class TracerPort(Protocol):
    """Port for distributed tracing and observability.

    The domain needs to:
    1. Create spans for units of work
    2. Set attributes on spans
    3. Record errors

    Implementations:
    - PhoenixTracerAdapter: OTel to Phoenix local UI
    - OTelTracerAdapter: OTel to any collector
    - ConsoleTracerAdapter: Print to console
    - NoOpTracerAdapter: Silent (for testing)
    """

    @contextmanager
    def span(
        self,
        name: str,
        attributes: dict[str, Any] | None = None,
    ) -> Iterator[Span]:
        """Create a span for a unit of work.

        Use as a context manager:
            with tracer.span("experiment_run", {"task_id": "..."}) as span:
                span.set_attribute("passed", True)
                # do work
        """
        ...

    def get_trace_id(self) -> str | None:
        """Get the current trace ID.

        Returns None if no active trace.
        """
        ...

    def set_global_attributes(self, attrs: dict[str, Any]) -> None:
        """Set attributes that apply to all subsequent spans.

        Useful for experiment-level metadata.
        """
        ...
