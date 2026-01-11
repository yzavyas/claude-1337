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
