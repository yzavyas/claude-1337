"""Tests for domain models."""

from datetime import datetime
from pathlib import Path

from ace.domain.models import (
    Extensions,
    ExtensionType,
    Installation,
    Package,
    Source,
)


class TestExtensionType:
    """Tests for ExtensionType enum."""

    def test_extension_types_exist(self):
        """All extension types are defined."""
        assert ExtensionType.SKILL == "skill"
        assert ExtensionType.AGENT == "agent"
        assert ExtensionType.HOOK == "hook"
        assert ExtensionType.MCP == "mcp"


class TestExtensions:
    """Tests for Extensions model."""

    def test_empty_extensions(self):
        """Empty extensions has zero total."""
        ext = Extensions()
        assert ext.total == 0
        assert ext.summary == "empty"

    def test_extensions_with_items(self):
        """Extensions counts items correctly."""
        ext = Extensions(
            skills=["core", "rust"],
            agents=["wolf"],
            hooks=["hooks.json"],
            mcps=[],
        )
        assert ext.total == 4
        assert "2 skill(s)" in ext.summary
        assert "1 agent(s)" in ext.summary
        assert "1 hook(s)" in ext.summary


class TestPackage:
    """Tests for Package model."""

    def test_package_basic(self):
        """Package has required fields."""
        pkg = Package(
            name="core-1337",
            path=Path("plugins/core-1337"),
        )
        assert pkg.name == "core-1337"
        assert pkg.version == "0.0.0"  # default
        assert pkg.description == ""  # default

    def test_package_with_extensions(self):
        """Package can have extensions."""
        pkg = Package(
            name="core-1337",
            description="Engineering excellence",
            version="1.0.0",
            path=Path("plugins/core-1337"),
            extensions=Extensions(skills=["core"], agents=["wolf"]),
        )
        assert pkg.extensions.total == 2


class TestSource:
    """Tests for Source model."""

    def test_source_not_pinned_by_default(self):
        """Source is not pinned without ref."""
        source = Source(name="test", url="https://github.com/test/test")
        assert not source.is_pinned

    def test_source_pinned_with_ref(self):
        """Source is pinned when ref is set."""
        source = Source(
            name="test",
            url="https://github.com/test/test",
            ref="v1.0.0",
        )
        assert source.is_pinned


class TestInstallation:
    """Tests for Installation model."""

    def test_installation_id(self):
        """Installation ID is source/package."""
        pkg = Package(
            name="core-1337",
            path=Path("plugins/core-1337"),
        )
        source = Source(name="claude-1337", url="https://github.com/test/test")
        inst = Installation(package=pkg, source=source)

        assert inst.id == "claude-1337/core-1337"

    def test_installation_has_timestamp(self):
        """Installation records install time."""
        pkg = Package(name="test", path=Path("test"))
        source = Source(name="test", url="https://example.com")
        inst = Installation(package=pkg, source=source)

        assert isinstance(inst.installed_at, datetime)
