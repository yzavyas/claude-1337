"""Plugin tests.

NOTE: Plugin structure/manifest/hooks validation is handled by plugin-dev:plugin-validator.
These tests only cover OUR specific implementations (hooks, scripts).
"""

import json
import subprocess
from pathlib import Path

import pytest

# Resolve project root relative to this file
PROJECT_ROOT = Path(__file__).parent.parent.parent


class TestSessionStartHook:
    """Test the session-start.sh hook script - our custom implementation."""

    @pytest.fixture
    def hook_script(self) -> Path:
        return PROJECT_ROOT / "plugins" / "core-1337" / "hooks" / "session-start.sh"

    def test_hook_script_exists(self, hook_script: Path):
        """Hook script exists and is executable."""
        assert hook_script.exists(), f"Hook script not found: {hook_script}"
        assert hook_script.stat().st_mode & 0o111, "Hook script not executable"

    def test_hook_script_is_posix(self, hook_script: Path):
        """Hook script uses POSIX shell, not bash-isms."""
        content = hook_script.read_text()
        assert content.startswith("#!/bin/sh"), "Should use #!/bin/sh for POSIX"
        assert "[[" not in content, "Should not use [[ ]] (bash-ism)"

    def test_hook_outputs_core_1337(self, hook_script: Path, tmp_path: Path):
        """Hook always outputs core-1337 load instruction."""
        # Create mock known_marketplaces.json pointing to project root
        mock_home = tmp_path / "mock_home" / ".claude" / "plugins"
        mock_home.mkdir(parents=True)

        marketplaces = {"claude-1337": {"installLocation": str(PROJECT_ROOT)}}
        (mock_home / "known_marketplaces.json").write_text(json.dumps(marketplaces))

        env = {"HOME": str(tmp_path / "mock_home")}
        result = subprocess.run(
            ["/bin/sh", str(hook_script)],
            capture_output=True,
            text=True,
            env=env,
        )

        assert result.returncode == 0, f"Script failed: {result.stderr}"
        assert "core-1337" in result.stdout, "Should mention core-1337"
        assert "**Load now:**" in result.stdout, "Should have load instruction"

    def test_hook_extracts_triggers(self, hook_script: Path, tmp_path: Path):
        """Hook extracts triggers from marketplace.json."""
        mock_home = tmp_path / "mock_home" / ".claude" / "plugins"
        mock_home.mkdir(parents=True)

        marketplaces = {"claude-1337": {"installLocation": str(PROJECT_ROOT)}}
        (mock_home / "known_marketplaces.json").write_text(json.dumps(marketplaces))

        env = {"HOME": str(tmp_path / "mock_home")}
        result = subprocess.run(
            ["/bin/sh", str(hook_script)],
            capture_output=True,
            text=True,
            env=env,
        )

        assert result.returncode == 0
        assert "rust-1337" in result.stdout, "Should list rust-1337"
        assert "terminal-1337" in result.stdout, "Should list terminal-1337"
        assert "SKILL.md" in result.stdout, "Should include path to SKILL.md"

    def test_hook_graceful_no_marketplace(self, hook_script: Path, tmp_path: Path):
        """Hook handles missing marketplace gracefully."""
        mock_home = tmp_path / "empty_home"
        mock_home.mkdir()

        env = {"HOME": str(mock_home)}
        result = subprocess.run(
            ["/bin/sh", str(hook_script)],
            capture_output=True,
            text=True,
            env=env,
        )

        assert result.returncode == 0, f"Script failed: {result.stderr}"
        assert "claude-1337" in result.stdout
