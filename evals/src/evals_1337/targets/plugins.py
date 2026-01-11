"""Plugin manifest validation."""

import json
import subprocess
from pathlib import Path
from typing import Any, NamedTuple

from pydantic import BaseModel, ValidationError


class Author(BaseModel):
    name: str
    email: str | None = None


class HookAction(BaseModel):
    """Individual hook action (command or prompt)."""

    type: str  # "command" or "prompt"
    command: str | None = None
    prompt: str | None = None
    timeout: int | None = None


class HookEntry(BaseModel):
    """Hook entry with optional matcher."""

    matcher: str | None = None
    hooks: list[HookAction]


class HooksConfig(BaseModel):
    """Valid hooks.json schema (nested object format).

    Format:
    {
      "description": "optional",
      "hooks": {
        "PreToolUse": [{ "matcher": "...", "hooks": [{ "type": "command", "command": "..." }] }],
        "SessionStart": [{ "hooks": [{ "type": "command", "command": "..." }] }]
      }
    }
    """

    description: str | None = None
    hooks: dict[str, list[HookEntry]]


class PluginManifest(BaseModel):
    """Valid plugin.json schema."""

    name: str
    description: str
    version: str
    author: Author | None = None
    homepage: str | None = None
    repository: str | None = None
    license: str | None = None
    keywords: list[str] | None = None

    # Component paths - must be strings, not arrays
    commands: str | None = None
    agents: str | None = None
    hooks: str | None = None
    skills: str | None = None


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


def validate_manifest(manifest_path: Path) -> ValidationResult:
    """Validate a plugin.json file against the schema."""
    plugin_name = manifest_path.parent.parent.name
    errors = []

    if not manifest_path.exists():
        return ValidationResult(plugin_name, False, ["plugin.json not found"])

    try:
        with open(manifest_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return ValidationResult(plugin_name, False, [f"Invalid JSON: {e}"])

    try:
        PluginManifest(**data)
    except ValidationError as e:
        for error in e.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            errors.append(f"{field}: {error['msg']}")

    # Check for common gotchas
    for field in ["agents", "commands", "hooks", "skills"]:
        if field in data and isinstance(data[field], list):
            errors.append(f"{field}: must be string path, not array")

    return ValidationResult(plugin_name, len(errors) == 0, errors)


def validate_hooks(hooks_path: Path) -> list[str]:
    """Validate a hooks.json file against the correct nested format.

    Correct format:
    {
      "hooks": {
        "EventName": [{ "matcher": "...", "hooks": [{ "type": "command", "command": "..." }] }]
      }
    }

    Wrong format (array-based):
    {
      "hooks": [{ "event": "...", "script": "..." }]
    }
    """
    errors = []

    if not hooks_path.exists():
        return []  # No hooks is valid

    try:
        with open(hooks_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"hooks.json: Invalid JSON: {e}"]

    # Check for wrong array format (common mistake from old documentation)
    if "hooks" in data and isinstance(data["hooks"], list):
        errors.append(
            "hooks.json: 'hooks' must be an object with event names as keys, not an array. "
            "Use {\"hooks\": {\"PreToolUse\": [{\"hooks\": [...]}]}} format."
        )
        return errors

    # Check that hooks is present and is a dict
    if "hooks" not in data:
        errors.append("hooks.json: missing 'hooks' field")
        return errors

    if not isinstance(data["hooks"], dict):
        errors.append("hooks.json: 'hooks' must be an object with event names as keys")
        return errors

    # Validate event names
    for event_name in data["hooks"]:
        if event_name not in VALID_HOOK_EVENTS:
            errors.append(f"hooks.json: unknown event '{event_name}'. Valid: {', '.join(sorted(VALID_HOOK_EVENTS))}")

    # Validate structure with Pydantic
    try:
        HooksConfig(**data)
    except ValidationError as e:
        for error in e.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            errors.append(f"hooks.json {field}: {error['msg']}")

    return errors


def validate_plugin(plugin_path: Path) -> ValidationResult:
    """Validate a plugin including manifest and hooks."""
    plugin_name = plugin_path.name
    errors = []

    # Validate manifest
    manifest_path = plugin_path / ".claude-plugin" / "plugin.json"
    manifest_result = validate_manifest(manifest_path)
    errors.extend(manifest_result.errors)

    # Validate hooks if present
    hooks_path = plugin_path / "hooks" / "hooks.json"
    hooks_errors = validate_hooks(hooks_path)
    errors.extend(hooks_errors)

    return ValidationResult(plugin_name, len(errors) == 0, errors)


def validate_with_cli(plugin_path: Path) -> ValidationResult:
    """Validate using claude plugin validate command."""
    plugin_name = plugin_path.name

    try:
        result = subprocess.run(
            ["claude", "plugin", "validate", str(plugin_path)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return ValidationResult(plugin_name, True, [])
        else:
            return ValidationResult(plugin_name, False, [result.stderr.strip()])
    except FileNotFoundError:
        return ValidationResult(plugin_name, False, ["claude CLI not found"])
    except subprocess.TimeoutExpired:
        return ValidationResult(plugin_name, False, ["Validation timed out"])


def discover_plugins(plugins_dir: Path) -> list[Path]:
    """Find all plugins with plugin.json manifests."""
    plugins = []
    for plugin_dir in plugins_dir.iterdir():
        if plugin_dir.is_dir():
            manifest = plugin_dir / ".claude-plugin" / "plugin.json"
            if manifest.exists():
                plugins.append(plugin_dir)
    return sorted(plugins)


def validate_all(plugins_dir: Path, use_cli: bool = False) -> list[ValidationResult]:
    """Validate all plugins in a directory."""
    results = []
    for plugin_path in discover_plugins(plugins_dir):
        if use_cli:
            result = validate_with_cli(plugin_path)
        else:
            result = validate_plugin(plugin_path)
        results.append(result)
    return results
