"""Atomic capability scanners - composable building blocks."""

from pathlib import Path


class SkillScanner:
    """Finds skills (SKILL.md files)."""

    def scan(self, root: Path) -> list[str]:
        """Return list of skill names found."""
        skills = []
        for skill_md in root.glob("**/SKILL.md"):
            # Skip if inside node_modules or hidden dirs
            if any(p.startswith(".") or p == "node_modules" for p in skill_md.parts):
                continue
            skills.append(skill_md.parent.name)
        return skills


class AgentScanner:
    """Finds agents (agents/*.md files)."""

    def scan(self, root: Path) -> list[str]:
        """Return list of agent names found."""
        agents_dir = root / "agents"
        if not agents_dir.exists():
            return []
        return [p.stem for p in agents_dir.glob("*.md")]


class HookScanner:
    """Finds hooks (hooks.json)."""

    def scan(self, root: Path) -> list[str]:
        """Return list of hook files found."""
        if (root / "hooks.json").exists():
            return ["hooks.json"]
        return []


class McpScanner:
    """Finds MCP configs (mcp.json or .mcp.json)."""

    def scan(self, root: Path) -> list[str]:
        """Return list of MCP configs found."""
        for name in ["mcp.json", ".mcp.json"]:
            if (root / name).exists():
                return [name]
        return []


class CommandScanner:
    """Finds commands (commands/*.md files)."""

    def scan(self, root: Path) -> list[str]:
        """Return list of command names found."""
        commands_dir = root / "commands"
        if not commands_dir.exists():
            return []
        return [p.stem for p in commands_dir.glob("*.md")]
