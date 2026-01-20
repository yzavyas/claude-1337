"""Claude Code target adapter - installs packages to Claude Code."""

import shutil
from pathlib import Path

from ace.domain.models import Package


class ClaudeCodeTargetAdapter:
    """Installs packages to Claude Code's plugin directory."""

    def __init__(self, global_config: bool = True, project_path: Path | None = None):
        self.global_config = global_config
        self.project_path = project_path

    @property
    def name(self) -> str:
        return "claude-code"

    def _config_path(self) -> Path:
        if self.global_config:
            return Path.home() / ".claude"
        elif self.project_path:
            return self.project_path / ".claude"
        else:
            return Path.cwd() / ".claude"

    def is_available(self) -> bool:
        """Check if Claude Code is available."""
        claude_dir = Path.home() / ".claude"
        return claude_dir.exists() or shutil.which("claude") is not None

    def install(self, package: Package, source_path: Path) -> None:
        """Install a package to Claude Code."""
        config_dir = self._config_path()
        dest_dir = config_dir / "plugins" / package.name

        if dest_dir.exists():
            shutil.rmtree(dest_dir)

        shutil.copytree(source_path, dest_dir)

    def uninstall(self, package: Package) -> None:
        """Remove a package from Claude Code."""
        config_dir = self._config_path()
        dest_dir = config_dir / "plugins" / package.name

        if dest_dir.exists():
            shutil.rmtree(dest_dir)

    def is_installed(self, package: Package) -> bool:
        """Check if a package is installed."""
        config_dir = self._config_path()
        return (config_dir / "plugins" / package.name).exists()

    def get_config_path(self) -> str:
        return str(self._config_path())
