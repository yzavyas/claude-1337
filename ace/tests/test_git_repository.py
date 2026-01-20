"""Tests for git source adapter."""

import json
from pathlib import Path

import pytest

from ace.adapters.out.git_repository import GitSourceAdapter
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


class TestGitSourceAdapter:
    """Tests for GitSourceAdapter."""

    def test_parse_package(self, temp_cache: Path, mock_source: Path):
        """Adapter can parse plugin.json files."""
        adapter = GitSourceAdapter(temp_cache)

        plugin_json = (
            mock_source / "plugins" / "test-plugin" / ".claude-plugin" / "plugin.json"
        )
        package = adapter._parse_package(plugin_json)

        assert package is not None
        assert package.name == "test-plugin"
        assert package.description == "A test plugin"
        assert package.version == "1.0.0"

    def test_parse_package_missing_file(self, temp_cache: Path, tmp_path: Path):
        """Adapter handles missing plugin.json gracefully."""
        adapter = GitSourceAdapter(temp_cache)

        missing = tmp_path / "nonexistent" / "plugin.json"
        package = adapter._parse_package(missing)

        assert package is None

    def test_parse_package_invalid_json(self, temp_cache: Path, tmp_path: Path):
        """Adapter handles invalid JSON gracefully."""
        adapter = GitSourceAdapter(temp_cache)

        bad_json = tmp_path / "bad" / ".claude-plugin"
        bad_json.mkdir(parents=True)
        (bad_json / "plugin.json").write_text("not valid json")

        package = adapter._parse_package(bad_json / "plugin.json")

        assert package is None

    def test_scan_contents(self, temp_cache: Path, mock_source: Path):
        """Adapter scans package contents correctly."""
        adapter = GitSourceAdapter(temp_cache)

        pkg_dir = mock_source / "plugins" / "test-plugin"
        contents = adapter._scan_contents(pkg_dir)

        assert "test-skill" in contents.skills
        assert "test-agent" in contents.agents
