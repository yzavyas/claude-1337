"""Domain models for ace (Agentic Capability Extensions).

Ontology:
- Source: Where packages come from (marketplaces, git repos)
- Package: The installable unit (core-1337, rust-1337)
- Extensions: What's inside a package (skills, agents, hooks, mcps)

User-facing: "Add sources, install packages"
"""

from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field


class ExtensionType(str, Enum):
    """Types of extensions a package can provide."""

    SKILL = "skill"
    AGENT = "agent"
    HOOK = "hook"
    MCP = "mcp"


class Extensions(BaseModel):
    """What's inside a package."""

    skills: list[str] = Field(default_factory=list)
    agents: list[str] = Field(default_factory=list)
    hooks: list[str] = Field(default_factory=list)
    mcps: list[str] = Field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.skills) + len(self.agents) + len(self.hooks) + len(self.mcps)

    @property
    def summary(self) -> str:
        """Human-readable summary."""
        parts = []
        if self.skills:
            parts.append(f"{len(self.skills)} skill(s)")
        if self.agents:
            parts.append(f"{len(self.agents)} agent(s)")
        if self.hooks:
            parts.append(f"{len(self.hooks)} hook(s)")
        if self.mcps:
            parts.append(f"{len(self.mcps)} mcp(s)")
        return ", ".join(parts) if parts else "empty"


class Package(BaseModel):
    """An installable package of extensions."""

    name: str
    description: str = ""
    version: str = "0.0.0"
    path: Path
    extensions: Extensions = Field(default_factory=Extensions)

    model_config = {"frozen": True}


class Source(BaseModel):
    """A source of packages (marketplace, git repo)."""

    name: str
    url: str
    default: bool = False
    ref: str | None = None

    model_config = {"frozen": True}

    @property
    def is_pinned(self) -> bool:
        return self.ref is not None


class Installation(BaseModel):
    """Record of an installed package."""

    package: Package
    source: Source
    installed_at: datetime = Field(default_factory=datetime.now)
    commit: str = ""
    target: str = "claude-code"

    @property
    def id(self) -> str:
        return f"{self.source.name}/{self.package.name}"
