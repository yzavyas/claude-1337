"""MCP headless runner - test MCP server tool calls.

MCP servers expose tools that Claude can call.
We test:
- Server connected
- Tool was called
- Response was valid
"""

from pathlib import Path
from typing import Any

from ...core.models import TestCase
from .base import HeadlessRunnerBase
from .observer import Observation


class MCPHeadlessRunner(HeadlessRunnerBase):
    """Test MCP tool calls using Claude Code headless mode.

    MCP tools are called when Claude needs external capabilities.
    Test prompts should trigger specific MCP tool usage.
    """

    def __init__(
        self,
        working_dir: Path | None = None,
        timeout: int = 60,
        target_server: str | None = None,
        target_tool: str | None = None,
    ):
        super().__init__(working_dir, timeout)
        self.target_server = target_server
        self.target_tool = target_tool

    @property
    def extension_type(self) -> str:
        return "mcp"

    def build_command(self, test_case: TestCase, **kwargs) -> list[str]:
        """Build claude command to trigger MCP tool usage.

        The prompt should require external data/actions that MCP provides.
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
        """Check if target MCP tool was called.

        MCP tools are identified by their naming pattern:
        - mcp_servername_toolname
        - servername::toolname
        """
        target_server = kwargs.get("target_server", self.target_server)
        target_tool = kwargs.get("target_tool", self.target_tool)

        tools_called = [
            obs.extension_name
            for obs in observations
            if obs.triggered
        ]

        # Check if target tool was called
        passed = False
        if target_tool:
            passed = any(target_tool in t for t in tools_called if t)
        elif target_server:
            passed = any(target_server in t for t in tools_called if t)
        else:
            passed = len(tools_called) > 0

        return passed, {
            "target_server": target_server,
            "target_tool": target_tool,
            "tools_called": tools_called,
            "observation_count": len(observations),
        }
