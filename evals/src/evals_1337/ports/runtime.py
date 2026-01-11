"""Runtime port: interface for executing prompts against LLMs.

This port abstracts the execution environment, allowing different backends:
- Anthropic API (direct, fast, controllable)
- Claude Agent SDK (full Claude Code experience)
- Mock (for testing)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class EvalConfig:
    """Configuration for a single eval run.

    Controls exactly what context Claude receives, enabling:
    - Baseline comparison (no context vs with context)
    - Layer-by-layer analysis (CLAUDE.md vs skill vs references)
    - Deterministic, reproducible evals
    """

    # Context layers (all optional, built in order)
    system_prompt: str | None = None
    """Base system prompt. Applied first if present."""

    claude_md_path: Path | None = None
    """Path to project CLAUDE.md. Loaded as project context."""

    skill_paths: list[Path] = field(default_factory=list)
    """Paths to SKILL.md files to load into context."""

    reference_paths: list[Path] = field(default_factory=list)
    """Paths to reference docs to load into context."""

    # Available skills for activation testing
    available_skills: list[dict[str, str]] = field(default_factory=list)
    """Skills available for the Skill tool. List of {name, description}."""

    # Runtime settings
    model: str = "claude-sonnet-4-20250514"
    """Model to use for inference."""

    max_tokens: int = 4096
    """Maximum tokens in response."""

    def build_system_prompt(self) -> str:
        """Compose full system prompt from configured layers.

        Layers are concatenated in order:
        1. Base system prompt (if any)
        2. CLAUDE.md content (if path provided)
        3. Skill content (for each skill path)
        4. Reference content (for each reference path)
        5. Available skills XML (for activation testing)
        """
        parts = []

        if self.system_prompt:
            parts.append(self.system_prompt)

        if self.claude_md_path and self.claude_md_path.exists():
            content = self.claude_md_path.read_text()
            parts.append(f"# Project Context\n\n{content}")

        for skill_path in self.skill_paths:
            if skill_path.exists():
                content = skill_path.read_text()
                parts.append(f"# Skill: {skill_path.stem}\n\n{content}")

        for ref_path in self.reference_paths:
            if ref_path.exists():
                content = ref_path.read_text()
                parts.append(f"# Reference: {ref_path.stem}\n\n{content}")

        if self.available_skills:
            skills_xml = self._build_available_skills_xml()
            parts.append(skills_xml)

        return "\n\n---\n\n".join(parts) if parts else ""

    def _build_available_skills_xml(self) -> str:
        """Build <available_skills> XML block for activation testing."""
        lines = ["<available_skills>"]
        for skill in self.available_skills:
            lines.append("<skill>")
            lines.append(f"  <name>{skill['name']}</name>")
            lines.append(f"  <description>{skill['description']}</description>")
            lines.append("</skill>")
        lines.append("</available_skills>")
        return "\n".join(lines)


@dataclass
class RuntimeResult:
    """Result from running a prompt through the runtime."""

    response: str
    """Final text response from the model."""

    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    """All tool calls made. Each dict has 'name' and 'input'."""

    skills_activated: list[str] = field(default_factory=list)
    """Names of skills that were called via Skill tool."""

    tokens_used: int = 0
    """Total tokens (input + output)."""

    duration_ms: int = 0
    """Execution time in milliseconds."""

    raw_response: Any = None
    """Raw response object from the API (for debugging)."""


class RuntimePort(ABC):
    """Port for executing prompts against an LLM.

    Implementations:
    - AnthropicAdapter: Direct API calls (fast, controllable)
    - MockAdapter: For testing without API calls
    """

    @abstractmethod
    async def run(self, prompt: str, config: EvalConfig) -> RuntimeResult:
        """Run a prompt with the given configuration.

        Args:
            prompt: The user prompt to send
            config: Configuration controlling context and settings

        Returns:
            RuntimeResult with response, tool calls, and metadata
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the runtime is available.

        Returns:
            True if runtime is ready to accept prompts
        """
        pass
