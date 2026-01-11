"""Skill simulation adapter - direct API with mock Skill tool.

This is fast but not realistic:
- Doesn't use actual Claude Code
- Mock Skill tool, not real skill loading
- Good for quick iteration, not final validation
"""

import asyncio
import time
from typing import Any

import anthropic

from ...core.models import (
    TestCase,
    EvalResult,
    EvalReport,
    Expectation,
    Outcome,
    compute_outcome,
)


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


class SkillSimulationRunner:
    """Simulation adapter for skill activation testing."""

    def __init__(
        self,
        model: str = "claude-sonnet-4-20250514",
        mode: str = "baseline",
    ):
        self.model = model
        self.mode = mode
        self._client: anthropic.AsyncAnthropic | None = None

    @property
    def extension_type(self) -> str:
        return "skills"

    @property
    def runtime(self) -> str:
        return "simulation"

    @property
    def client(self) -> anthropic.AsyncAnthropic:
        if self._client is None:
            self._client = anthropic.AsyncAnthropic()
        return self._client

    async def run_single(
        self,
        test_case: TestCase,
        target_skill: str,
        available_skills: list[dict[str, str]],
        **kwargs,
    ) -> EvalResult:
        """Run a single test case."""
        mode = kwargs.get("mode", self.mode)
        model = kwargs.get("model", self.model)

        start = time.monotonic()

        try:
            skills_xml = build_available_skills(available_skills)
            system_prompt = MODES.get(mode)

            system = skills_xml
            if system_prompt:
                system = f"{system_prompt}\n\n{skills_xml}"

            response = await self.client.messages.create(
                model=model,
                max_tokens=1024,
                system=system,
                tools=[SKILL_TOOL],
                messages=[{"role": "user", "content": test_case.prompt}],
            )

            # Extract skill calls
            skills_called = []
            for block in response.content:
                if block.type == "tool_use" and block.name == "Skill":
                    skill_input = block.input
                    if isinstance(skill_input, dict) and "skill" in skill_input:
                        skills_called.append(skill_input["skill"])

            duration_ms = int((time.monotonic() - start) * 1000)
            activated = target_skill in skills_called
            outcome = compute_outcome(test_case.expectation, activated)

            return EvalResult(
                test_case=test_case,
                passed=activated,
                outcome=outcome,
                duration_ms=duration_ms,
                details={
                    "target_skill": target_skill,
                    "skills_activated": skills_called,
                    "mode": mode,
                    "runtime": "simulation",
                },
            )

        except Exception as e:
            return EvalResult(
                test_case=test_case,
                passed=False,
                outcome=Outcome.ERROR,
                duration_ms=int((time.monotonic() - start) * 1000),
                error=str(e),
            )

    async def run_batch(
        self,
        test_cases: list[TestCase],
        target_skill: str,
        available_skills: list[dict[str, str]],
        runs: int = 1,
        **kwargs,
    ) -> EvalReport:
        """Run multiple test cases."""
        report = EvalReport(
            name=target_skill,
            target_type=self.extension_type,
            config={
                "mode": kwargs.get("mode", self.mode),
                "runs": runs,
                "model": kwargs.get("model", self.model),
                "runtime": self.runtime,
            },
        )

        for test_case in test_cases:
            for _ in range(runs):
                result = await self.run_single(
                    test_case=test_case,
                    target_skill=target_skill,
                    available_skills=available_skills,
                    **kwargs,
                )
                report.results.append(result)
                await asyncio.sleep(0.3)  # Rate limiting

        return report
