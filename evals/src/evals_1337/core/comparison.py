"""Baseline comparison: measure extension value by comparing configs.

The key question: "Does this extension make Claude better?"

Approach:
1. Run same prompts against multiple configs (baseline, with_skill, etc.)
2. Compute metrics for each config
3. Calculate deltas and statistical significance
"""

import asyncio
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from .models import EvalMetrics, EvalResult, Expectation, Outcome, TestCase, compute_outcome
from ..ports.runtime import EvalConfig, RuntimePort, RuntimeResult


class ComparisonTestCase(TestCase):
    """Test case for comparison evals.

    Extends TestCase with skill activation testing support.
    """

    # For skill activation testing
    target_skill: str | None = None


@dataclass
class ConfigResult:
    """Results for a single config across all test cases."""

    config_name: str
    config: EvalConfig
    results: list[EvalResult] = field(default_factory=list)

    def metrics(self) -> EvalMetrics:
        """Compute aggregate metrics."""
        m = EvalMetrics()
        for r in self.results:
            match r.outcome:
                case Outcome.TP:
                    m.tp += 1
                case Outcome.FP:
                    m.fp += 1
                case Outcome.TN:
                    m.tn += 1
                case Outcome.FN:
                    m.fn += 1
                case Outcome.ACCEPTABLE:
                    m.acceptable += 1
                case Outcome.ERROR:
                    m.errors += 1
        return m


@dataclass
class ComparisonReport:
    """Complete comparison across multiple configs."""

    name: str
    test_cases: list[ComparisonTestCase]
    config_results: list[ConfigResult] = field(default_factory=list)
    runs_per_case: int = 1

    def summary(self) -> list[dict[str, Any]]:
        """Summary table for each config."""
        rows = []
        baseline_f1 = None

        for i, cr in enumerate(self.config_results):
            m = cr.metrics()
            f1 = m.f1

            delta_baseline = None
            delta_previous = None

            if i == 0:
                baseline_f1 = f1
            else:
                if baseline_f1 is not None:
                    delta_baseline = f1 - baseline_f1
                if i > 0:
                    prev_m = self.config_results[i - 1].metrics()
                    delta_previous = f1 - prev_m.f1

            rows.append({
                "config": cr.config_name,
                "precision": round(m.precision, 3),
                "recall": round(m.recall, 3),
                "f1": round(f1, 3),
                "delta_baseline": round(delta_baseline, 3) if delta_baseline is not None else None,
                "delta_previous": round(delta_previous, 3) if delta_previous is not None else None,
                "tp": m.tp,
                "fp": m.fp,
                "tn": m.tn,
                "fn": m.fn,
            })

        return rows


class ComparisonRunner:
    """Runs comparison evals across multiple configs."""

    def __init__(self, runtime: RuntimePort):
        self._runtime = runtime

    async def run_comparison(
        self,
        name: str,
        test_cases: list[ComparisonTestCase],
        configs: dict[str, EvalConfig],
        runs_per_case: int = 3,
    ) -> ComparisonReport:
        """Run test cases against each config and compare results.

        Args:
            name: Name for this comparison
            test_cases: Test cases to run
            configs: Named configs to compare (run in order)
            runs_per_case: Runs per test case (for stochastic handling)

        Returns:
            ComparisonReport with results for each config
        """
        report = ComparisonReport(
            name=name,
            test_cases=test_cases,
            runs_per_case=runs_per_case,
        )

        for config_name, config in configs.items():
            config_result = ConfigResult(
                config_name=config_name,
                config=config,
            )

            for test_case in test_cases:
                for _ in range(runs_per_case):
                    result = await self._run_single(test_case, config)
                    config_result.results.append(result)
                    # Small delay to avoid rate limiting
                    await asyncio.sleep(0.2)

            report.config_results.append(config_result)

        return report

    async def _run_single(
        self,
        test_case: ComparisonTestCase,
        config: EvalConfig,
    ) -> EvalResult:
        """Run a single test case with a config."""
        try:
            runtime_result = await self._runtime.run(test_case.prompt, config)

            # Determine if passed based on test type
            if test_case.target_skill:
                # Skill activation test - check if skill was called OR
                # if response shows domain knowledge (fallback for non-tool scenarios)
                skill_activated = test_case.target_skill in runtime_result.skills_activated

                # Response quality heuristic: longer, substantive responses
                # indicate the skill context is being used
                response = runtime_result.response.lower()
                has_substance = len(runtime_result.response) > 100

                # For domain questions, check if response mentions relevant concepts
                # This is a heuristic until we have LLM-as-judge
                domain_keywords = self._get_domain_keywords(test_case.target_skill)
                has_domain_knowledge = any(kw in response for kw in domain_keywords)

                passed = skill_activated or (has_substance and has_domain_knowledge)
            else:
                # General test - consider passed if we got a substantive response
                passed = len(runtime_result.response) > 50

            outcome = compute_outcome(test_case.expectation, passed)

            return EvalResult(
                test_case=test_case,  # type: ignore (compatible structure)
                passed=passed,
                outcome=outcome,
                duration_ms=runtime_result.duration_ms,
                details={
                    "skills_activated": runtime_result.skills_activated,
                    "tool_calls": runtime_result.tool_calls,
                    "tokens_used": runtime_result.tokens_used,
                    "response_length": len(runtime_result.response),
                    "response_preview": runtime_result.response[:200] if runtime_result.response else "",
                },
            )

        except Exception as e:
            return EvalResult(
                test_case=test_case,  # type: ignore
                passed=False,
                outcome=Outcome.ERROR,
                error=str(e),
            )

    def _get_domain_keywords(self, skill_name: str) -> list[str]:
        """Get domain keywords for a skill to check response quality.

        This is a heuristic until we implement LLM-as-judge.
        """
        # Map skill names to expected keywords in good responses
        keyword_map = {
            "rust-1337": ["clap", "cargo", "crate", "tokio", "async", "ownership", "borrow"],
            "core-1337": ["evidence", "methodology", "principles", "craftsmanship", "verification"],
            "kotlin-1337": ["coroutine", "suspend", "gradle", "jetpack", "compose"],
            "terminal-1337": ["zsh", "bash", "shell", "alias", "prompt"],
        }
        return keyword_map.get(skill_name, [])


def load_configs_from_yaml(yaml_path: Path) -> dict[str, EvalConfig]:
    """Load comparison configs from YAML file.

    Expected format:
    ```yaml
    configs:
      baseline:
        system_prompt: null
        claude_md_path: null
        skill_paths: []

      with_skill:
        claude_md_path: "./CLAUDE.md"
        skill_paths:
          - "plugins/core-1337/SKILL.md"
    ```
    """
    import yaml

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    configs = {}
    base_path = yaml_path.parent

    for name, cfg in data.get("configs", {}).items():
        claude_md = cfg.get("claude_md_path")
        skill_paths = cfg.get("skill_paths", [])
        ref_paths = cfg.get("reference_paths", [])

        configs[name] = EvalConfig(
            system_prompt=cfg.get("system_prompt"),
            claude_md_path=base_path / claude_md if claude_md else None,
            skill_paths=[base_path / p for p in skill_paths],
            reference_paths=[base_path / p for p in ref_paths],
            model=cfg.get("model", "claude-sonnet-4-20250514"),
            max_tokens=cfg.get("max_tokens", 4096),
        )

    return configs
