"""Filesystem registry adapter - stores state in JSON files."""

import json
from datetime import datetime
from pathlib import Path

from ace.domain.models import Installation, Package, PackageContents, Source


class FilesystemRegistryAdapter:
    """Stores ace state in filesystem JSON files."""

    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self._sources_file = config_dir / "sources.json"
        self._installs_file = config_dir / "installations.json"

    def _load_sources(self) -> dict:
        if self._sources_file.exists():
            return json.loads(self._sources_file.read_text())
        return {}

    def _save_sources(self, sources: dict) -> None:
        self._sources_file.write_text(json.dumps(sources, indent=2))

    def _load_installs(self) -> dict:
        if self._installs_file.exists():
            return json.loads(self._installs_file.read_text())
        return {}

    def _save_installs(self, installs: dict) -> None:
        self._installs_file.write_text(json.dumps(installs, indent=2))

    # Source methods

    def list_sources(self) -> list[Source]:
        sources = self._load_sources()
        return [
            Source(
                name=name,
                url=data["url"],
                default=data.get("default", False),
                ref=data.get("ref"),
            )
            for name, data in sources.items()
        ]

    def add_source(self, source: Source) -> None:
        sources = self._load_sources()

        if source.default:
            for name in sources:
                sources[name]["default"] = False

        sources[source.name] = {
            "url": source.url,
            "default": source.default,
            "ref": source.ref,
        }
        self._save_sources(sources)

    def remove_source(self, name: str) -> None:
        sources = self._load_sources()
        if name in sources:
            del sources[name]
            self._save_sources(sources)

    def get_source(self, name: str) -> Source | None:
        sources = self._load_sources()
        if name not in sources:
            return None
        data = sources[name]
        return Source(
            name=name,
            url=data["url"],
            default=data.get("default", False),
            ref=data.get("ref"),
        )

    # Installation methods

    def list_installations(self, target: str | None = None) -> list[Installation]:
        installs = self._load_installs()
        result = []

        for install_id, data in installs.items():
            if target and data.get("target") != target:
                continue

            pkg_data = data["package"]
            source_data = data["source"]

            contents = PackageContents(**pkg_data.get("contents", {}))

            package = Package(
                name=pkg_data["name"],
                description=pkg_data.get("description", ""),
                version=pkg_data.get("version", "0.0.0"),
                path=Path(pkg_data["path"]),
                contents=contents,
            )

            source = Source(
                name=source_data["name"],
                url=source_data["url"],
                default=source_data.get("default", False),
                ref=source_data.get("ref"),
            )

            result.append(Installation(
                package=package,
                source=source,
                installed_at=datetime.fromisoformat(data["installed_at"]),
                commit=data.get("commit", ""),
                target=data.get("target", "claude-code"),
            ))

        return result

    def add_installation(self, installation: Installation) -> None:
        installs = self._load_installs()

        installs[installation.id] = {
            "package": {
                "name": installation.package.name,
                "description": installation.package.description,
                "version": installation.package.version,
                "path": str(installation.package.path),
                "contents": installation.package.contents.model_dump(),
            },
            "source": {
                "name": installation.source.name,
                "url": installation.source.url,
                "default": installation.source.default,
                "ref": installation.source.ref,
            },
            "installed_at": installation.installed_at.isoformat(),
            "commit": installation.commit,
            "target": installation.target,
        }

        self._save_installs(installs)

    def remove_installation(self, installation_id: str) -> None:
        installs = self._load_installs()
        if installation_id in installs:
            del installs[installation_id]
            self._save_installs(installs)

    def get_installation(self, installation_id: str) -> Installation | None:
        for inst in self.list_installations():
            if inst.id == installation_id:
                return inst
        return None
