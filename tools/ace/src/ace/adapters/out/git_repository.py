"""Git source adapter - fetches packages from git repos."""

from pathlib import Path

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

from ace.adapters.out.scanners import ClaudePluginScanner, SkillOnlyScanner
from ace.domain.models import Package, Source
from ace.ports.out.scanner import ScannerPort


class SourceError(Exception):
    """Error interacting with a source."""

    pass


class GitSourceAdapter:
    """Fetches packages from git-based sources."""

    def __init__(self, cache_dir: Path, scanner: ScannerPort | None = None):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._scanner = scanner

    def _source_path(self, source: Source) -> Path:
        return self.cache_dir / source.name

    def _get_scanner(self, path: Path) -> ScannerPort:
        """Get appropriate scanner for the source directory."""
        if self._scanner:
            return self._scanner

        # Auto-detect: try Claude plugin format first, then skill-only
        claude_scanner = ClaudePluginScanner()
        if claude_scanner.can_scan(path):
            return claude_scanner

        skill_scanner = SkillOnlyScanner()
        if skill_scanner.can_scan(path):
            return skill_scanner

        # Default to Claude plugin scanner
        return claude_scanner

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

        scanner = self._get_scanner(path)
        return scanner.scan(path)

    def get_package(self, source: Source, name: str) -> Package | None:
        """Get a specific package by name."""
        for package in self.list_packages(source):
            if package.name == name:
                return package
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
