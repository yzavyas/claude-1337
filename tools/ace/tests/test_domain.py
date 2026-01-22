"""Tests for domain models."""

from datetime import datetime
from pathlib import Path

from ace.domain.models import (
    Extension,
    ExtensionType,
    Installation,
    Package,
    PackageContents,
    Source,
)


class TestExtension:
    """Tests for Extension model."""

    def test_extension_id(self):
        """Extension ID is type/name."""
        ext = Extension(
            name="wolf",
            type=ExtensionType.AGENT,
            path=Path("agents/wolf.md"),
        )
        assert ext.id == "agent/wolf"

    def test_extension_types(self):
        """All extension types work correctly."""
        for ext_type in ExtensionType:
            ext = Extension(
                name="test",
                type=ext_type,
                path=Path(f"{ext_type.value}/test"),
            )
            assert ext.type == ext_type


class TestPackageContents:
    """Tests for PackageContents model."""

    def test_empty_contents(self):
        """Empty contents has zero total."""
        contents = PackageContents()
        assert contents.total == 0
        assert contents.summary == "empty"

    def test_contents_with_items(self):
        """Contents counts items correctly."""
        contents = PackageContents(
            skills=["core", "rust"],
            agents=["wolf"],
            hooks=["hooks.json"],
            mcp=[],
        )
        assert contents.total == 4
        assert "2 skill(s)" in contents.summary
        assert "1 agent(s)" in contents.summary
        assert "1 hook(s)" in contents.summary


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

    def test_package_with_contents(self):
        """Package can have contents."""
        pkg = Package(
            name="core-1337",
            description="Engineering excellence",
            version="1.0.0",
            path=Path("plugins/core-1337"),
            contents=PackageContents(skills=["core"], agents=["wolf"]),
        )
        assert pkg.contents.total == 2


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
