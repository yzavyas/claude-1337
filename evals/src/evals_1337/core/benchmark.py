"""A/B Benchmark: Compare baseline vs with-skill.

Simple, clear, config-driven.
"""

import asyncio
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from ..ports.runtime import EvalConfig, RuntimePort, RuntimeResult


@dataclass
class BenchmarkCase:
    """A single test case in the benchmark."""
    prompt: str
    category: str
    expect_improvement: bool
    keywords: list[str] = field(default_factory=list)


@dataclass
class BenchmarkResult:
    """Result of running A vs B for one test case."""
    case: BenchmarkCase
    response_a: str
    response_b: str
    duration_a_ms: int
    duration_b_ms: int

    # Analysis
    keywords_a: list[str] = field(default_factory=list)  # Keywords found in A
    keywords_b: list[str] = field(default_factory=list)  # Keywords found in B

    @property
    def a_keyword_count(self) -> int:
        return len(self.keywords_a)

    @property
    def b_keyword_count(self) -> int:
        return len(self.keywords_b)

    @property
    def b_is_better(self) -> bool:
        """Did B (with skill) produce better response than A (baseline)?"""
        # Simple heuristic: more keywords = better for domain questions
        if self.case.keywords:
            return self.b_keyword_count > self.a_keyword_count
        # For non-keyword cases, similar length means no degradation
        return len(self.response_b) >= len(self.response_a) * 0.8

    @property
    def meets_expectation(self) -> bool:
        """Did result match expectation?"""
        if self.case.expect_improvement:
            return self.b_is_better
        else:
            # For control cases, B shouldn't be worse
            return len(self.response_b) >= len(self.response_a) * 0.5


@dataclass
class BenchmarkReport:
    """Full benchmark report."""
    name: str
    description: str
    results: list[BenchmarkResult] = field(default_factory=list)

    @property
    def improvement_rate(self) -> float:
        """% of cases where B was better."""
        if not self.results:
            return 0.0
        improved = sum(1 for r in self.results if r.b_is_better)
        return improved / len(self.results)

    @property
    def expectation_met_rate(self) -> float:
        """% of cases that met expectations."""
        if not self.results:
            return 0.0
        met = sum(1 for r in self.results if r.meets_expectation)
        return met / len(self.results)

    def summary(self) -> dict[str, Any]:
        """Summary for display/export."""
        return {
            "name": self.name,
            "total_cases": len(self.results),
            "improvement_rate": f"{self.improvement_rate:.1%}",
            "expectation_met_rate": f"{self.expectation_met_rate:.1%}",
            "by_category": self._by_category(),
        }

    def _by_category(self) -> dict[str, dict]:
        """Results grouped by category."""
        categories: dict[str, list[BenchmarkResult]] = {}
        for r in self.results:
            cat = r.case.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(r)

        return {
            cat: {
                "total": len(results),
                "improved": sum(1 for r in results if r.b_is_better),
                "met_expectation": sum(1 for r in results if r.meets_expectation),
            }
            for cat, results in categories.items()
        }


class BenchmarkRunner:
    """Runs A/B benchmark from config."""

    def __init__(self, runtime: RuntimePort):
        self._runtime = runtime

    async def run(self, config_path: Path) -> BenchmarkReport:
        """Run benchmark from YAML config."""
        config = self._load_config(config_path)

        # Build A and B configs
        config_a = self._build_eval_config(config["comparison"]["a"], config_path)
        config_b = self._build_eval_config(config["comparison"]["b"], config_path)

        # Parse test cases
        cases = [
            BenchmarkCase(
                prompt=tc["prompt"],
                category=tc.get("category", "general"),
                expect_improvement=tc.get("expect_improvement", True),
                keywords=tc.get("keywords", []),
            )
            for tc in config["test_cases"]
        ]

        settings = config.get("settings", {})
        runs = settings.get("runs_per_case", 1)

        report = BenchmarkReport(
            name=config["name"],
            description=config.get("description", ""),
        )

        # Run each case
        for case in cases:
            for _ in range(runs):
                result = await self._run_case(case, config_a, config_b)
                report.results.append(result)
                await asyncio.sleep(0.2)  # Rate limiting

        return report

    async def _run_case(
        self,
        case: BenchmarkCase,
        config_a: EvalConfig,
        config_b: EvalConfig,
    ) -> BenchmarkResult:
        """Run A vs B for one case."""
        # Run A (baseline)
        result_a = await self._runtime.run(case.prompt, config_a)

        # Run B (with skill)
        result_b = await self._runtime.run(case.prompt, config_b)

        # Find keywords in responses
        response_a_lower = result_a.response.lower()
        response_b_lower = result_b.response.lower()

        keywords_a = [kw for kw in case.keywords if kw.lower() in response_a_lower]
        keywords_b = [kw for kw in case.keywords if kw.lower() in response_b_lower]

        return BenchmarkResult(
            case=case,
            response_a=result_a.response,
            response_b=result_b.response,
            duration_a_ms=result_a.duration_ms,
            duration_b_ms=result_b.duration_ms,
            keywords_a=keywords_a,
            keywords_b=keywords_b,
        )

    def _load_config(self, config_path: Path) -> dict:
        """Load YAML config."""
        with open(config_path) as f:
            return yaml.safe_load(f)

    def _build_eval_config(self, comparison_config: dict, config_path: Path) -> EvalConfig:
        """Build EvalConfig from comparison config section."""
        base_path = config_path.parent

        skill_paths = []
        for sp in comparison_config.get("skill_paths", []):
            skill_paths.append(base_path / sp)

        return EvalConfig(
            system_prompt=comparison_config.get("system_prompt"),
            skill_paths=skill_paths,
            model=comparison_config.get("model", "claude-sonnet-4-20250514"),
        )
