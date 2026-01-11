"""Anthropic API adapter for runtime port.

Direct API calls with explicit context control.
No CLI plugins, no installed hooks - just what you configure.
"""

import time
from typing import Any

import anthropic

from ..ports.runtime import EvalConfig, RuntimePort, RuntimeResult


# Mock Skill tool for activation testing
SKILL_TOOL = {
    "name": "Skill",
    "description": "Activate a skill to load specialized knowledge",
    "input_schema": {
        "type": "object",
        "properties": {
            "skill": {"type": "string", "description": "The skill name"}
        },
        "required": ["skill"],
    },
}


class AnthropicAdapter(RuntimePort):
    """Anthropic API adapter for direct, controllable evals.

    Benefits over CLI:
    - Explicit context control (no installed plugins interfering)
    - Deterministic system prompts
    - Layer-by-layer configuration for baseline comparison
    """

    def __init__(self, api_key: str | None = None):
        """Initialize with optional API key.

        If not provided, uses ANTHROPIC_API_KEY environment variable.
        """
        self._client = anthropic.AsyncAnthropic(api_key=api_key)

    async def run(self, prompt: str, config: EvalConfig) -> RuntimeResult:
        """Run prompt with configured context.

        The system prompt is built from config layers:
        1. Base system prompt
        2. CLAUDE.md content
        3. Skill content
        4. Reference content
        5. Available skills XML
        """
        start = time.monotonic()

        system_prompt = config.build_system_prompt()

        # Build tools list - include Skill tool if testing activation
        tools = []
        if config.available_skills:
            tools.append(SKILL_TOOL)

        # Make API call
        kwargs: dict[str, Any] = {
            "model": config.model,
            "max_tokens": config.max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        if tools:
            kwargs["tools"] = tools

        response = await self._client.messages.create(**kwargs)

        # Extract results
        text_parts = []
        tool_calls = []
        skills_activated = []

        for block in response.content:
            if block.type == "text":
                text_parts.append(block.text)
            elif block.type == "tool_use":
                tool_call = {
                    "name": block.name,
                    "input": block.input,
                }
                tool_calls.append(tool_call)

                # Track skill activations specifically
                if block.name == "Skill":
                    skill_input = block.input
                    if isinstance(skill_input, dict) and "skill" in skill_input:
                        skills_activated.append(skill_input["skill"])

        duration_ms = int((time.monotonic() - start) * 1000)

        # Calculate tokens
        tokens_used = response.usage.input_tokens + response.usage.output_tokens

        return RuntimeResult(
            response="\n".join(text_parts),
            tool_calls=tool_calls,
            skills_activated=skills_activated,
            tokens_used=tokens_used,
            duration_ms=duration_ms,
            raw_response=response,
        )

    async def health_check(self) -> bool:
        """Check API connectivity."""
        try:
            # Simple ping with minimal tokens
            await self._client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1,
                messages=[{"role": "user", "content": "ping"}],
            )
            return True
        except Exception:
            return False


class MockAdapter(RuntimePort):
    """Mock adapter for testing without API calls."""

    def __init__(self, responses: list[RuntimeResult] | None = None):
        """Initialize with optional canned responses.

        If responses provided, they're returned in order (cycling).
        If not provided, returns empty responses.
        """
        self._responses = responses or []
        self._call_index = 0
        self._calls: list[tuple[str, EvalConfig]] = []

    async def run(self, prompt: str, config: EvalConfig) -> RuntimeResult:
        """Return mock response, recording the call."""
        self._calls.append((prompt, config))

        if self._responses:
            result = self._responses[self._call_index % len(self._responses)]
            self._call_index += 1
            return result

        return RuntimeResult(response="Mock response", duration_ms=1)

    async def health_check(self) -> bool:
        """Always healthy."""
        return True

    @property
    def calls(self) -> list[tuple[str, EvalConfig]]:
        """Get recorded calls for assertions."""
        return self._calls
