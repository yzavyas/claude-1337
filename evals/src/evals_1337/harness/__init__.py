"""Plugin test harness.

Universal harness for testing any Claude Code plugin type:
- Skills
- Hooks
- Agents
- Commands
- MCP servers

The harness auto-discovers plugin structure and runs appropriate tests.
"""

from .plugin_harness import (
    PluginHarness,
    PluginTestResult,
    PluginType,
    discover_plugin_type,
    run_plugin_tests,
    compute_pass_at_k,
    compute_pass_hat_k,
)

__all__ = [
    "PluginHarness",
    "PluginTestResult",
    "PluginType",
    "discover_plugin_type",
    "run_plugin_tests",
    "compute_pass_at_k",
    "compute_pass_hat_k",
]
