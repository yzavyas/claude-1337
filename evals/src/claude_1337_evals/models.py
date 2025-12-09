"""Pydantic models for skill activation testing."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class RunStatus(str, Enum):
    """Status of a single test run."""

    ACTIVATED = "activated"  # Skill() tool was called
    NOT_ACTIVATED = "not_activated"  # No Skill() call detected
    ERROR = "error"  # Test failed


class SkillReference(BaseModel):
    """A skill to test."""

    name: str = Field(description="Skill name as it appears in available_skills")
    plugin: str = Field(description="Plugin containing the skill")
    expected_triggers: list[str] = Field(
        description="Prompts that should trigger this skill"
    )


class ActivationRun(BaseModel):
    """Result of a single activation test run."""

    skill_name: str
    prompt: str
    status: RunStatus
    skill_called: bool = False
    tool_calls: list[str] = Field(default_factory=list)
    response_preview: str = ""
    duration_ms: int = 0
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class TestSuite(BaseModel):
    """Configuration for a test suite."""

    name: str
    description: str = ""
    skills: list[SkillReference]
    runs_per_prompt: int = Field(default=3, ge=1, le=10)


class ActivationReport(BaseModel):
    """Complete activation test report."""

    suite_name: str
    timestamp: datetime = Field(default_factory=datetime.now)
    runs: list[ActivationRun] = Field(default_factory=list)

    @property
    def total_runs(self) -> int:
        return len(self.runs)

    @property
    def activated_count(self) -> int:
        return sum(1 for r in self.runs if r.status == RunStatus.ACTIVATED)

    @property
    def activation_rate(self) -> float:
        if not self.runs:
            return 0.0
        return self.activated_count / self.total_runs

    def skill_stats(self) -> dict[str, dict]:
        """Get activation stats per skill."""
        stats: dict[str, dict] = {}
        for run in self.runs:
            if run.skill_name not in stats:
                stats[run.skill_name] = {"total": 0, "activated": 0}
            stats[run.skill_name]["total"] += 1
            if run.status == RunStatus.ACTIVATED:
                stats[run.skill_name]["activated"] += 1

        for skill, data in stats.items():
            data["rate"] = data["activated"] / data["total"] if data["total"] else 0

        return stats
