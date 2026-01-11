"""
Official Claude Code Extension Schemas

Pydantic models defining the complete schema for Claude Code extensions.
Source: https://code.claude.com/docs/en/plugins-reference.md

These models are the source of truth - references must document ALL fields here.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


# =============================================================================
# Shared Types
# =============================================================================


class HookType(str, Enum):
    COMMAND = "command"
    PROMPT = "prompt"


class HookEvent(str, Enum):
    PRE_TOOL_USE = "PreToolUse"
    POST_TOOL_USE = "PostToolUse"
    USER_PROMPT_SUBMIT = "UserPromptSubmit"
    STOP = "Stop"
    SUBAGENT_STOP = "SubagentStop"
    PERMISSION_REQUEST = "PermissionRequest"
    SESSION_START = "SessionStart"
    SESSION_END = "SessionEnd"
    PRE_COMPACT = "PreCompact"
    NOTIFICATION = "Notification"


class ModelChoice(str, Enum):
    INHERIT = "inherit"
    SONNET = "sonnet"
    OPUS = "opus"
    HAIKU = "haiku"


class AgentColor(str, Enum):
    BLUE = "blue"
    CYAN = "cyan"
    GREEN = "green"
    YELLOW = "yellow"
    MAGENTA = "magenta"
    RED = "red"


# =============================================================================
# Hook Schemas
# =============================================================================


class HookAction(BaseModel):
    """Individual hook action within a hook entry."""

    type: HookType
    command: str | None = None  # For type=command
    prompt: str | None = None  # For type=prompt
    timeout: int | None = Field(default=60, description="Timeout in seconds")
    once: bool | None = Field(default=False, description="Run only once per invocation")


class HookEntry(BaseModel):
    """Hook entry with optional matcher and actions."""

    matcher: str | None = Field(
        default=None, description="Tool name pattern (regex). Required for PreToolUse/PostToolUse/PermissionRequest"
    )
    hooks: list[HookAction]


class HooksConfig(BaseModel):
    """Complete hooks.json schema."""

    description: str | None = None
    hooks: dict[HookEvent, list[HookEntry]]


# =============================================================================
# Skill Schema
# =============================================================================


class SkillFrontmatter(BaseModel):
    """
    Complete skill frontmatter schema.

    Source: https://code.claude.com/docs/en/skills.md
    """

    name: str = Field(description="Skill identifier")
    description: str = Field(
        max_length=1024, description="What it does + 'Use when:' triggers. Max 1024 chars."
    )

    # Optional fields
    allowed_tools: str | list[str] | None = Field(
        default=None, alias="allowed-tools", description="Restrict tools when skill active"
    )
    model: str | None = Field(default=None, description="Override model for this skill")
    context: Literal["fork"] | None = Field(
        default=None, description="Run in isolated sub-agent context"
    )
    agent: str | None = Field(
        default=None, description="Agent type when using context: fork (Explore, Plan, general-purpose)"
    )
    hooks: dict[HookEvent, list[HookEntry]] | None = Field(
        default=None, description="Skill-scoped hooks"
    )
    user_invocable: bool = Field(
        default=True, alias="user-invocable", description="Show in slash command menu"
    )
    disable_model_invocation: bool = Field(
        default=False,
        alias="disable-model-invocation",
        description="Block Skill tool from invoking this skill",
    )

    class Config:
        populate_by_name = True


# =============================================================================
# Command Schema
# =============================================================================


class CommandFrontmatter(BaseModel):
    """
    Complete slash command frontmatter schema.

    Source: https://code.claude.com/docs/en/slash-commands.md
    """

    description: str = Field(description="Shows in /slash menu")

    # Optional fields
    allowed_tools: str | list[str] | None = Field(
        default=None, alias="allowed-tools", description="Restrict which tools command can use"
    )
    argument_hint: str | None = Field(
        default=None,
        alias="argument-hint",
        description="Expected arguments for autocomplete. E.g., '[pr-number] [priority]'",
    )
    model: str | None = Field(
        default=None, description="Specific model to use. E.g., 'claude-3-5-haiku-20241022'"
    )
    context: Literal["fork"] | None = Field(
        default=None, description="Run command in isolated sub-agent"
    )
    agent: str | None = Field(default=None, description="Model when using context: fork")
    hooks: dict[HookEvent, list[HookEntry]] | None = Field(
        default=None, description="Command-scoped hooks. Supports 'once: true' for single execution."
    )
    disable_model_invocation: bool = Field(
        default=False,
        alias="disable-model-invocation",
        description="Prevent Skill tool from invoking this command",
    )

    class Config:
        populate_by_name = True


# =============================================================================
# Agent Schema
# =============================================================================


class AgentFrontmatter(BaseModel):
    """
    Complete agent frontmatter schema.

    Source: https://code.claude.com/docs/en/sub-agents.md
    """

    name: str = Field(
        min_length=3, max_length=50, description="Identifier (lowercase, hyphens, 3-50 chars)"
    )
    description: str = Field(
        description="Triggering conditions + <example> blocks with <commentary>"
    )
    model: ModelChoice = Field(description="inherit, sonnet, opus, or haiku")
    color: AgentColor = Field(description="Visual identifier in UI")

    # Optional fields
    tools: list[str] | None = Field(
        default=None, description="Array of allowed tools. Default: all tools"
    )
    skills: str | list[str] | None = Field(
        default=None,
        description="Skills to load into subagent context at startup. Subagents don't inherit skills.",
    )

    class Config:
        populate_by_name = True


# =============================================================================
# Plugin Schema
# =============================================================================


class Author(BaseModel):
    """Plugin author information."""

    name: str
    email: str | None = None
    url: str | None = None


class PluginManifest(BaseModel):
    """
    Complete plugin.json schema.

    Source: https://code.claude.com/docs/en/plugins-reference.md
    """

    name: str = Field(description="Plugin identifier (kebab-case, unique)")

    # Recommended fields
    description: str | None = Field(
        default=None, description="What it does + 'Use when:' triggers"
    )
    version: str | None = Field(default=None, description="Semver (e.g., '0.1.0')")
    author: Author | None = None

    # Optional fields
    homepage: str | None = Field(default=None, description="URL to documentation")
    repository: str | None = Field(default=None, description="URL to source code")
    license: str | None = Field(default=None, description="SPDX identifier")
    keywords: list[str] | None = Field(default=None, description="Search terms")
    strict: bool = Field(
        default=False,
        description="Path traversal control. true=contained, false=can access siblings",
    )

    # Component path overrides (auto-discovered from standard locations)
    commands: str | None = Field(default=None, description="Path to commands directory")
    agents: str | None = Field(default=None, description="Path to agents directory")
    skills: str | None = Field(default=None, description="Path to skills directory")
    hooks: str | None = Field(default=None, description="Path to hooks config")
    mcpServers: str | None = Field(default=None, description="Path to MCP config")
    lspServers: str | None = Field(default=None, description="Path to LSP config")


# =============================================================================
# MCP Schema
# =============================================================================


class MCPServerType(str, Enum):
    STDIO = "stdio"
    HTTP = "http"  # Recommended
    SSE = "sse"  # Deprecated
    WEBSOCKET = "websocket"


class MCPServerConfig(BaseModel):
    """
    MCP server configuration.

    Source: https://code.claude.com/docs/en/mcp.md
    """

    # For stdio servers
    command: str | None = None
    args: list[str] | None = None

    # For HTTP/SSE/WebSocket servers
    type: MCPServerType | None = None
    url: str | None = None
    headers: dict[str, str] | None = Field(
        default=None, description="Authentication headers (Bearer token, API keys)"
    )

    # Common
    env: dict[str, str] | None = Field(
        default=None, description="Environment variables. Supports ${VAR} and ${VAR:-default}"
    )


class MCPConfig(BaseModel):
    """Complete .mcp.json schema."""

    mcpServers: dict[str, MCPServerConfig]


# =============================================================================
# Marketplace Schema
# =============================================================================


class MarketplacePlugin(BaseModel):
    """Plugin entry in marketplace.json."""

    name: str
    source: str = Field(description="Path to plugin directory")
    description: str | None = None
    version: str | None = None
    author: Author | None = None
    homepage: str | None = None
    repository: str | None = None
    license: str | None = None
    keywords: list[str] | None = None
    category: str | None = None
    strict: bool = False
    skills: list[str] | None = Field(
        default=None, description="Paths to skills directories"
    )


class MarketplaceOwner(BaseModel):
    """Marketplace owner information."""

    name: str
    email: str | None = None


class MarketplaceMetadata(BaseModel):
    """Marketplace metadata."""

    description: str | None = None
    version: str | None = None


class MarketplaceConfig(BaseModel):
    """Complete marketplace.json schema."""

    name: str
    owner: MarketplaceOwner | None = None
    metadata: MarketplaceMetadata | None = None
    plugins: list[MarketplacePlugin]


# =============================================================================
# Schema Registry
# =============================================================================

SCHEMAS = {
    "skill": SkillFrontmatter,
    "command": CommandFrontmatter,
    "agent": AgentFrontmatter,
    "plugin": PluginManifest,
    "hooks": HooksConfig,
    "mcp": MCPConfig,
    "marketplace": MarketplaceConfig,
}


def get_schema_fields(schema_name: str) -> set[str]:
    """Get all field names for a schema, including aliases."""
    schema = SCHEMAS.get(schema_name)
    if not schema:
        raise ValueError(f"Unknown schema: {schema_name}")

    fields = set()
    for name, field_info in schema.model_fields.items():
        fields.add(name)
        # Add alias if present
        if field_info.alias:
            fields.add(field_info.alias)

    return fields


def get_required_fields(schema_name: str) -> set[str]:
    """Get required field names for a schema."""
    schema = SCHEMAS.get(schema_name)
    if not schema:
        raise ValueError(f"Unknown schema: {schema_name}")

    required = set()
    for name, field_info in schema.model_fields.items():
        if field_info.is_required():
            required.add(name)
            if field_info.alias:
                required.add(field_info.alias)

    return required
