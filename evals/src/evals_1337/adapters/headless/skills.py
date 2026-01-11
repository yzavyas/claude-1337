"""Skill headless runner - test skill activation with real Claude Code.

Uses `claude -p` to run prompts and observes actual Skill() tool calls.
"""

from pathlib import Path
from typing import Any

from ...core.models import TestCase
from .base import HeadlessRunnerBase
from .observer import Observation


class SkillHeadlessRunner(HeadlessRunnerBase):
    """Test skill activation using Claude Code headless mode."""

    def __init__(
        self,
        working_dir: Path | None = None,
        timeout: int = 60,
        target_skill: str | None = None,
    ):
        super().__init__(working_dir, timeout)
        self.target_skill = target_skill

    @property
    def extension_type(self) -> str:
        return "skills"

    def build_command(self, test_case: TestCase, **kwargs) -> list[str]:
        """Build claude command for skill activation test.

        Uses --output-format stream-json to get parseable output.
        """
        return [
            "claude",
            "-p", test_case.prompt,
            "--output-format", "stream-json",
        ]

    def interpret_observations(
        self,
        observations: list[Observation],
        test_case: TestCase,
        **kwargs,
    ) -> tuple[bool, dict[str, Any]]:
        """Check if target skill was activated.

        Returns (passed, details) where passed is True if target skill
        was in the activated skills.
        """
        target = kwargs.get("target_skill", self.target_skill)
        skills_activated = [
            obs.extension_name
            for obs in observations
            if obs.extension_name
        ]

        passed = target in skills_activated if target else len(skills_activated) > 0

        return passed, {
            "target_skill": target,
            "skills_activated": skills_activated,
            "observation_count": len(observations),
        }
