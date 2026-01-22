"""LLM Port - Interface for language model interactions.

Why a Protocol?
--------------
The domain defines WHAT it needs (generate text), not HOW.
Adapters provide the HOW (Claude SDK, OpenAI, mock for tests).

To add a new LLM:
1. Create adapters/driven/your_llm.py
2. Implement LLMPort protocol
3. Register in container.py
"""

from typing import Protocol, AsyncIterator, Any

from pydantic import BaseModel, ConfigDict, Field, computed_field


class LLMConfig(BaseModel):
    """Configuration for LLM calls.

    Value object - immutable after creation.
    """
    model_config = ConfigDict(frozen=True)

    model: str = "sonnet"
    max_tokens: int = 8192
    temperature: float = Field(default=0.0, ge=0.0, le=2.0)

    # System prompt (condition framing for Claude agents)
    system_prompt: str = ""

    # Tool permissions (for Claude SDK)
    allowed_tools: tuple[str, ...] = ("Read", "Write", "Bash", "Glob", "Grep")
    permission_mode: str = "acceptEdits"


class LLMResponse(BaseModel):
    """Response from an LLM call.

    Value object - immutable after creation.
    """
    model_config = ConfigDict(frozen=True)

    content: str
    tokens_input: int = Field(ge=0)
    tokens_output: int = Field(ge=0)
    duration_ms: int = Field(ge=0)

    # Optional metadata
    model: str = ""
    finish_reason: str = ""
    raw_response: Any = None

    @computed_field
    @property
    def total_tokens(self) -> int:
        return self.tokens_input + self.tokens_output


class LLMPort(Protocol):
    """Port for language model interactions.

    The domain needs to:
    1. Send prompts to an LLM
    2. Get text responses back
    3. Track token usage

    Implementations:
    - ClaudeSDKAdapter: Uses Claude Agent SDK for tool-using agent
    - MockLLMAdapter: For testing without real API calls
    """

    async def generate(
        self,
        prompt: str,
        config: LLMConfig,
    ) -> LLMResponse:
        """Generate a response from the LLM.

        Args:
            prompt: The input prompt
            config: Configuration for this call

        Returns:
            LLMResponse with content and usage stats
        """
        ...

    async def generate_with_iteration(
        self,
        prompt: str,
        config: LLMConfig,
        max_iterations: int = 1,
        review_prompt: str = "",
    ) -> tuple[LLMResponse, int]:
        """Generate with optional self-review iterations.

        Args:
            prompt: The initial prompt
            config: Configuration for this call
            max_iterations: Maximum number of iterations
            review_prompt: Prompt for self-review (if iterating)

        Returns:
            Tuple of (final response, iterations used)
        """
        ...

    async def stream_generate(
        self,
        prompt: str,
        config: LLMConfig,
    ) -> AsyncIterator[str]:
        """Stream response tokens as they're generated.

        Yields text chunks as they arrive.
        """
        ...
