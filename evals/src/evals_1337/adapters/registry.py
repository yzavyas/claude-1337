"""Default registry with all available adapters."""

from ..ports import RunnerRegistry


def create_default_registry() -> RunnerRegistry:
    """Create registry with all available adapters.

    Import adapters lazily to avoid import errors if dependencies missing.
    """
    registry = RunnerRegistry()

    # Simulation adapters (direct API, mock tools)
    try:
        from .simulation.skills import SkillSimulationRunner
        registry.register(SkillSimulationRunner())
    except ImportError:
        pass

    # Headless adapters (claude -p, stream-json)
    try:
        from .headless.skills import SkillHeadlessRunner
        registry.register(SkillHeadlessRunner())
    except ImportError:
        pass

    try:
        from .headless.hooks import HookHeadlessRunner
        registry.register(HookHeadlessRunner())
    except ImportError:
        pass

    try:
        from .headless.agents import AgentHeadlessRunner
        registry.register(AgentHeadlessRunner())
    except ImportError:
        pass

    try:
        from .headless.commands import CommandHeadlessRunner
        registry.register(CommandHeadlessRunner())
    except ImportError:
        pass

    try:
        from .headless.mcp import MCPHeadlessRunner
        registry.register(MCPHeadlessRunner())
    except ImportError:
        pass

    return registry
