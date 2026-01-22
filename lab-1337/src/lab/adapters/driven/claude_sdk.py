"""Claude SDK Adapter - LLM implementation using Claude Agent SDK.

This adapter wraps the Claude Agent SDK to implement our LLMPort interface.
It provides tool-using agent capabilities for experiments.
"""

import time
from pathlib import Path
from typing import AsyncIterator

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    TextBlock,
    ThinkingBlock,
    ToolUseBlock,
    ToolResultBlock,
)

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
        capture_trace: bool = False,
    ) -> LLMResponse | tuple[LLMResponse, list[dict]]:
        """Generate a response from Claude.

        Uses the Claude Code SDK to run an agentic session.

        Args:
            prompt: The user prompt
            config: LLM configuration
            capture_trace: If True, returns (response, trace) tuple

        Returns:
            LLMResponse, or (LLMResponse, trace) if capture_trace=True
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
        conversation_trace: list[dict] = []  # Capture full trace
        result_message: ResultMessage | None = None  # Capture for token counts

        async for message in query(
            prompt=prompt,
            options=options,
        ):
            if isinstance(message, AssistantMessage):
                # Track content from assistant messages
                for block in message.content:
                    if isinstance(block, TextBlock):
                        content_parts.append(block.text)

                # Capture message for trace
                if capture_trace:
                    conversation_trace.append({
                        "role": "assistant",
                        "content": [self._serialize_block(b) for b in message.content],
                        "timestamp": time.time(),
                    })

            elif isinstance(message, ResultMessage):
                # Always capture ResultMessage for token counts
                result_message = message
                if capture_trace:
                    conversation_trace.append({
                        "role": "result",
                        "usage": message.usage if message.usage else {},
                        "timestamp": time.time(),
                    })

        duration_ms = int((time.time() - start_time) * 1000)

        # Extract actual token counts from ResultMessage.usage (SDK pattern)
        tokens_input = 0
        tokens_output = 0
        if result_message and result_message.usage:
            tokens_input = result_message.usage.get("input_tokens", 0)
            tokens_output = result_message.usage.get("output_tokens", 0)

        content = "\n".join(content_parts)

        response = LLMResponse(
            content=content,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            duration_ms=duration_ms,
            model=config.model,
            finish_reason="stop",
        )

        if capture_trace:
            return response, conversation_trace
        return response

    def _serialize_block(self, block) -> dict:
        """Serialize a content block for trace storage.

        Handles all SDK content block types for proper trace fidelity.
        """
        if isinstance(block, TextBlock):
            return {"type": "text", "text": block.text}
        elif isinstance(block, ThinkingBlock):
            return {
                "type": "thinking",
                "thinking": block.thinking,
                "signature": getattr(block, "signature", None),
            }
        elif isinstance(block, ToolUseBlock):
            return {
                "type": "tool_use",
                "id": block.id,
                "name": block.name,
                "input": block.input,
            }
        elif isinstance(block, ToolResultBlock):
            return {
                "type": "tool_result",
                "tool_use_id": block.tool_use_id,
                "content": block.content,
                "is_error": getattr(block, "is_error", False),
            }
        # Fallback for unknown types
        return {"type": type(block).__name__, "data": str(block)}

    async def generate_with_iteration(
        self,
        prompt: str,
        config: LLMConfig,
        max_iterations: int = 1,
        review_prompt: str = "",
        capture_trace: bool = False,
    ) -> tuple[LLMResponse, int] | tuple[LLMResponse, int, list[dict]]:
        """Generate with self-review iterations.

        For now, implements a simple loop where we ask the agent
        to review its own work between iterations.

        Args:
            prompt: The user prompt
            config: LLM configuration
            max_iterations: Maximum iterations
            review_prompt: Prompt for self-review
            capture_trace: If True, returns (response, iterations, trace) tuple

        Returns:
            (LLMResponse, iterations), or (LLMResponse, iterations, trace) if capture_trace=True
        """
        full_trace: list[dict] = []

        if capture_trace:
            result = await self.generate(prompt, config, capture_trace=True)
            current_response, trace = result
            full_trace.extend(trace)
        else:
            current_response = await self.generate(prompt, config)

        iterations_used = 1

        if max_iterations <= 1 or not review_prompt:
            if capture_trace:
                return current_response, iterations_used, full_trace
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
            if capture_trace:
                result = await self.generate(full_review_prompt, config, capture_trace=True)
                review_response, trace = result
                full_trace.extend(trace)
            else:
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

        if capture_trace:
            return current_response, iterations_used, full_trace
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
        """Map our model names to Claude SDK model names.

        Model ID formats vary by generation:
        - Claude 3.5: claude-3-5-{model}-{date}
        - Claude 4: claude-{model}-4-{date}
        """
        model_map = {
            "sonnet": "claude-sonnet-4-20250514",
            "opus": "claude-opus-4-20250514",
            "haiku": "claude-3-5-haiku-20241022",  # Claude 3.5 Haiku uses different format
        }
        return model_map.get(model, model)
