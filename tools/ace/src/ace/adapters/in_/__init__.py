"""Inbound adapters - driving adapters that interact with users.

In hexagonal architecture, these adapters drive the application:
- CLI: command-line interface
- (future: REST API, etc.)
"""

from ace.adapters.in_.cli import main

__all__ = ["main"]
