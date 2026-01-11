"""Headless observer - parse stream-json output from claude -p.

Stream-json format emits one JSON object per line:
{"type": "assistant", "message": {...}}
{"type": "tool_use", "name": "Read", "input": {...}}
{"type": "tool_result", ...}
{"type": "result", "cost": {...}, "duration_ms": ...}

We parse these to extract observations about extension behavior.
"""

import json
from typing import Any
from dataclasses import dataclass

from ...ports.observer import Observation


@dataclass
class StreamMessage:
    """A single message from stream-json output."""

    type: str
    data: dict[str, Any]
    raw: str


class HeadlessObserver:
    """Observer for Claude Code headless stream-json output."""

    @property
    def runtime(self) -> str:
        return "headless"

    def parse_stream(self, output: str) -> list[StreamMessage]:
        """Parse stream-json output into messages."""
        messages = []
        for line in output.strip().split("\n"):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                msg_type = data.get("type", "unknown")
                messages.append(StreamMessage(type=msg_type, data=data, raw=line))
            except json.JSONDecodeError:
                continue
        return messages

    def observe_skills(self, output: str) -> list[Observation]:
        """Extract skill activation observations.

        Look for tool_use with name="Skill".
        """
        messages = self.parse_stream(output)
        observations = []

        for msg in messages:
            if msg.type == "tool_use" and msg.data.get("name") == "Skill":
                skill_input = msg.data.get("input", {})
                skill_name = skill_input.get("skill") or skill_input.get("name")

                observations.append(Observation(
                    extension_type="skills",
                    extension_name=skill_name,
                    triggered=True,
                    success=None,  # Skill activation doesn't have success/fail
                    duration_ms=0,  # Would need to match with tool_result
                    details={"input": skill_input},
                    raw_output=msg.raw,
                ))

        return observations

    def observe_hooks(self, output: str) -> list[Observation]:
        """Extract hook execution observations.

        Look for hook-related messages in the stream.
        Hook output format TBD - need to check actual Claude Code output.
        """
        messages = self.parse_stream(output)
        observations = []

        for msg in messages:
            # Hooks might appear as system messages or special types
            if msg.type == "system" and "hook" in msg.data.get("message", "").lower():
                observations.append(Observation(
                    extension_type="hooks",
                    extension_name=None,  # Parse from message
                    triggered=True,
                    success=True,  # Parse exit code
                    duration_ms=0,
                    details=msg.data,
                    raw_output=msg.raw,
                ))

        return observations

    def observe_agents(self, output: str) -> list[Observation]:
        """Extract agent/Task observations.

        Look for tool_use with name="Task".
        """
        messages = self.parse_stream(output)
        observations = []

        for msg in messages:
            if msg.type == "tool_use" and msg.data.get("name") == "Task":
                task_input = msg.data.get("input", {})
                agent_type = task_input.get("subagent_type")

                observations.append(Observation(
                    extension_type="agents",
                    extension_name=agent_type,
                    triggered=True,
                    success=None,  # Need to match with tool_result
                    duration_ms=0,
                    details={"input": task_input},
                    raw_output=msg.raw,
                ))

        return observations

    def observe_commands(self, output: str) -> list[Observation]:
        """Extract command invocation observations.

        Commands expand to prompts - look for command expansion markers.
        """
        messages = self.parse_stream(output)
        observations = []

        # Commands are handled differently - they expand before Claude sees them
        # We might see them in the initial prompt or as a special message type
        for msg in messages:
            if msg.type == "command" or "command" in str(msg.data).lower():
                observations.append(Observation(
                    extension_type="commands",
                    extension_name=msg.data.get("name"),
                    triggered=True,
                    success=True,
                    duration_ms=0,
                    details=msg.data,
                    raw_output=msg.raw,
                ))

        return observations

    def observe_mcp(self, output: str) -> list[Observation]:
        """Extract MCP tool call observations.

        Look for tool_use where the tool comes from an MCP server.
        MCP tools are prefixed with server name: "mcp_servername_toolname"
        """
        messages = self.parse_stream(output)
        observations = []

        for msg in messages:
            if msg.type == "tool_use":
                tool_name = msg.data.get("name", "")
                # MCP tools have a specific naming pattern
                if tool_name.startswith("mcp_") or "::" in tool_name:
                    observations.append(Observation(
                        extension_type="mcp",
                        extension_name=tool_name,
                        triggered=True,
                        success=None,
                        duration_ms=0,
                        details={"input": msg.data.get("input", {})},
                        raw_output=msg.raw,
                    ))

        return observations

    def get_result_metadata(self, output: str) -> dict[str, Any]:
        """Extract final result metadata (cost, duration, etc.)."""
        messages = self.parse_stream(output)

        for msg in reversed(messages):
            if msg.type == "result":
                return msg.data

        return {}
