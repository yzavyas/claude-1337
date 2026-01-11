"""Plugin validation tests."""

from pathlib import Path

import pytest

from evals_1337.targets.plugins import (
    HookAction,
    HookEntry,
    HooksConfig,
    PluginManifest,
    discover_plugins,
    validate_all,
    validate_hooks,
    validate_manifest,
    validate_plugin,
)

# Resolve plugins directory relative to this file
# evals/tests/test_plugins.py -> evals -> claude-1337 -> plugins
PLUGINS_DIR = Path(__file__).parent.parent.parent / "plugins"


class TestPluginManifestSchema:
    """Test the manifest schema validation."""

    def test_minimal_valid(self):
        """Minimal valid manifest."""
        manifest = PluginManifest(
            name="test-plugin",
            description="Test. Use when: testing.",
            version="0.1.0",
        )
        assert manifest.name == "test-plugin"

    def test_full_valid(self):
        """Full valid manifest with all optional fields."""
        manifest = PluginManifest(
            name="test-plugin",
            description="Test. Use when: testing.",
            version="0.1.0",
            author={"name": "tester", "email": "test@example.com"},
            license="MIT",
            keywords=["test", "example"],
            agents="./agents",
        )
        assert manifest.agents == "./agents"

    def test_agents_must_be_string(self):
        """Arrays are invalid for component paths."""
        with pytest.raises(Exception):
            PluginManifest(
                name="test",
                description="Test",
                version="0.1.0",
                agents=["./agents/"],  # type: ignore - intentionally wrong
            )


class TestHooksSchema:
    """Test the hooks.json schema validation (nested object format)."""

    def test_valid_hooks(self):
        """Valid hooks config with nested format."""
        config = HooksConfig(
            hooks={
                "PreToolUse": [
                    HookEntry(
                        matcher="Bash",
                        hooks=[HookAction(type="command", command="./test.sh")]
                    )
                ]
            }
        )
        assert "PreToolUse" in config.hooks
        assert len(config.hooks["PreToolUse"]) == 1

    def test_hooks_must_be_dict(self):
        """Hooks must be dict with event names, not array."""
        with pytest.raises(Exception):
            HooksConfig(
                hooks=[  # type: ignore - intentionally wrong (array format)
                    {"event": "PreToolUse", "script": "./test.sh"}
                ]
            )

    def test_hook_entry_requires_hooks_list(self):
        """Each hook entry needs a hooks list with actions."""
        with pytest.raises(Exception):
            HooksConfig(
                hooks={
                    "PreToolUse": [
                        {"matcher": "Bash"}  # type: ignore - missing hooks list
                    ]
                }
            )

    def test_valid_session_start_hook(self):
        """SessionStart hook without matcher."""
        config = HooksConfig(
            description="Test hooks",
            hooks={
                "SessionStart": [
                    HookEntry(
                        hooks=[HookAction(type="command", command="./load-context.sh")]
                    )
                ]
            }
        )
        assert config.description == "Test hooks"
        assert "SessionStart" in config.hooks


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
        assert len(plugins) > 0, "No plugins found"

    def test_all_manifests_valid(self, plugins_dir: Path):
        """All plugin manifests pass schema validation."""
        results = validate_all(plugins_dir, use_cli=False)

        failed = [r for r in results if not r.valid]
        if failed:
            msg = "\n".join(
                f"  {r.plugin_name}: {', '.join(r.errors)}" for r in failed
            )
            pytest.fail(f"Invalid plugin manifests:\n{msg}")

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
        manifest_path = plugins_dir / plugin_name / ".claude-plugin" / "plugin.json"
        if not manifest_path.exists():
            pytest.skip(f"{plugin_name} has no plugin.json")

        result = validate_manifest(manifest_path)
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

    def test_hook_outputs_core_1337(self, hook_script: Path, project_root: Path, tmp_path: Path):
        """Hook always outputs core-1337 load instruction."""
        import subprocess
        import json

        # Create mock known_marketplaces.json pointing to project root
        mock_home = tmp_path / "mock_home" / ".claude" / "plugins"
        mock_home.mkdir(parents=True)

        marketplaces = {
            "claude-1337": {
                "installLocation": str(project_root)
            }
        }
        (mock_home / "known_marketplaces.json").write_text(json.dumps(marketplaces))

        # Run script with mock HOME
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

    def test_hook_extracts_triggers(self, hook_script: Path, project_root: Path, tmp_path: Path):
        """Hook extracts triggers from marketplace.json."""
        import subprocess
        import json

        # Create mock known_marketplaces.json
        mock_home = tmp_path / "mock_home" / ".claude" / "plugins"
        mock_home.mkdir(parents=True)

        marketplaces = {
            "claude-1337": {
                "installLocation": str(project_root)
            }
        }
        (mock_home / "known_marketplaces.json").write_text(json.dumps(marketplaces))

        env = {"HOME": str(tmp_path / "mock_home")}
        result = subprocess.run(
            ["/bin/sh", str(hook_script)],
            capture_output=True,
            text=True,
            env=env,
        )

        assert result.returncode == 0
        # Should have extracted some plugin triggers
        assert "rust-1337" in result.stdout, "Should list rust-1337"
        assert "terminal-1337" in result.stdout, "Should list terminal-1337"
        assert "SKILL.md" in result.stdout, "Should include path to SKILL.md"

    def test_hook_graceful_no_marketplace(self, hook_script: Path, tmp_path: Path):
        """Hook handles missing marketplace gracefully."""
        import subprocess

        # Empty HOME with no marketplaces
        mock_home = tmp_path / "empty_home"
        mock_home.mkdir()

        env = {"HOME": str(mock_home)}
        result = subprocess.run(
            ["/bin/sh", str(hook_script)],
            capture_output=True,
            text=True,
            env=env,
        )

        # Should not crash, should still output core-1337 header
        assert result.returncode == 0, f"Script failed: {result.stderr}"
        assert "claude-1337" in result.stdout
