"""Application use cases - orchestrates domain operations through ports."""

from datetime import datetime

from ace.domain.models import Installation, Package, Source
from ace.ports.out import RegistryPort, SourcePort, TargetPort


class Ace:
    """Application facade for ace.

    Orchestrates: source management, package discovery, installation.
    """

    def __init__(
        self,
        source_port: SourcePort,
        registry_port: RegistryPort,
        targets: dict[str, TargetPort],
    ):
        self._source = source_port
        self._registry = registry_port
        self._targets = targets

    # === Source Management ===

    def add_source(
        self, url: str, name: str | None = None, set_default: bool = False
    ) -> Source:
        if not name:
            name = self._derive_source_name(url)

        source = Source(name=name, url=url, default=set_default)
        self._source.fetch(source)
        self._registry.add_source(source)
        return source

    def _derive_source_name(self, url: str) -> str:
        name = url.rstrip("/").split("/")[-1]
        if name.endswith(".git"):
            name = name[:-4]
        return name

    def remove_source(self, name: str) -> None:
        self._registry.remove_source(name)

    def list_sources(self) -> list[Source]:
        return self._registry.list_sources()

    def get_source(self, name: str) -> Source | None:
        return self._registry.get_source(name)

    def refresh_source(self, name: str | None = None) -> None:
        sources = self._registry.list_sources()
        if name:
            sources = [s for s in sources if s.name == name]
        for source in sources:
            self._source.fetch(source)

    # === Package Discovery ===

    def list_packages(
        self, source_name: str | None = None
    ) -> list[tuple[Source, Package]]:
        results: list[tuple[Source, Package]] = []

        sources = self._registry.list_sources()
        if source_name:
            sources = [s for s in sources if s.name == source_name]

        for source in sources:
            try:
                packages = self._source.list_packages(source)
                for package in packages:
                    results.append((source, package))
            except Exception:
                continue

        return results

    def get_package(
        self, source_name: str, package_name: str
    ) -> tuple[Source, Package] | None:
        source = self._registry.get_source(source_name)
        if not source:
            return None

        package = self._source.get_package(source, package_name)
        if not package:
            return None

        return (source, package)

    # === Installation ===

    def install(
        self,
        package_ref: str,
        target: str = "claude-code",
        pin_commit: bool = True,
    ) -> Installation:
        """Install a package.

        package_ref can be:
        - "package-name" (uses default source)
        - "source/package-name" (explicit source)
        """
        if "/" in package_ref:
            source_name, package_name = package_ref.split("/", 1)
        else:
            sources = self._registry.list_sources()
            default_sources = [s for s in sources if s.default]
            if not default_sources:
                raise ValueError("No default source. Use source/package format.")
            source_name = default_sources[0].name
            package_name = package_ref

        source = self._registry.get_source(source_name)
        if not source:
            raise ValueError(f"Source not found: {source_name}")

        package = self._source.get_package(source, package_name)
        if not package:
            raise ValueError(f"Package not found: {package_name}")

        target_port = self._targets.get(target)
        if not target_port:
            raise ValueError(f"Unknown target: {target}")

        if not target_port.is_available():
            raise ValueError(f"Target not available: {target}")

        source_path = self._source.get_package_path(source, package)
        target_port.install(package, source_path)

        commit = self._source.get_commit(source) if pin_commit else ""
        installation = Installation(
            package=package,
            source=source,
            installed_at=datetime.now(),
            commit=commit,
            target=target,
        )
        self._registry.add_installation(installation)

        return installation

    def uninstall(self, package_ref: str) -> None:
        installations = self._registry.list_installations()
        matching = [
            i for i in installations if package_ref in i.id or i.package.name == package_ref
        ]

        if not matching:
            raise ValueError(f"Not installed: {package_ref}")

        for inst in matching:
            target_port = self._targets.get(inst.target)
            if target_port:
                target_port.uninstall(inst.package)
            self._registry.remove_installation(inst.id)

    def list_installed(self, target: str | None = None) -> list[Installation]:
        return self._registry.list_installations(target)

    def update(self, package_ref: str | None = None) -> list[Installation]:
        installations = self._registry.list_installations()
        if package_ref:
            installations = [i for i in installations if package_ref in i.id]

        updated = []
        for inst in installations:
            self._source.fetch(inst.source)

            target_port = self._targets.get(inst.target)
            if not target_port:
                continue

            package = self._source.get_package(inst.source, inst.package.name)
            if not package:
                continue

            source_path = self._source.get_package_path(inst.source, package)
            target_port.install(package, source_path)

            new_install = Installation(
                package=package,
                source=inst.source,
                installed_at=datetime.now(),
                commit=self._source.get_commit(inst.source),
                target=inst.target,
            )
            self._registry.remove_installation(inst.id)
            self._registry.add_installation(new_install)
            updated.append(new_install)

        return updated

    # === Info ===

    def list_targets(self) -> list[str]:
        return [name for name, t in self._targets.items() if t.is_available()]
