"""Skill activation runner using Claude Agent SDK.

Runs prompts through Claude Code and detects if skills are activated
by monitoring for Skill() tool calls in the response stream.

This version supports labeled test cases with ground truth expectations,
enabling precision/recall metrics rather than just raw activation rate.
"""

import asyncio
import os
import time
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, query
from claude_agent_sdk.types import AssistantMessage, TextBlock, ToolUseBlock

from .models import (
    ActivationReport,
    ActivationRun,
    Expectation,
    Outcome,
    RunStatus,
    TestCase,
    TestSuite,
    compute_outcome,
)

# Default plugin paths - each plugin must be loaded individually
# Goes from src/claude_1337_evals/runner.py -> evals -> claude-1337 -> plugins
DEFAULT_PLUGINS_PATH = Path(__file__).resolve().parent.parent.parent.parent / "plugins"

# System prompt that forces skill evaluation before responding
# WARNING: This artificially inflates activation rates - use only for testing hooks
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

# No system prompt - true baseline
BASELINE_SYSTEM_PROMPT = None


def get_default_options(
    plugin_paths: list[Path] | None = None,
    mode: str = "baseline",
) -> ClaudeAgentOptions:
    """Create default options with marketplace plugins loaded.

    The Agent SDK requires individual plugin paths (each with .claude-plugin/plugin.json),
    not the marketplace root.

    Args:
        plugin_paths: List of plugin directories to load
        mode: One of "baseline", "smart", or "forced"
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

    system_prompt = {
        "baseline": BASELINE_SYSTEM_PROMPT,
        "smart": SMART_EVAL_SYSTEM_PROMPT,
        "forced": FORCED_EVAL_SYSTEM_PROMPT,
    }.get(mode, BASELINE_SYSTEM_PROMPT)

    return ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep", "Skill", "WebSearch"],
        plugins=[{"type": "local", "path": str(p)} for p in plugin_paths],
        system_prompt=system_prompt,
    )


async def run_single_test(
    skill_name: str,
    test_case: TestCase,
    options: ClaudeAgentOptions | None = None,
) -> ActivationRun:
    """Run a single test and detect skill activation.

    Args:
        skill_name: Name of the skill we're testing
        test_case: The test case with prompt and expectation
        options: Optional ClaudeAgentOptions for customization

    Returns:
        ActivationRun with results including outcome (TP/FP/TN/FN)
    """
    start_time = time.monotonic()
    tool_calls: list[str] = []
    skills_activated: list[str] = []
    skill_called = False
    response_text = ""
    error: str | None = None

    if options is None:
        options = get_default_options()

    try:
        async for message in query(prompt=test_case.prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_text += block.text[:500]
                    elif isinstance(block, ToolUseBlock):
                        tool_calls.append(block.name)
                        if block.name == "Skill":
                            # Extract which skill was activated
                            skill_input = block.input
                            if isinstance(skill_input, dict) and "skill" in skill_input:
                                activated_skill = skill_input["skill"]
                                skills_activated.append(activated_skill)
                                if activated_skill == skill_name:
                                    skill_called = True
                            else:
                                # Skill was called but couldn't parse which one
                                skill_called = True

    except Exception as e:
        error = str(e)

    duration_ms = int((time.monotonic() - start_time) * 1000)

    if error:
        status = RunStatus.ERROR
        outcome = Outcome.ERROR  # Error cases are excluded from metrics
    elif skill_called:
        status = RunStatus.ACTIVATED
        outcome = compute_outcome(test_case.expectation, True)
    else:
        status = RunStatus.NOT_ACTIVATED
        outcome = compute_outcome(test_case.expectation, False)

    return ActivationRun(
        skill_name=skill_name,
        prompt=test_case.prompt,
        expectation=test_case.expectation,
        status=status,
        outcome=outcome,
        skill_called=skill_called,
        skills_activated=skills_activated,
        tool_calls=tool_calls,
        response_preview=response_text[:200],
        duration_ms=duration_ms,
        error=error,
    )


async def run_test_suite(
    suite: TestSuite,
    options: ClaudeAgentOptions | None = None,
    config_description: str = "",
) -> ActivationReport:
    """Run a complete test suite with labeled expectations.

    Args:
        suite: The test suite configuration
        options: Optional ClaudeAgentOptions
        config_description: Description of the config (e.g., "baseline", "with_hooks")

    Returns:
        ActivationReport with precision/recall metrics
    """
    report = ActivationReport(
        suite_name=suite.name,
        config_description=config_description,
    )

    # Run skill-specific test cases
    for skill_spec in suite.skills:
        for test_case in skill_spec.test_cases:
            for _ in range(suite.runs_per_case):
                run = await run_single_test(
                    skill_name=skill_spec.name,
                    test_case=test_case,
                    options=options,
                )
                report.runs.append(run)
                await asyncio.sleep(0.5)

    # Run negative test cases (should not trigger any skill)
    for test_case in suite.negative_cases:
        for _ in range(suite.runs_per_case):
            run = await run_single_test(
                skill_name="__none__",  # Special marker for "no skill expected"
                test_case=test_case,
                options=options,
            )
            report.runs.append(run)
            await asyncio.sleep(0.5)

    return report


async def run_comparison(
    suite: TestSuite,
    modes: list[str] | None = None,
) -> dict[str, ActivationReport]:
    """Run suite across multiple configurations for comparison.

    Args:
        suite: The test suite
        modes: List of modes to test (default: ["baseline", "smart", "forced"])

    Returns:
        Dict mapping mode name to ActivationReport
    """
    if modes is None:
        modes = ["baseline", "smart", "forced"]

    results = {}
    for mode in modes:
        options = get_default_options(mode=mode)
        report = await run_test_suite(
            suite,
            options,
            config_description=mode,
        )
        results[mode] = report

    return results


# Legacy function for backwards compatibility
async def run_baseline_comparison(
    suite: TestSuite,
) -> tuple[ActivationReport, ActivationReport]:
    """Run suite with and without forced eval for comparison.

    DEPRECATED: Use run_comparison() instead.
    """
    results = await run_comparison(suite, modes=["baseline", "forced"])
    return results["baseline"], results["forced"]
