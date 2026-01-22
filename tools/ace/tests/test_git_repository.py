"""Tests for git source adapter and scanners."""

import json
from pathlib import Path

import pytest

from ace.adapters.out.scanners import ClaudePluginScanner
from ace.domain.models import Source


@pytest.fixture
def temp_cache(tmp_path: Path) -> Path:
    """Create a temporary cache directory."""
    cache = tmp_path / "cache"
    cache.mkdir()
    return cache


@pytest.fixture
def mock_source(tmp_path: Path) -> Path:
    """Create a mock source (marketplace) structure."""
    source = tmp_path / "mock-marketplace"
    source.mkdir()

    # Create a package
    pkg = source / "plugins" / "test-plugin"
    pkg.mkdir(parents=True)

    # Add .claude-plugin/plugin.json
    plugin_meta = pkg / ".claude-plugin"
    plugin_meta.mkdir()
    (plugin_meta / "plugin.json").write_text(
        json.dumps(
            {
                "name": "test-plugin",
                "description": "A test plugin",
                "version": "1.0.0",
            }
        )
    )

    # Add skills directory
    skills = pkg / "skills" / "test-skill"
    skills.mkdir(parents=True)
    (skills / "SKILL.md").write_text("# Test Skill\n\nA skill for testing.")

    # Add agents directory
    agents = pkg / "agents"
    agents.mkdir()
    (agents / "test-agent.md").write_text("# Test Agent\n\nAn agent for testing.")

    return source


class TestClaudePluginScanner:
    """Tests for ClaudePluginScanner."""

    def test_can_scan_detects_plugin_structure(self, mock_source: Path):
        """Scanner detects Claude plugin structure."""
        scanner = ClaudePluginScanner()
        assert scanner.can_scan(mock_source)

    def test_can_scan_rejects_empty_dir(self, tmp_path: Path):
        """Scanner rejects directories without plugins."""
        scanner = ClaudePluginScanner()
        assert not scanner.can_scan(tmp_path)

    def test_scan_finds_packages(self, mock_source: Path):
        """Scanner finds packages in source."""
        scanner = ClaudePluginScanner()
        packages = scanner.scan(mock_source)

        assert len(packages) == 1
        pkg = packages[0]
        assert pkg.name == "test-plugin"
        assert pkg.description == "A test plugin"
        assert pkg.version == "1.0.0"

    def test_scan_finds_extensions(self, mock_source: Path):
        """Scanner discovers extensions within packages."""
        scanner = ClaudePluginScanner()
        packages = scanner.scan(mock_source)

        pkg = packages[0]
        assert "test-skill" in pkg.extensions.skills
        assert "test-agent" in pkg.extensions.agents

    def test_scan_handles_invalid_json(self, tmp_path: Path):
        """Scanner handles malformed plugin.json."""
        pkg = tmp_path / "bad-plugin"
        pkg.mkdir()
        meta = pkg / ".claude-plugin"
        meta.mkdir()
        (meta / "plugin.json").write_text("not valid json")

        scanner = ClaudePluginScanner()
        packages = scanner.scan(tmp_path)

        # Should not crash, just skip invalid
        assert len(packages) == 0


class TestSource:
    """Tests for Source model used in git operations."""

    def test_source_creation(self):
        """Source can be created with URL."""
        source = Source(
            name="test",
            url="https://github.com/test/test",
        )
        assert source.name == "test"
        assert source.url == "https://github.com/test/test"
        assert not source.default
        assert source.ref is None
