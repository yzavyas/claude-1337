"""Console Tracer Adapter - Simple tracing to stdout.

A lightweight tracer that prints spans to the console.
Useful for development and debugging without external dependencies.
"""

import time
import uuid
from contextlib import contextmanager
from typing import Any, Iterator

from rich.console import Console
from rich.tree import Tree

from lab.ports.driven.tracer import TracerPort, Span


class ConsoleTracerAdapter:
    """Simple tracer that prints to console.

    Implements the TracerPort protocol with Rich-formatted output.
    Useful for development and debugging.
    """

    def __init__(self, verbose: bool = True):
        """Initialize the console tracer.

        Args:
            verbose: If True, print detailed span info. If False, just names.
        """
        self.verbose = verbose
        self.console = Console()
        self.global_attributes: dict[str, Any] = {}
        self._current_trace_id: str | None = None
        self._depth = 0

    @contextmanager
    def span(
        self,
        name: str,
        attributes: dict[str, Any] | None = None,
    ) -> Iterator[Span]:
        """Create a span that prints to console."""
        # Generate IDs
        trace_id = self._current_trace_id or str(uuid.uuid4())[:8]
        span_id = str(uuid.uuid4())[:8]
        self._current_trace_id = trace_id

        # Merge attributes
        all_attributes = {**self.global_attributes}
        if attributes:
            all_attributes.update(attributes)

        # Create span
        span = Span(
            name=name,
            trace_id=trace_id,
            span_id=span_id,
            attributes=all_attributes,
        )

        # Print start
        indent = "  " * self._depth
        if self.verbose:
            self.console.print(f"{indent}[dim]▸[/] [bold blue]{name}[/] started", highlight=False)
            if all_attributes:
                for key, value in all_attributes.items():
                    self.console.print(f"{indent}  [dim]{key}:[/] {value}", highlight=False)

        start_time = time.time()
        self._depth += 1

        try:
            yield span
        except Exception as e:
            span.record_exception(e)
            raise
        finally:
            self._depth -= 1
            duration_ms = int((time.time() - start_time) * 1000)

            # Print end with any new attributes
            if self.verbose:
                new_attrs = {
                    k: v for k, v in span.attributes.items()
                    if k not in all_attributes
                }
                if new_attrs:
                    for key, value in new_attrs.items():
                        self.console.print(f"{indent}  [dim]{key}:[/] {value}", highlight=False)

                if span.attributes.get("error"):
                    self.console.print(
                        f"{indent}[dim]◂[/] [bold red]{name}[/] [dim]({duration_ms}ms)[/] [red]ERROR[/]",
                        highlight=False,
                    )
                else:
                    self.console.print(
                        f"{indent}[dim]◂[/] [bold green]{name}[/] [dim]({duration_ms}ms)[/]",
                        highlight=False,
                    )

    def get_trace_id(self) -> str | None:
        """Get the current trace ID."""
        return self._current_trace_id

    def set_global_attributes(self, attrs: dict[str, Any]) -> None:
        """Set attributes that apply to all subsequent spans."""
        self.global_attributes.update(attrs)


class NoOpTracerAdapter:
    """A tracer that does nothing.

    Useful for testing or when tracing is disabled.
    """

    def __init__(self):
        self._current_trace_id: str | None = None

    @contextmanager
    def span(
        self,
        name: str,
        attributes: dict[str, Any] | None = None,
    ) -> Iterator[Span]:
        """Create a no-op span."""
        span = Span(name=name)
        yield span

    def get_trace_id(self) -> str | None:
        """No trace ID in no-op mode."""
        return None

    def set_global_attributes(self, attrs: dict[str, Any]) -> None:
        """No-op."""
        pass
