"""Skill activation testing.

Tests whether skills trigger on the right prompts using precision/recall metrics.
Ground truth: observe actual Skill() tool calls in Claude's response.

Two failure modes:
- False Positive: Triggers when it shouldn't (noise)
- False Negative: Doesn't trigger when it should (miss)
"""

import asyncio
import time
from pathlib import Path

import anthropic
from pydantic import BaseModel, Field

from ..core.models import (
    Expectation,
    Outcome,
    TestCase,
    EvalResult,
    EvalReport,
    compute_outcome,
)


class SkillTestCase(TestCase):
    """Test case for skill activation."""

    @property
    def should_activate(self) -> bool:
        """Should this skill activate for this prompt?"""
        return self.expectation == Expectation.MUST_PASS


class SkillTestSpec(BaseModel):
    """Test specification for a single skill."""

    name: str = Field(min_length=1)
    """Skill name as it appears in available_skills."""

    plugin: str = Field(min_length=1)
    """Plugin containing the skill."""

    test_cases: list[SkillTestCase] = Field(min_length=1)
    """Labeled test cases for this skill."""


class SkillTestSuite(BaseModel):
    """Complete test suite for skill activation."""

    name: str = Field(min_length=1)
    description: str = ""
    skills: list[SkillTestSpec] = Field(min_length=1)
    negative_cases: list[SkillTestCase] = Field(default_factory=list)
    runs_per_case: int = Field(default=5, ge=1, le=20)


# System prompts for different modes
MODES = {
    "baseline": None,
    "smart": """Skills in <available_skills> contain curated knowledge.
Before responding to domain questions, check if a relevant skill exists.""",
    "forced": """Before EVERY response, you MUST:
1. Check <available_skills> for relevant skills
2. For each skill, check: "Does this prompt relate to {skill}? YES/NO"
3. If YES, call Skill(name) before responding""",
}


def build_available_skills(skills: list[dict[str, str]]) -> str:
    """Build the <available_skills> XML block."""
    lines = ["<available_skills>"]
    for skill in skills:
        lines.append("<skill>")
        lines.append(f"  <name>{skill['name']}</name>")
        lines.append(f"  <description>{skill['description']}</description>")
        lines.append("</skill>")
    lines.append("</available_skills>")
    return "\n".join(lines)


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


async def run_single_activation(
    client: anthropic.AsyncAnthropic,
    prompt: str,
    target_skill: str,
    skills: list[dict[str, str]],
    mode: str = "baseline",
    model: str = "claude-sonnet-4-20250514",
) -> tuple[bool, list[str], int]:
    """Run a single prompt and detect if target skill activates."""
    start = time.monotonic()

    available_skills = build_available_skills(skills)
    system_prompt = MODES.get(mode)

    system = available_skills
    if system_prompt:
        system = f"{system_prompt}\n\n{available_skills}"

    response = await client.messages.create(
        model=model,
        max_tokens=1024,
        system=system,
        tools=[SKILL_TOOL],
        messages=[{"role": "user", "content": prompt}],
    )

    skills_called = []
    for block in response.content:
        if block.type == "tool_use" and block.name == "Skill":
            skill_input = block.input
            if isinstance(skill_input, dict) and "skill" in skill_input:
                skills_called.append(skill_input["skill"])

    duration_ms = int((time.monotonic() - start) * 1000)
    target_activated = target_skill in skills_called

    return target_activated, skills_called, duration_ms


async def run_skill_test(
    skill_spec: SkillTestSpec,
    skills: list[dict[str, str]],
    mode: str = "baseline",
    runs: int = 5,
    model: str = "claude-sonnet-4-20250514",
) -> EvalReport:
    """Run activation test for a single skill."""
    client = anthropic.AsyncAnthropic()
    report = EvalReport(
        name=skill_spec.name,
        target_type="skills",
        config={"mode": mode, "runs": runs, "model": model},
    )

    for test_case in skill_spec.test_cases:
        for _ in range(runs):
            try:
                activated, all_skills, duration = await run_single_activation(
                    client=client,
                    prompt=test_case.prompt,
                    target_skill=skill_spec.name,
                    skills=skills,
                    mode=mode,
                    model=model,
                )

                outcome = compute_outcome(test_case.expectation, activated)

                result = EvalResult(
                    test_case=test_case,
                    passed=activated,
                    outcome=outcome,
                    duration_ms=duration,
                    details={
                        "target_skill": skill_spec.name,
                        "skills_activated": all_skills,
                    },
                )

            except Exception as e:
                result = EvalResult(
                    test_case=test_case,
                    passed=False,
                    outcome=Outcome.ERROR,
                    error=str(e),
                )

            report.results.append(result)
            await asyncio.sleep(0.3)

    return report


def load_skill_descriptions(plugin_dir: Path) -> dict[str, str] | None:
    """Load skill name and description from a plugin directory."""
    skill_file = plugin_dir / "SKILL.md"
    if not skill_file.exists():
        return None

    content = skill_file.read_text()

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            name = None
            description = None
            for line in frontmatter.strip().split("\n"):
                if line.startswith("name:"):
                    name = line.split(":", 1)[1].strip().strip('"')
                elif line.startswith("description:"):
                    description = line.split(":", 1)[1].strip().strip('"')

            if name and description:
                return {"name": name, "description": description}

    return None


def discover_skills(plugins_dir: Path) -> list[dict[str, str]]:
    """Discover all skills from a plugins directory."""
    skills = []
    for plugin_dir in plugins_dir.iterdir():
        if plugin_dir.is_dir():
            skill = load_skill_descriptions(plugin_dir)
            if skill:
                skills.append(skill)
    return skills
