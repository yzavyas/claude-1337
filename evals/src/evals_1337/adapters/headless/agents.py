"""Agent headless runner - test agent execution with real Claude Code.

Agents are spawned via Task tool. We observe:
- Agent was invoked
- Agent completed successfully
- Tools used by agent
- Output produced
"""

from pathlib import Path
from typing import Any

from ...core.models import TestCase
from .base import HeadlessRunnerBase
from .observer import Observation


class AgentHeadlessRunner(HeadlessRunnerBase):
    """Test agent execution using Claude Code headless mode.

    Agents are invoked when Claude uses the Task tool.
    Test prompts should be designed to trigger agent usage.
    """

    def __init__(
        self,
        working_dir: Path | None = None,
        timeout: int = 120,  # Agents take longer
        target_agent: str | None = None,
    ):
        super().__init__(working_dir, timeout)
        self.target_agent = target_agent

    @property
    def extension_type(self) -> str:
        return "agents"

    def build_command(self, test_case: TestCase, **kwargs) -> list[str]:
        """Build claude command to trigger agent usage.

        The prompt should be something that requires agent delegation.
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
        """Check if target agent was invoked and completed.

        For agents, we look for:
        - Task tool was called with the right subagent_type
        - Agent completed (need to match with tool_result)
        """
        target = kwargs.get("target_agent", self.target_agent)

        agents_invoked = [
            obs.extension_name
            for obs in observations
            if obs.triggered
        ]

        # Check if target agent was invoked
        if target:
            passed = target in agents_invoked
        else:
            passed = len(agents_invoked) > 0

        return passed, {
            "target_agent": target,
            "agents_invoked": agents_invoked,
            "observation_count": len(observations),
        }
