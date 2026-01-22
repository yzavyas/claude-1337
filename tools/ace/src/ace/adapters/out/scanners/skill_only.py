"""Skill-only scanner - repos with just SKILL.md files (no plugin manifest).

Each skill becomes its own package (skill-as-package).
"""

import re
from pathlib import Path

from ace.domain.models import Extensions, Package


class SkillOnlyScanner:
    """Scans for standalone skills (SKILL.md without plugin.json).

    Structure (Vercel agent-skills style):
        skills/
        ├── skill-name/
        │   ├── SKILL.md
        │   └── scripts/deploy.sh
        └── another-skill/SKILL.md

    Each skill becomes its own package with a single extension.
    """

    def can_scan(self, root_path: Path) -> bool:
        has_skill_md = any(root_path.glob("**/SKILL.md"))
        has_plugin_json = any(root_path.glob("**/.claude-plugin/plugin.json"))
        return has_skill_md and not has_plugin_json

    def scan(self, root_path: Path) -> list[Package]:
        seen: set[str] = set()
        packages: list[Package] = []

        for skill_md in root_path.glob("**/SKILL.md"):
            # Skip hidden dirs and node_modules
            if any(p.startswith(".") or p == "node_modules" for p in skill_md.parts):
                continue

            package = self._parse(skill_md)
            if package and package.name not in seen:
                seen.add(package.name)
                packages.append(package)

        return packages

    def _parse(self, skill_md: Path) -> Package | None:
        try:
            content = skill_md.read_text()
            skill_dir = skill_md.parent
            name, description = self._parse_frontmatter(content, skill_dir.name)

            return Package(
                name=name,
                description=description,
                version="0.0.0",
                path=skill_dir,
                extensions=Extensions(skills=[name]),
            )
        except Exception:
            return None

    def _parse_frontmatter(self, content: str, fallback: str) -> tuple[str, str]:
        name, description = fallback, ""

        match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if match:
            for line in match.group(1).split("\n"):
                if line.startswith("name:"):
                    name = line.split(":", 1)[1].strip().strip('"\'')
                elif line.startswith("description:"):
                    description = line.split(":", 1)[1].strip().strip('"\'')

        return name, description
