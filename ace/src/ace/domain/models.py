"""Domain models for ace (Agentic Capability Extensions).

Ontology:
- Source: Where packages come from (marketplaces, git repos)
- Package: The installable bundle (core-1337, rust-1337)
- Extension: Individual capability inside a package (skill, agent, hook, mcp)

User-facing: "Add sources, install extensions"
Internal: Sources contain Packages, Packages contain Extensions
"""

from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field


class ExtensionType(str, Enum):
    """Extension modalities - the types of capability extensions."""

    SKILL = "skill"
    AGENT = "agent"
    HOOK = "hook"
    MCP = "mcp"


class Extension(BaseModel):
    """An individual extension within a package.

    Addressed as: package:type/name (e.g., core-1337:agent/wolf)
    """

    name: str
    type: ExtensionType
    path: Path

    model_config = {"frozen": True}

    @property
    def id(self) -> str:
        """Extension ID within package: type/name."""
        return f"{self.type.value}/{self.name}"


class PackageContents(BaseModel):
    """What's inside a package - the extensions it provides."""

    skills: list[str] = Field(default_factory=list)
    agents: list[str] = Field(default_factory=list)
    hooks: list[str] = Field(default_factory=list)
    mcp: list[str] = Field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.skills) + len(self.agents) + len(self.hooks) + len(self.mcp)

    @property
    def summary(self) -> str:
        """Human-readable summary of contents."""
        parts = []
        if self.skills:
            parts.append(f"{len(self.skills)} skill(s)")
        if self.agents:
            parts.append(f"{len(self.agents)} agent(s)")
        if self.hooks:
            parts.append(f"{len(self.hooks)} hook(s)")
        if self.mcp:
            parts.append(f"{len(self.mcp)} mcp")
        return ", ".join(parts) if parts else "empty"


class Package(BaseModel):
    """A package - the installable bundle containing extensions.

    User-facing term: "extension" (ace install core-1337)
    Internal term: "package"
    """

    name: str
    description: str = ""
    version: str = "0.0.0"
    path: Path
    contents: PackageContents = Field(default_factory=PackageContents)

    model_config = {"frozen": True}


class Source(BaseModel):
    """A source of packages (marketplace, git repo).

    Examples:
    - github.com/yzavyas/claude-1337
    - github.com/anthropics/claude-code-plugins
    """

    name: str
    url: str
    default: bool = False
    ref: str | None = None  # pinned commit/tag/branch

    model_config = {"frozen": True}

    @property
    def is_pinned(self) -> bool:
        return self.ref is not None


class Installation(BaseModel):
    """Record of an installed package."""

    package: Package
    source: Source
    installed_at: datetime = Field(default_factory=datetime.now)
    commit: str = ""  # git commit at install time
    target: str = "claude-code"

    @property
    def id(self) -> str:
        """Installation ID: source/package."""
        return f"{self.source.name}/{self.package.name}"
