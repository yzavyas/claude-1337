"""Claude Code plugin scanner - .claude-plugin/plugin.json format.

Composes atomic extension scanners within plugin boundaries.
"""

import json
from pathlib import Path

from ace.adapters.out.scanners.capability_scanners import (
    AgentScanner,
    HookScanner,
    McpScanner,
    SkillScanner,
)
from ace.domain.models import Extensions, Package


class ClaudePluginScanner:
    """Scans for Claude Code plugins.

    Composes: SkillScanner + AgentScanner + HookScanner + McpScanner
    within .claude-plugin boundaries.
    """

    def __init__(self):
        self._skill = SkillScanner()
        self._agent = AgentScanner()
        self._hook = HookScanner()
        self._mcp = McpScanner()

    def can_scan(self, root_path: Path) -> bool:
        return any(root_path.glob("**/.claude-plugin/plugin.json"))

    def scan(self, root_path: Path) -> list[Package]:
        seen: set[str] = set()
        packages: list[Package] = []

        for plugin_json in root_path.glob("**/.claude-plugin/plugin.json"):
            package = self._parse(plugin_json)
            if package and package.name not in seen:
                seen.add(package.name)
                packages.append(package)

        return packages

    def _parse(self, plugin_json: Path) -> Package | None:
        try:
            data = json.loads(plugin_json.read_text())
            pkg_dir = plugin_json.parent.parent

            # Compose extension scanners within this package's directory
            skills_dir = pkg_dir / "skills"
            extensions = Extensions(
                skills=self._skill.scan(skills_dir) if skills_dir.exists() else [],
                agents=self._agent.scan(pkg_dir),
                hooks=self._hook.scan(pkg_dir),
                mcps=self._mcp.scan(pkg_dir),
            )

            return Package(
                name=data.get("name", pkg_dir.name),
                description=data.get("description", ""),
                version=data.get("version", "0.0.0"),
                path=pkg_dir,
                extensions=extensions,
            )
        except Exception:
            return None
