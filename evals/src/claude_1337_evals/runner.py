"""Skill activation runner using Claude Agent SDK.

Runs prompts through Claude Code and detects if skills are activated
by monitoring for Skill() tool calls in the response stream.
"""

import asyncio
import os
import time
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, query
from claude_agent_sdk.types import AssistantMessage, TextBlock, ToolUseBlock

from .models import ActivationReport, ActivationRun, RunStatus, TestSuite

# Default plugin paths - each plugin must be loaded individually
# Goes from src/claude_1337_evals/runner.py -> evals -> claude-1337 -> plugins
DEFAULT_PLUGINS_PATH = Path(__file__).resolve().parent.parent.parent.parent / "plugins"

# System prompt that forces skill evaluation before responding
# Note: "any user request" is costly — this is for testing only
FORCED_EVAL_SYSTEM_PROMPT = """Before responding to any user request, you MUST:

1. EVALUATE each skill in <available_skills>:
   - State: [skill-name] - YES/NO - [one-line reason]

2. ACTIVATE relevant skills:
   - For each YES skill, call Skill(skill-name) BEFORE proceeding
   - This is MANDATORY - do not skip

3. Only THEN respond to the user request."""

# Production-friendly prompt: only evaluate once per topic
SMART_EVAL_SYSTEM_PROMPT = """When you receive a request that might benefit from specialized knowledge:

1. Check if you've already activated a relevant skill this session
2. If not, scan <available_skills> for matches and activate before responding
3. Skip re-evaluation for topics you've already covered

This is a one-time check per topic, not per message."""


def get_default_options(
    plugin_paths: list[Path] | None = None,
    force_eval: bool = False,
) -> ClaudeAgentOptions:
    """Create default options with marketplace plugins loaded.

    The Agent SDK requires individual plugin paths (each with .claude-plugin/plugin.json),
    not the marketplace root.

    Args:
        plugin_paths: List of plugin directories to load
        force_eval: If True, add system prompt that forces skill evaluation
    """
    if plugin_paths is None:
        plugins_root = Path(
            os.environ.get("CLAUDE_1337_PLUGINS", DEFAULT_PLUGINS_PATH)
        )
        # Load all plugins from the plugins directory
        plugin_paths = [
            p for p in plugins_root.iterdir()
            if p.is_dir() and (p / ".claude-plugin").exists()
        ]

    return ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep", "Skill", "WebSearch"],
        plugins=[{"type": "local", "path": str(p)} for p in plugin_paths],
        system_prompt=FORCED_EVAL_SYSTEM_PROMPT if force_eval else None,
    )


async def run_single_test(
    skill_name: str,
    prompt: str,
    options: ClaudeAgentOptions | None = None,
) -> ActivationRun:
    """Run a single test and detect skill activation.

    Args:
        skill_name: Name of the skill we expect to be activated
        prompt: The prompt to send to Claude
        options: Optional ClaudeAgentOptions for customization

    Returns:
        ActivationRun with results including whether Skill() was called
    """
    start_time = time.monotonic()
    tool_calls: list[str] = []
    skill_called = False
    response_text = ""
    error: str | None = None

    if options is None:
        options = get_default_options()

    try:
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_text += block.text[:500]
                    elif isinstance(block, ToolUseBlock):
                        tool_calls.append(block.name)
                        if block.name == "Skill":
                            skill_called = True

    except Exception as e:
        error = str(e)

    duration_ms = int((time.monotonic() - start_time) * 1000)

    if error:
        status = RunStatus.ERROR
    elif skill_called:
        status = RunStatus.ACTIVATED
    else:
        status = RunStatus.NOT_ACTIVATED

    return ActivationRun(
        skill_name=skill_name,
        prompt=prompt,
        status=status,
        skill_called=skill_called,
        tool_calls=tool_calls,
        response_preview=response_text[:200],
        duration_ms=duration_ms,
        error=error,
    )


async def run_test_suite(
    suite: TestSuite,
    options: ClaudeAgentOptions | None = None,
) -> ActivationReport:
    """Run a complete test suite.

    Args:
        suite: The test suite configuration
        options: Optional ClaudeAgentOptions

    Returns:
        ActivationReport with all results
    """
    report = ActivationReport(suite_name=suite.name)

    for skill in suite.skills:
        for prompt in skill.expected_triggers:
            for _ in range(suite.runs_per_prompt):
                run = await run_single_test(
                    skill_name=skill.name,
                    prompt=prompt,
                    options=options,
                )
                report.runs.append(run)
                await asyncio.sleep(0.5)

    return report


async def run_baseline_comparison(
    suite: TestSuite,
) -> tuple[ActivationReport, ActivationReport]:
    """Run suite with and without forced eval for comparison.

    Args:
        suite: The test suite

    Returns:
        Tuple of (baseline_report, forced_eval_report)
    """
    # Baseline: no system prompt
    baseline_options = get_default_options(force_eval=False)
    baseline_report = await run_test_suite(suite, baseline_options)
    baseline_report.suite_name = f"{suite.name}_baseline"

    # With forced eval: system prompt forces skill evaluation
    forced_options = get_default_options(force_eval=True)
    forced_report = await run_test_suite(suite, forced_options)
    forced_report.suite_name = f"{suite.name}_forced_eval"

    return baseline_report, forced_report
