"""ResultObserver port - how to observe extension behavior from runtime output.

Different runtimes emit different output formats:
- simulation: direct tool_use blocks from API response
- headless: stream-json messages from claude -p
- sdk: event callbacks from SDK

Observers parse these and extract what we need to measure.
"""

from typing import Protocol, Any
from dataclasses import dataclass


@dataclass
class Observation:
    """What we observed from a runtime execution."""

    extension_type: str
    """Which extension type was involved."""

    extension_name: str | None
    """Name of the specific extension (skill name, hook name, etc.)."""

    triggered: bool
    """Did the extension trigger/activate?"""

    success: bool | None
    """Did it complete successfully? None if N/A."""

    duration_ms: int
    """Execution time in milliseconds."""

    details: dict[str, Any]
    """Extension-specific details."""

    raw_output: str | None = None
    """Raw output for debugging."""


class ResultObserver(Protocol):
    """Port: How to extract observations from runtime output.

    Each runtime format needs its own observer implementation.
    """

    @property
    def runtime(self) -> str:
        """Which runtime format this parses (simulation, headless, sdk)."""
        ...

    def observe_skills(self, output: Any) -> list[Observation]:
        """Extract skill activation observations."""
        ...

    def observe_hooks(self, output: Any) -> list[Observation]:
        """Extract hook execution observations."""
        ...

    def observe_agents(self, output: Any) -> list[Observation]:
        """Extract agent completion observations."""
        ...

    def observe_commands(self, output: Any) -> list[Observation]:
        """Extract command invocation observations."""
        ...

    def observe_mcp(self, output: Any) -> list[Observation]:
        """Extract MCP tool call observations."""
        ...
