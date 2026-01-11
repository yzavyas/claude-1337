"""Adapters - implementations of ports for specific runtimes.

Available adapters:
- simulation: Direct API calls with mock tools (fast, but not realistic)
- headless: Claude Code CLI with -p flag (realistic, slower)
- sdk: Python/TypeScript SDK (programmatic control)
"""

from .registry import create_default_registry

__all__ = ["create_default_registry"]
