"""Git source adapter - fetches packages from git repos."""

import json
from pathlib import Path

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

from ace.domain.models import Package, PackageContents, Source


class SourceError(Exception):
    """Error interacting with a source."""

    pass


class GitSourceAdapter:
    """Fetches packages from git-based sources."""

    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _source_path(self, source: Source) -> Path:
        return self.cache_dir / source.name

    def fetch(self, source: Source) -> None:
        """Fetch/clone source to local cache."""
        path = self._source_path(source)

        if path.exists():
            try:
                repo = Repo(path)
                repo.remotes.origin.fetch()
                if source.ref:
                    repo.git.checkout(source.ref)
            except (InvalidGitRepositoryError, GitCommandError) as e:
                raise SourceError(f"Failed to update {source.name}: {e}") from e
        else:
            try:
                repo = Repo.clone_from(source.url, path)
                if source.ref:
                    repo.git.checkout(source.ref)
            except GitCommandError as e:
                raise SourceError(f"Failed to clone {source.name}: {e}") from e

    def list_packages(self, source: Source) -> list[Package]:
        """List all packages in a source."""
        path = self._source_path(source)
        if not path.exists():
            self.fetch(source)

        seen: set[str] = set()
        packages: list[Package] = []

        for plugin_json in path.glob("**/.claude-plugin/plugin.json"):
            pkg = self._parse_package(plugin_json)
            if pkg and pkg.name not in seen:
                seen.add(pkg.name)
                packages.append(pkg)

        return packages

    def _parse_package(self, plugin_json: Path) -> Package | None:
        """Parse a plugin.json into a Package."""
        try:
            data = json.loads(plugin_json.read_text())
            pkg_dir = plugin_json.parent.parent

            contents = self._scan_contents(pkg_dir)

            return Package(
                name=data.get("name", pkg_dir.name),
                description=data.get("description", ""),
                version=data.get("version", "0.0.0"),
                path=pkg_dir,
                contents=contents,
            )
        except Exception:
            return None

    def _scan_contents(self, pkg_dir: Path) -> PackageContents:
        """Scan package directory for extensions."""
        skills: list[str] = []
        agents: list[str] = []
        hooks: list[str] = []
        mcp: list[str] = []

        # Skills
        skills_dir = pkg_dir / "skills"
        if skills_dir.exists():
            for skill_md in skills_dir.glob("**/SKILL.md"):
                skills.append(skill_md.parent.name)

        # Agents
        agents_dir = pkg_dir / "agents"
        if agents_dir.exists():
            for agent_md in agents_dir.glob("*.md"):
                agents.append(agent_md.stem)

        # Hooks
        if (pkg_dir / "hooks.json").exists():
            hooks.append("hooks.json")

        # MCP
        for mcp_name in ["mcp.json", ".mcp.json"]:
            if (pkg_dir / mcp_name).exists():
                mcp.append(mcp_name)
                break

        return PackageContents(skills=skills, agents=agents, hooks=hooks, mcp=mcp)

    def get_package(self, source: Source, name: str) -> Package | None:
        """Get a specific package by name."""
        for pkg in self.list_packages(source):
            if pkg.name == name:
                return pkg
        return None

    def get_package_path(self, source: Source, package: Package) -> Path:
        """Get local filesystem path to package."""
        return package.path

    def get_commit(self, source: Source) -> str:
        """Get current commit hash of source."""
        path = self._source_path(source)
        try:
            return Repo(path).head.commit.hexsha
        except Exception:
            return ""
