"""Plugin manifest validation."""

import json
import subprocess
from pathlib import Path
from typing import NamedTuple

from pydantic import BaseModel, ValidationError


class Author(BaseModel):
    name: str
    email: str | None = None


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
            manifest = plugin_path / ".claude-plugin" / "plugin.json"
            result = validate_manifest(manifest)
        results.append(result)
    return results
