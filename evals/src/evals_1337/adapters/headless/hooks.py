"""Hook headless runner - test hook execution with real Claude Code.

Hooks trigger on lifecycle events. We trigger events and observe hook execution.
"""

from pathlib import Path
from typing import Any

from ...core.models import TestCase
from .base import HeadlessRunnerBase
from .observer import Observation


class HookHeadlessRunner(HeadlessRunnerBase):
    """Test hook execution using Claude Code headless mode.

    Hooks are event-triggered. To test:
    1. SessionStart hooks: Just start a session
    2. PreToolUse hooks: Send prompt that triggers tool use
    3. PostToolUse hooks: Same as PreToolUse
    4. Stop hooks: Complete a task
    """

    def __init__(
        self,
        working_dir: Path | None = None,
        timeout: int = 60,
        target_hook: str | None = None,
    ):
        super().__init__(working_dir, timeout)
        self.target_hook = target_hook

    @property
    def extension_type(self) -> str:
        return "hooks"

    def build_command(self, test_case: TestCase, **kwargs) -> list[str]:
        """Build claude command to trigger hooks.

        The prompt should be designed to trigger the target hook event.
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
        """Check if target hook executed.

        For hooks, we look for:
        - Hook triggered (the event happened)
        - Hook succeeded (exit code 0 or 1)
        - Hook blocked (exit code 2, for blocking hooks)
        """
        target = kwargs.get("target_hook", self.target_hook)

        hooks_fired = [
            obs.extension_name
            for obs in observations
            if obs.triggered
        ]

        # For now, passed = any hook fired for this event type
        # More specific matching can be added based on hook names
        passed = len(hooks_fired) > 0

        # Check for blocked hooks
        blocked = any(
            obs.details.get("exit_code") == 2
            for obs in observations
        )

        return passed, {
            "target_hook": target,
            "hooks_fired": hooks_fired,
            "blocked": blocked,
            "observation_count": len(observations),
        }
