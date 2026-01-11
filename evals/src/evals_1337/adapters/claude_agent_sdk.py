"""Claude Agent SDK adapter for runtime port.

Uses the Claude Agent SDK for full Claude Code experience with:
- Built-in tools (Read, Edit, Bash, Glob, Grep, etc.)
- Hooks for behavior observation
- Sessions for context persistence
- Skills and CLAUDE.md support

This is the recommended adapter for production evals.
"""

import time
from typing import Any

from ..ports.runtime import EvalConfig, RuntimePort, RuntimeResult


class ClaudeAgentSDKAdapter(RuntimePort):
    """Claude Agent SDK adapter for realistic, full-featured evals.

    Benefits over raw Anthropic API:
    - Same infrastructure that powers Claude Code
    - Built-in tool execution (no need to implement tools)
    - Proper tool loop handling
    - Session management for multi-turn context

    For baseline comparison, we use custom system_prompt to control
    exactly what context Claude receives.
    """

    def __init__(
        self,
        working_dir: str | None = None,
        permission_mode: str = "bypassPermissions",
    ):
        """Initialize the adapter.

        Args:
            working_dir: Working directory for file operations. Defaults to cwd.
            permission_mode: How to handle tool permissions.
                - "bypassPermissions": Skip all permission prompts (for automated evals)
                - "acceptEdits": Auto-accept file edits
                - "default": Normal interactive mode
        """
        self._working_dir = working_dir
        self._permission_mode = permission_mode

    async def run(self, prompt: str, config: EvalConfig) -> RuntimeResult:
        """Run prompt with configured context using Claude Agent SDK.

        The system prompt is built from config layers, giving full control
        over what context Claude receives for baseline comparison.
        """
        # Import here to allow graceful degradation if SDK not installed
        try:
            from claude_agent_sdk import query, ClaudeAgentOptions
        except ImportError:
            raise ImportError(
                "claude-agent-sdk not installed. "
                "Install with: pip install claude-agent-sdk"
            )

        start = time.monotonic()

        # Build system prompt from config layers
        system_prompt = config.build_system_prompt()

        # Configure options
        options_kwargs: dict[str, Any] = {
            "permission_mode": self._permission_mode,
        }

        # Set system prompt - use custom string for full control
        if system_prompt:
            options_kwargs["system_prompt"] = system_prompt
        # If no custom prompt, use empty (SDK default) for pure baseline

        # For skill activation testing, we need to provide a mock Skill tool
        # The SDK doesn't have a built-in Skill tool, so we use allowed_tools
        # to control what's available and observe behavior
        if config.available_skills:
            # Use minimal tools for activation testing
            # The Skill tool would need to be implemented as a custom tool
            options_kwargs["allowed_tools"] = []  # No tools for pure activation test

        if self._working_dir:
            options_kwargs["cwd"] = self._working_dir

        options = ClaudeAgentOptions(**options_kwargs)

        # Collect results
        text_parts = []
        tool_calls = []
        skills_activated = []
        tokens_used = 0

        async for message in query(prompt=prompt, options=options):
            # Priority 1: Check for final result (most reliable)
            if hasattr(message, 'result') and message.result:
                text_parts.append(str(message.result))
                # Token usage if available on result message
                if hasattr(message, 'usage'):
                    usage = message.usage
                    tokens_used = getattr(usage, 'input_tokens', 0) + getattr(usage, 'output_tokens', 0)
                continue

            # Priority 2: Check message type for assistant content
            msg_type = getattr(message, 'type', None)

            if msg_type == 'assistant':
                # Content is directly on message, not message.message
                content = getattr(message, 'content', None)
                if content:
                    for block in content:
                        if hasattr(block, 'text'):
                            text_parts.append(block.text)
                        elif hasattr(block, 'type') and block.type == 'tool_use':
                            tool_call = {
                                "name": getattr(block, 'name', 'unknown'),
                                "input": getattr(block, 'input', {}),
                            }
                            tool_calls.append(tool_call)

                            # Track Skill tool calls specifically
                            if getattr(block, 'name', '') == 'Skill':
                                skill_input = getattr(block, 'input', {})
                                if isinstance(skill_input, dict) and 'skill' in skill_input:
                                    skills_activated.append(skill_input['skill'])

            # Priority 3: Check for text attribute directly on message
            elif hasattr(message, 'text') and message.text:
                text_parts.append(str(message.text))

        duration_ms = int((time.monotonic() - start) * 1000)

        return RuntimeResult(
            response="\n".join(text_parts),
            tool_calls=tool_calls,
            skills_activated=skills_activated,
            tokens_used=tokens_used,
            duration_ms=duration_ms,
        )

    async def health_check(self) -> bool:
        """Check if SDK is available and working."""
        try:
            from claude_agent_sdk import query, ClaudeAgentOptions

            # Quick test with minimal prompt
            async for message in query(
                prompt="Say 'ok'",
                options=ClaudeAgentOptions(
                    permission_mode="bypassPermissions",
                    system_prompt="Respond with just 'ok'",
                    max_turns=1,
                )
            ):
                if hasattr(message, 'type') and message.type == 'result':
                    return True

            return True
        except Exception:
            return False


class ClaudeAgentSDKWithSkillToolAdapter(RuntimePort):
    """Agent SDK adapter with custom Skill tool for activation testing.

    This adapter adds a mock Skill tool that Claude can call,
    allowing us to test skill activation behavior.
    """

    def __init__(
        self,
        working_dir: str | None = None,
        permission_mode: str = "bypassPermissions",
    ):
        self._working_dir = working_dir
        self._permission_mode = permission_mode
        self._skill_calls: list[str] = []

    async def run(self, prompt: str, config: EvalConfig) -> RuntimeResult:
        """Run prompt with custom Skill tool."""
        try:
            from claude_agent_sdk import query, ClaudeAgentOptions
        except ImportError:
            raise ImportError(
                "claude-agent-sdk not installed. "
                "Install with: pip install claude-agent-sdk"
            )

        start = time.monotonic()
        self._skill_calls = []

        # Build system prompt from config
        system_prompt = config.build_system_prompt()

        # Define custom Skill tool handler
        async def skill_tool_handler(input_data: dict, tool_use_id: str, context: Any) -> dict:
            """Handle Skill tool calls."""
            skill_name = input_data.get('skill', 'unknown')
            self._skill_calls.append(skill_name)
            return {"result": f"Skill '{skill_name}' activated successfully."}

        # Configure options with custom tool
        options_kwargs: dict[str, Any] = {
            "permission_mode": self._permission_mode,
            "allowed_tools": ["Skill"],  # Only allow our custom Skill tool
            "custom_tools": {
                "Skill": {
                    "description": "Activate a skill to load specialized knowledge",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "skill": {
                                "type": "string",
                                "description": "The skill name to activate"
                            }
                        },
                        "required": ["skill"]
                    },
                    "handler": skill_tool_handler,
                }
            }
        }

        if system_prompt:
            options_kwargs["system_prompt"] = system_prompt

        if self._working_dir:
            options_kwargs["cwd"] = self._working_dir

        options = ClaudeAgentOptions(**options_kwargs)

        # Collect results
        text_parts = []
        tool_calls = []
        tokens_used = 0

        async for message in query(prompt=prompt, options=options):
            # Priority 1: Check for final result (most reliable)
            if hasattr(message, 'result') and message.result:
                text_parts.append(str(message.result))
                if hasattr(message, 'usage'):
                    usage = message.usage
                    tokens_used = getattr(usage, 'input_tokens', 0) + getattr(usage, 'output_tokens', 0)
                continue

            # Priority 2: Check message type for assistant content
            msg_type = getattr(message, 'type', None)

            if msg_type == 'assistant':
                # Content is directly on message, not message.message
                content = getattr(message, 'content', None)
                if content:
                    for block in content:
                        if hasattr(block, 'text'):
                            text_parts.append(block.text)
                        elif hasattr(block, 'type') and block.type == 'tool_use':
                            tool_calls.append({
                                "name": getattr(block, 'name', 'unknown'),
                                "input": getattr(block, 'input', {}),
                            })

            # Priority 3: Check for text attribute directly on message
            elif hasattr(message, 'text') and message.text:
                text_parts.append(str(message.text))

        duration_ms = int((time.monotonic() - start) * 1000)

        return RuntimeResult(
            response="\n".join(text_parts),
            tool_calls=tool_calls,
            skills_activated=self._skill_calls,
            tokens_used=tokens_used,
            duration_ms=duration_ms,
        )

    async def health_check(self) -> bool:
        """Check if SDK is available."""
        try:
            from claude_agent_sdk import query
            return True
        except ImportError:
            return False
