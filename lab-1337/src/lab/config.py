"""Configuration loading for experiments.

Tasks: YAML files defining prompts and test cases.
Agents: Markdown files with frontmatter defining system prompts and iteration config.
"""

import re
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field


class TestCase(BaseModel):
    """A single test case for evaluation."""

    input: Any
    expected: Any
    description: str = ""


class TaskConfig(BaseModel):
    """Configuration for a coding task."""

    name: str
    description: str = ""
    prompt: str
    review_prompt: str = ""  # Optional, used for self-review strategy
    function_name: str
    test_cases: list[TestCase] = Field(default_factory=list)


class IterationConfig(BaseModel):
    """Configuration for iteration strategy."""

    strategy: Literal["none", "test-feedback", "self-review", "ralph"] = "none"
    max_iterations: int = 1
    feedback_template: str = ""  # For test-feedback strategy
    review_template: str = ""  # For self-review strategy


class AgentConfig(BaseModel):
    """Configuration for an experimental agent/condition."""

    name: str
    description: str = ""
    system_prompt: str
    iteration: IterationConfig = Field(default_factory=IterationConfig)


def parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}, content

    # Find the closing ---
    end_match = re.search(r"\n---\s*\n", content[3:])
    if not end_match:
        return {}, content

    frontmatter_str = content[3 : end_match.start() + 3]
    body = content[end_match.end() + 3 :]

    frontmatter = yaml.safe_load(frontmatter_str) or {}
    return frontmatter, body


def load_task(task_path: Path) -> TaskConfig:
    """Load a task configuration from YAML file."""
    with open(task_path) as f:
        data = yaml.safe_load(f)
    return TaskConfig.model_validate(data)


def load_agent(agent_path: Path) -> AgentConfig:
    """Load an agent configuration from markdown file."""
    content = agent_path.read_text()
    frontmatter, _ = parse_frontmatter(content)
    return AgentConfig.model_validate(frontmatter)


def list_tasks(tasks_dir: Path) -> list[str]:
    """List available task names."""
    return [p.stem for p in tasks_dir.glob("*.yaml")]


def list_agents(agents_dir: Path) -> list[str]:
    """List available agent names."""
    return [p.stem for p in agents_dir.glob("*.md")]


