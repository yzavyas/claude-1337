"""Outbound adapters - implementations of ports."""

from ace.adapters.out.claude_code_target import ClaudeCodeTargetAdapter
from ace.adapters.out.filesystem_registry import FilesystemRegistryAdapter
from ace.adapters.out.git_repository import GitSourceAdapter, SourceError

__all__ = [
    "ClaudeCodeTargetAdapter",
    "FilesystemRegistryAdapter",
    "GitSourceAdapter",
    "SourceError",
]
