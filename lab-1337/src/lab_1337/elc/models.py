"""Pydantic models for Enhancement Lifecycle artifacts."""

import re
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, computed_field


class EnhancementStatus(str, Enum):
    """Valid states in the enhancement lifecycle."""

    DRAFT = "draft"
    DISCUSSION = "discussion"
    FCP = "fcp"  # Final Comment Period
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    POSTPONED = "postponed"
    IMPLEMENTED = "implemented"


class LEP(BaseModel):
    """Lab Enhancement Proposal."""

    number: str = Field(..., pattern=r"^\d{3}$")
    title: str
    status: EnhancementStatus = EnhancementStatus.DRAFT
    created: date = Field(default_factory=date.today)
    authors: list[str] = Field(default_factory=list)
    tracking: Optional[str] = None
    path: Optional[Path] = None

    @computed_field
    @property
    def slug(self) -> str:
        """Kebab-case slug from title."""
        slug = self.title.lower()
        slug = re.sub(r"[^a-z0-9\s-]", "", slug)
        slug = re.sub(r"[\s_]+", "-", slug)
        slug = re.sub(r"-+", "-", slug)
        return slug[:40].strip("-")

    @computed_field
    @property
    def filename(self) -> str:
        """Standard filename for this LEP."""
        return f"lep-{self.number}-{self.slug}.md"

    @computed_field
    @property
    def experiment_dirname(self) -> str:
        """Standard experiment directory name."""
        return f"lep-{self.number}-{self.slug}"

    def has_imp(self, implementations_dir: Path) -> bool:
        """Check if an IMP exists for this LEP."""
        pattern = f"imp-{self.number}-*.md"
        return any(implementations_dir.glob(pattern))

    def has_experiment(self, experiments_dir: Path) -> bool:
        """Check if an experiment exists for this LEP."""
        return (experiments_dir / self.experiment_dirname).exists()


class IMP(BaseModel):
    """Implementation Plan."""

    number: str = Field(..., pattern=r"^\d{3}$")  # Matches LEP number
    title: str  # Inherited from LEP
    status: EnhancementStatus = EnhancementStatus.DRAFT
    created: date = Field(default_factory=date.today)
    authors: list[str] = Field(default_factory=list)
    lep_ref: str  # Reference to LEP number
    path: Optional[Path] = None

    @computed_field
    @property
    def slug(self) -> str:
        """Kebab-case slug from title."""
        slug = self.title.lower()
        slug = re.sub(r"[^a-z0-9\s-]", "", slug)
        slug = re.sub(r"[\s_]+", "-", slug)
        slug = re.sub(r"-+", "-", slug)
        return slug[:40].strip("-")

    @computed_field
    @property
    def filename(self) -> str:
        """Standard filename for this IMP."""
        return f"imp-{self.number}-{self.slug}.md"


# Status display helpers
STATUS_COLORS = {
    EnhancementStatus.DRAFT: "dim",
    EnhancementStatus.DISCUSSION: "cyan",
    EnhancementStatus.FCP: "yellow",
    EnhancementStatus.ACCEPTED: "green",
    EnhancementStatus.REJECTED: "red",
    EnhancementStatus.POSTPONED: "dim yellow",
    EnhancementStatus.IMPLEMENTED: "bold green",
}


def status_color(status: EnhancementStatus) -> str:
    """Get rich color for status."""
    return STATUS_COLORS.get(status, "white")
