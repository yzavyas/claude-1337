"""Phoenix Tracer Adapter - OTel tracing to Phoenix local UI.

Phoenix (https://github.com/Arize-ai/phoenix) provides a beautiful local
UI for viewing traces. This adapter sends spans to Phoenix via OTLP.
"""

import uuid
from contextlib import contextmanager
from typing import Any, Iterator

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from lab.ports.driven.tracer import TracerPort, Span


class PhoenixTracerAdapter:
    """Tracer adapter using Phoenix for local trace visualization.

    Implements the TracerPort protocol using OpenTelemetry to send
    traces to Phoenix running locally.

    Usage:
        1. Start Phoenix: `uv run phoenix serve`
        2. Run experiments with this tracer
        3. View traces at http://localhost:6006
    """

    def __init__(
        self,
        service_name: str = "lab-1337",
        endpoint: str = "http://localhost:6006/v1/traces",
    ):
        """Initialize the Phoenix tracer.

        Args:
            service_name: Name to identify this service in traces
            endpoint: Phoenix OTLP endpoint (default: localhost:6006)
        """
        self.service_name = service_name
        self.global_attributes: dict[str, Any] = {}
        self._current_trace_id: str | None = None

        # Set up OTel with Phoenix exporter
        provider = TracerProvider()
        exporter = OTLPSpanExporter(endpoint=endpoint)
        processor = BatchSpanProcessor(exporter)
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)

        self._tracer = trace.get_tracer(service_name)

    @contextmanager
    def span(
        self,
        name: str,
        attributes: dict[str, Any] | None = None,
    ) -> Iterator[Span]:
        """Create a traced span.

        Opens an OTel span and wraps it in our Span interface.
        """
        # Merge global and span-specific attributes
        all_attributes = {**self.global_attributes}
        if attributes:
            all_attributes.update(attributes)

        with self._tracer.start_as_current_span(name, attributes=all_attributes) as otel_span:
            # Extract trace and span IDs
            context = otel_span.get_span_context()
            trace_id = format(context.trace_id, '032x')
            span_id = format(context.span_id, '016x')

            self._current_trace_id = trace_id

            # Create our Span wrapper
            span = Span(
                name=name,
                trace_id=trace_id,
                span_id=span_id,
                attributes=all_attributes,
            )

            try:
                yield span
            finally:
                # Copy any attributes added to our span back to OTel span
                for key, value in span.attributes.items():
                    if key not in all_attributes:
                        otel_span.set_attribute(key, value)

    def get_trace_id(self) -> str | None:
        """Get the current trace ID."""
        return self._current_trace_id

    def set_global_attributes(self, attrs: dict[str, Any]) -> None:
        """Set attributes that apply to all subsequent spans."""
        self.global_attributes.update(attrs)
