"""Tests for plugin harness."""

import pytest
from pathlib import Path

from evals_1337.harness import (
    PluginType,
    discover_plugin_type,
    compute_pass_at_k,
    compute_pass_hat_k,
)


class TestPluginType:
    """Test PluginType enum."""

    def test_values(self):
        assert PluginType.SKILL.value == "skill"
        assert PluginType.HOOK.value == "hook"
        assert PluginType.AGENT.value == "agent"
        assert PluginType.COMMAND.value == "command"
        assert PluginType.MCP.value == "mcp"


class TestDiscoverPluginType:
    """Test plugin type discovery."""

    def test_discovers_skill(self, tmp_path: Path):
        """Finds SKILL.md -> skill type."""
        (tmp_path / "SKILL.md").write_text("---\nname: test\n---\n# Test")
        types = discover_plugin_type(tmp_path)
        assert PluginType.SKILL in types

    def test_discovers_hook(self, tmp_path: Path):
        """Finds hooks/hooks.json -> hook type."""
        hooks_dir = tmp_path / "hooks"
        hooks_dir.mkdir()
        (hooks_dir / "hooks.json").write_text('{"hooks": {}}')
        types = discover_plugin_type(tmp_path)
        assert PluginType.HOOK in types

    def test_discovers_agent(self, tmp_path: Path):
        """Finds agents/*.md -> agent type."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "test-agent.md").write_text("# Test Agent")
        types = discover_plugin_type(tmp_path)
        assert PluginType.AGENT in types

    def test_discovers_command(self, tmp_path: Path):
        """Finds commands/*.md -> command type."""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()
        (commands_dir / "test-cmd.md").write_text("# Test Command")
        types = discover_plugin_type(tmp_path)
        assert PluginType.COMMAND in types

    def test_discovers_mcp(self, tmp_path: Path):
        """Finds .mcp.json -> mcp type."""
        (tmp_path / ".mcp.json").write_text('{"servers": {}}')
        types = discover_plugin_type(tmp_path)
        assert PluginType.MCP in types

    def test_discovers_multiple(self, tmp_path: Path):
        """Can discover multiple types."""
        (tmp_path / "SKILL.md").write_text("---\nname: test\n---")
        hooks_dir = tmp_path / "hooks"
        hooks_dir.mkdir()
        (hooks_dir / "hooks.json").write_text('{"hooks": {}}')

        types = discover_plugin_type(tmp_path)
        assert PluginType.SKILL in types
        assert PluginType.HOOK in types

    def test_empty_directory(self, tmp_path: Path):
        """Empty directory returns no types."""
        types = discover_plugin_type(tmp_path)
        assert types == []


class TestPassAtK:
    """Test pass@k computation."""

    def test_all_success(self):
        """100% success rate -> pass@k = 1.0."""
        result = compute_pass_at_k(successes=10, total=10, k=3)
        assert result == 1.0

    def test_no_success(self):
        """0% success rate -> pass@k = 0.0."""
        result = compute_pass_at_k(successes=0, total=10, k=3)
        assert result == 0.0

    def test_partial_success(self):
        """75% success rate with k=3."""
        # With 75% success, chance of all 3 failing = 0.25^3 ≈ 0.016
        # So pass@3 ≈ 0.984
        result = compute_pass_at_k(successes=75, total=100, k=3)
        assert result > 0.98

    def test_insufficient_total(self):
        """Total < k returns 0.0."""
        result = compute_pass_at_k(successes=1, total=2, k=3)
        assert result == 0.0


class TestPassHatK:
    """Test pass^k computation."""

    def test_all_success(self):
        """100% success rate -> pass^k = 1.0."""
        result = compute_pass_hat_k(successes=10, total=10, k=3)
        assert result == 1.0

    def test_no_success(self):
        """0% success rate -> pass^k = 0.0."""
        result = compute_pass_hat_k(successes=0, total=10, k=3)
        assert result == 0.0

    def test_partial_success(self):
        """75% success rate -> pass^3 = 0.75^3 ≈ 0.42."""
        result = compute_pass_hat_k(successes=75, total=100, k=3)
        expected = 0.75 ** 3
        assert abs(result - expected) < 0.001

    def test_zero_total(self):
        """Zero total returns 0.0."""
        result = compute_pass_hat_k(successes=0, total=0, k=3)
        assert result == 0.0
