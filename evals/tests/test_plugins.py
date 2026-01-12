"""Plugin validation tests.

Uses simple JSON validation for fast tests.
For comprehensive validation, use plugin-dev:plugin-validator agent.
"""

from pathlib import Path

import pytest

from evals_1337.targets.plugins import (
    ValidationResult,
    discover_plugins,
    validate_all,
    validate_hooks,
    validate_manifest,
    validate_plugin,
)

# Resolve plugins directory relative to this file
PLUGINS_DIR = Path(__file__).parent.parent.parent / "plugins"


class TestManifestValidation:
    """Test manifest validation."""

    def test_valid_manifest(self, tmp_path: Path):
        """Valid manifest passes."""
        plugin_dir = tmp_path / "test-plugin" / ".claude-plugin"
        plugin_dir.mkdir(parents=True)
        (plugin_dir / "plugin.json").write_text('{"name": "test-plugin"}')

        result = validate_manifest(plugin_dir / "plugin.json")
        assert result.valid
        assert result.errors == []

    def test_missing_name(self, tmp_path: Path):
        """Manifest without name fails."""
        plugin_dir = tmp_path / "test-plugin" / ".claude-plugin"
        plugin_dir.mkdir(parents=True)
        (plugin_dir / "plugin.json").write_text('{"description": "test"}')

        result = validate_manifest(plugin_dir / "plugin.json")
        assert not result.valid
        assert "name" in result.errors[0]

    def test_array_paths_rejected(self, tmp_path: Path):
        """Arrays for component paths are rejected."""
        plugin_dir = tmp_path / "test-plugin" / ".claude-plugin"
        plugin_dir.mkdir(parents=True)
        (plugin_dir / "plugin.json").write_text(
            '{"name": "test", "agents": ["./agents/"]}'
        )

        result = validate_manifest(plugin_dir / "plugin.json")
        assert not result.valid
        assert "agents" in result.errors[0]


class TestHooksValidation:
    """Test hooks.json validation."""

    def test_valid_hooks(self, tmp_path: Path):
        """Valid hooks config passes."""
        hooks_file = tmp_path / "hooks.json"
        hooks_file.write_text(
            '{"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": []}]}}'
        )

        errors = validate_hooks(hooks_file)
        assert errors == []

    def test_array_format_rejected(self, tmp_path: Path):
        """Array format for hooks is rejected."""
        hooks_file = tmp_path / "hooks.json"
        hooks_file.write_text('{"hooks": [{"event": "PreToolUse"}]}')

        errors = validate_hooks(hooks_file)
        assert len(errors) == 1
        assert "object" in errors[0]

    def test_invalid_event_name(self, tmp_path: Path):
        """Unknown event names are flagged."""
        hooks_file = tmp_path / "hooks.json"
        hooks_file.write_text('{"hooks": {"InvalidEvent": []}}')

        errors = validate_hooks(hooks_file)
        assert len(errors) == 1
        assert "InvalidEvent" in errors[0]

    def test_valid_session_start(self, tmp_path: Path):
        """SessionStart without matcher is valid."""
        hooks_file = tmp_path / "hooks.json"
        hooks_file.write_text(
            '{"hooks": {"SessionStart": [{"hooks": [{"type": "command"}]}]}}'
        )

        errors = validate_hooks(hooks_file)
        assert errors == []


class TestMarketplaceValidation:
    """Test all plugins in the marketplace."""

    @pytest.fixture
    def plugins_dir(self) -> Path:
        return PLUGINS_DIR

    def test_plugins_dir_exists(self, plugins_dir: Path):
        """Plugins directory exists."""
        assert plugins_dir.exists(), f"Plugins dir not found: {plugins_dir}"

    def test_discover_plugins(self, plugins_dir: Path):
        """Can discover plugins with manifests."""
        plugins = discover_plugins(plugins_dir)
        assert len(plugins) >= 9, "Expected at least 9 plugins"

    def test_all_manifests_valid(self, plugins_dir: Path):
        """All plugin manifests pass validation."""
        results = validate_all(plugins_dir)

        failed = [r for r in results if not r.valid]
        if failed:
            msg = "\n".join(
                f"  {r.plugin_name}: {', '.join(r.errors)}" for r in failed
            )
            pytest.fail(f"Invalid plugins:\n{msg}")

    @pytest.mark.parametrize(
        "plugin_name",
        [
            "core-1337",
            "eval-1337",
            "rust-1337",
            "sensei-1337",
            "terminal-1337",
            "experience-1337",
            "1337-extension-builder",
            "kotlin-1337",
            "jvm-analysis-1337",
        ],
    )
    def test_specific_plugin_valid(self, plugins_dir: Path, plugin_name: str):
        """Individual plugin validation."""
        result = validate_plugin(plugins_dir / plugin_name)
        assert result.valid, f"{plugin_name} invalid: {result.errors}"


class TestSessionStartHook:
    """Test the session-start.sh hook script."""

    @pytest.fixture
    def project_root(self) -> Path:
        return Path(__file__).parent.parent.parent

    @pytest.fixture
    def hook_script(self, project_root: Path) -> Path:
        return project_root / "plugins" / "core-1337" / "hooks" / "session-start.sh"

    @pytest.fixture
    def marketplace_json(self, project_root: Path) -> Path:
        return project_root / ".claude-plugin" / "marketplace.json"

    def test_hook_script_exists(self, hook_script: Path):
        """Hook script exists and is executable."""
        assert hook_script.exists(), f"Hook script not found: {hook_script}"
        assert hook_script.stat().st_mode & 0o111, "Hook script not executable"

    def test_hook_script_is_posix(self, hook_script: Path):
        """Hook script uses POSIX shell, not bash-isms."""
        content = hook_script.read_text()
        assert content.startswith("#!/bin/sh"), "Should use #!/bin/sh for POSIX"
        assert "[[" not in content, "Should not use [[ ]] (bash-ism)"

    def test_hook_outputs_core_1337(
        self, hook_script: Path, project_root: Path, tmp_path: Path
    ):
        """Hook always outputs core-1337 load instruction."""
        import json
        import subprocess

        # Create mock known_marketplaces.json pointing to project root
        mock_home = tmp_path / "mock_home" / ".claude" / "plugins"
        mock_home.mkdir(parents=True)

        marketplaces = {"claude-1337": {"installLocation": str(project_root)}}
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

    def test_hook_extracts_triggers(
        self, hook_script: Path, project_root: Path, tmp_path: Path
    ):
        """Hook extracts triggers from marketplace.json."""
        import json
        import subprocess

        mock_home = tmp_path / "mock_home" / ".claude" / "plugins"
        mock_home.mkdir(parents=True)

        marketplaces = {"claude-1337": {"installLocation": str(project_root)}}
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
        import subprocess

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
