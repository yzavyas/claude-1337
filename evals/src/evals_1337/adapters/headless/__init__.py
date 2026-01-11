"""Headless adapters - Claude Code CLI with -p flag.

This is the realistic adapter:
- Uses actual Claude Code
- Real skill loading, hook execution, agent spawning
- Parses stream-json output for observations

Usage:
    claude -p "prompt" --output-format stream-json
"""

from .observer import HeadlessObserver

__all__ = ["HeadlessObserver"]
