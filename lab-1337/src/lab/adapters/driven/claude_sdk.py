"""Claude SDK Adapter - LLM implementation using Claude Agent SDK.

This adapter wraps the Claude Agent SDK to implement our LLMPort interface.
It provides tool-using agent capabilities for experiments.
"""

import time
from pathlib import Path
from typing import AsyncIterator

from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage, TextBlock

from lab.ports.driven.llm import LLMPort, LLMConfig, LLMResponse


class ClaudeSDKAdapter:
    """LLM adapter using Claude Agent SDK.

    Implements the LLMPort protocol for experiments.
    Uses the Claude Code SDK for tool-using agent capabilities.
    """

    def __init__(self, working_dir: Path | None = None):
        """Initialize the adapter.

        Args:
            working_dir: Directory where the agent will execute.
                        Defaults to current directory.
        """
        self.working_dir = working_dir or Path.cwd()

    async def generate(
        self,
        prompt: str,
        config: LLMConfig,
    ) -> LLMResponse:
        """Generate a response from Claude.

        Uses the Claude Code SDK to run an agentic session.
        """
        start_time = time.time()

        # Build options from config
        options = ClaudeAgentOptions(
            model=self._map_model(config.model),
            max_turns=50,  # Reasonable default for experiments
            permission_mode=config.permission_mode,
            allowed_tools=list(config.allowed_tools),
            system_prompt=config.system_prompt if config.system_prompt else None,
            cwd=config.cwd if config.cwd else None,
        )

        # Collect results from the streaming query
        content_parts: list[str] = []
        tokens_input = 0
        tokens_output = 0

        async for message in query(
            prompt=prompt,
            options=options,
        ):
            if isinstance(message, AssistantMessage):
                # Track content from assistant messages
                for block in message.content:
                    if isinstance(block, TextBlock):
                        content_parts.append(block.text)

            elif isinstance(message, ResultMessage):
                # ResultMessage contains the final result
                # We track these for debugging but don't include in content
                pass

        duration_ms = int((time.time() - start_time) * 1000)

        # Note: The SDK doesn't expose token counts directly
        # We'd need to extract from usage stats if available
        # For now, estimate based on content length as placeholder
        content = "\n".join(content_parts)
        tokens_output = len(content) // 4  # Rough estimate

        return LLMResponse(
            content=content,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            duration_ms=duration_ms,
            model=config.model,
            finish_reason="stop",
        )

    async def generate_with_iteration(
        self,
        prompt: str,
        config: LLMConfig,
        max_iterations: int = 1,
        review_prompt: str = "",
    ) -> tuple[LLMResponse, int]:
        """Generate with self-review iterations.

        For now, implements a simple loop where we ask the agent
        to review its own work between iterations.
        """
        current_response = await self.generate(prompt, config)
        iterations_used = 1

        if max_iterations <= 1 or not review_prompt:
            return current_response, iterations_used

        # Iterate with self-review
        for _ in range(max_iterations - 1):
            # Build review prompt
            full_review_prompt = f"""
Previous solution:
{current_response.content}

{review_prompt}

If improvements are needed, provide the improved solution.
If the solution is correct, respond with "SOLUTION_VERIFIED".
"""
            review_response = await self.generate(full_review_prompt, config)
            iterations_used += 1

            # Check if verified
            if "SOLUTION_VERIFIED" in review_response.content:
                break

            # Use the improved response
            current_response = LLMResponse(
                content=review_response.content,
                tokens_input=current_response.tokens_input + review_response.tokens_input,
                tokens_output=current_response.tokens_output + review_response.tokens_output,
                duration_ms=current_response.duration_ms + review_response.duration_ms,
                model=config.model,
                finish_reason="stop",
            )

        return current_response, iterations_used

    async def stream_generate(
        self,
        prompt: str,
        config: LLMConfig,
    ) -> AsyncIterator[str]:
        """Stream response tokens as they're generated.

        Yields text chunks from assistant messages.
        """
        options = ClaudeAgentOptions(
            model=self._map_model(config.model),
            max_turns=50,
            permission_mode=config.permission_mode,
            allowed_tools=list(config.allowed_tools),
            system_prompt=config.system_prompt if config.system_prompt else None,
            cwd=config.cwd if config.cwd else None,
        )

        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        yield block.text

    def _map_model(self, model: str) -> str:
        """Map our model names to Claude SDK model names."""
        model_map = {
            "sonnet": "claude-sonnet-4-20250514",
            "opus": "claude-opus-4-20250514",
            "haiku": "claude-haiku-3-5-20241022",
        }
        return model_map.get(model, model)
