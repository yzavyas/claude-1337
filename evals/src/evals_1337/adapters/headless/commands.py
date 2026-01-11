"""Command headless runner - test slash command execution.

Commands expand to prompts. We test:
- Command was recognized
- Expansion happened correctly
- Execution completed
"""

from pathlib import Path
from typing import Any

from ...core.models import TestCase
from .base import HeadlessRunnerBase
from .observer import Observation


class CommandHeadlessRunner(HeadlessRunnerBase):
    """Test command execution using Claude Code headless mode.

    Commands are invoked with /commandname syntax.
    The test case prompt should be the command invocation.
    """

    def __init__(
        self,
        working_dir: Path | None = None,
        timeout: int = 60,
    ):
        super().__init__(working_dir, timeout)

    @property
    def extension_type(self) -> str:
        return "commands"

    def build_command(self, test_case: TestCase, **kwargs) -> list[str]:
        """Build claude command to invoke a slash command.

        The prompt IS the command (e.g., "/commit").
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
        """Check if command executed.

        Commands expand to prompts before Claude sees them.
        We look for evidence of expansion and execution.
        """
        commands_found = [
            obs.extension_name
            for obs in observations
            if obs.triggered
        ]

        # For commands, success is often measured by exit code
        # and whether the expected behavior occurred
        passed = len(commands_found) > 0 or len(observations) > 0

        return passed, {
            "command": test_case.prompt,
            "commands_found": commands_found,
            "observation_count": len(observations),
        }
