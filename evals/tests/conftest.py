"""Pytest configuration for claude-1337 evals."""

import os
import pytest
from anthropic import Anthropic


@pytest.fixture
def client():
    """Anthropic client for API calls."""
    return Anthropic()


@pytest.fixture
def skills_dir():
    """Path to skills directory."""
    return os.path.join(os.path.dirname(__file__), "..", "..", "plugins")


@pytest.fixture
def rust_skill_content(skills_dir):
    """Load rust-1337 SKILL.md content."""
    path = os.path.join(skills_dir, "rust-1337", "SKILL.md")
    with open(path) as f:
        return f.read()


@pytest.fixture
def terminal_skill_content(skills_dir):
    """Load terminal-1337 SKILL.md content."""
    path = os.path.join(skills_dir, "terminal-1337", "skills", "SKILL.md")
    with open(path) as f:
        return f.read()
