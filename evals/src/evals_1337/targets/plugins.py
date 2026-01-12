"""Plugin validation using official Claude Code CLI."""

import json
import subprocess
from pathlib import Path
from typing import NamedTuple


class ValidationResult(NamedTuple):
    plugin_name: str
    valid: bool
    errors: list[str]


VALID_HOOK_EVENTS = {
    "PreToolUse",
    "PostToolUse",
    "UserPromptSubmit",
    "Stop",
    "SubagentStop",
    "SessionStart",
    "SessionEnd",
    "PreCompact",
    "Notification",
    "PermissionRequest",
}


def validate_json(path: Path) -> tuple[dict | None, str | None]:
    """Load and validate JSON file. Returns (data, error)."""
    if not path.exists():
        return None, f"{path.name} not found"
    try:
        with open(path) as f:
            return json.load(f), None
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON: {e}"


def validate_manifest(manifest_path: Path) -> ValidationResult:
    """Validate plugin.json - just check it's valid JSON with required fields."""
    plugin_name = manifest_path.parent.parent.name

    data, error = validate_json(manifest_path)
    if error:
        return ValidationResult(plugin_name, False, [error])

    errors = []

    # Required field
    if "name" not in data:
        errors.append("missing required field: name")

    # Common gotcha: arrays instead of strings for paths
    for field in ["agents", "commands", "hooks", "skills"]:
        if field in data and isinstance(data[field], list):
            errors.append(f"{field}: must be string path, not array")

    return ValidationResult(plugin_name, len(errors) == 0, errors)


def validate_hooks(hooks_path: Path) -> list[str]:
    """Validate hooks.json structure."""
    if not hooks_path.exists():
        return []  # No hooks is valid

    data, error = validate_json(hooks_path)
    if error:
        return [f"hooks.json: {error}"]

    errors = []

    # Must have hooks field as dict (not array - common mistake)
    if "hooks" not in data:
        errors.append("hooks.json: missing 'hooks' field")
        return errors

    if isinstance(data["hooks"], list):
        errors.append(
            "hooks.json: 'hooks' must be object with event names as keys, not array"
        )
        return errors

    if not isinstance(data["hooks"], dict):
        errors.append("hooks.json: 'hooks' must be object")
        return errors

    # Validate event names
    for event_name in data["hooks"]:
        if event_name not in VALID_HOOK_EVENTS:
            errors.append(f"hooks.json: unknown event '{event_name}'")

    return errors


def validate_plugin(plugin_path: Path) -> ValidationResult:
    """Validate a plugin's manifest and hooks."""
    plugin_name = plugin_path.name
    errors = []

    # Validate manifest
    manifest_path = plugin_path / ".claude-plugin" / "plugin.json"
    manifest_result = validate_manifest(manifest_path)
    errors.extend(manifest_result.errors)

    # Validate hooks if present
    hooks_path = plugin_path / "hooks" / "hooks.json"
    errors.extend(validate_hooks(hooks_path))

    return ValidationResult(plugin_name, len(errors) == 0, errors)


def discover_plugins(plugins_dir: Path) -> list[Path]:
    """Find all plugins with plugin.json manifests."""
    plugins = []
    for plugin_dir in plugins_dir.iterdir():
        if plugin_dir.is_dir():
            manifest = plugin_dir / ".claude-plugin" / "plugin.json"
            if manifest.exists():
                plugins.append(plugin_dir)
    return sorted(plugins)


def validate_all(plugins_dir: Path) -> list[ValidationResult]:
    """Validate all plugins in a directory."""
    return [validate_plugin(p) for p in discover_plugins(plugins_dir)]
