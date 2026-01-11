"""Data analysis utilities using pandas.

Transforms eval results into DataFrames for aggregation, comparison, and export.
"""

from typing import Any

import pandas as pd

from ..core.models import EvalReport, EvalResult, EvalMetrics, Outcome


def results_to_dataframe(report: EvalReport) -> pd.DataFrame:
    """Convert eval results to a pandas DataFrame.

    Each row is a single test result with columns:
    - prompt, expectation, outcome, passed, duration_ms
    - Plus any details fields
    """
    rows = []
    for r in report.results:
        row = {
            "prompt": r.test_case.prompt,
            "expectation": r.test_case.expectation.value,
            "outcome": r.outcome.value,
            "passed": r.passed,
            "duration_ms": r.duration_ms,
            "error": r.error,
            "timestamp": r.timestamp,
        }
        # Flatten details
        for k, v in r.details.items():
            if isinstance(v, list):
                row[k] = ", ".join(str(x) for x in v)
            else:
                row[k] = v
        rows.append(row)

    return pd.DataFrame(rows)


def aggregate_by_skill(reports: list[EvalReport]) -> pd.DataFrame:
    """Aggregate metrics across multiple skill reports.

    Returns DataFrame with one row per skill:
    - name, precision, recall, f1, accuracy
    - tp, fp, tn, fn counts
    """
    rows = []
    for report in reports:
        m = report.metrics()
        rows.append({
            "skill": report.name,
            "target_type": report.target_type,
            "precision": m.precision,
            "recall": m.recall,
            "f1": m.f1,
            "accuracy": m.accuracy,
            "tp": m.tp,
            "fp": m.fp,
            "tn": m.tn,
            "fn": m.fn,
            "total": m.total,
            "errors": m.errors,
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("f1", ascending=False)
    return df


def compare_modes(reports_by_mode: dict[str, EvalReport]) -> pd.DataFrame:
    """Compare metrics across different prompting modes.

    Input: {"baseline": report1, "smart": report2, "forced": report3}
    Returns DataFrame comparing precision/recall/f1 across modes.
    """
    rows = []
    for mode, report in reports_by_mode.items():
        m = report.metrics()
        rows.append({
            "mode": mode,
            "precision": m.precision,
            "recall": m.recall,
            "f1": m.f1,
            "accuracy": m.accuracy,
            "total": m.total,
        })

    return pd.DataFrame(rows)


def compare_runtimes(
    simulation_report: EvalReport,
    headless_report: EvalReport,
) -> pd.DataFrame:
    """Compare simulation vs headless runtime results.

    Useful for validating that simulation is representative of real behavior.
    """
    rows = []
    for name, report in [("simulation", simulation_report), ("headless", headless_report)]:
        m = report.metrics()
        rows.append({
            "runtime": name,
            "precision": m.precision,
            "recall": m.recall,
            "f1": m.f1,
            "avg_duration_ms": sum(r.duration_ms for r in report.results) / len(report.results) if report.results else 0,
            "total": m.total,
        })

    return pd.DataFrame(rows)


class EvalAnalyzer:
    """High-level analyzer for eval results.

    Supports loading, aggregating, and comparing results across
    multiple runs, modes, and runtimes.
    """

    def __init__(self):
        self.reports: list[EvalReport] = []
        self._df: pd.DataFrame | None = None

    def add_report(self, report: EvalReport) -> None:
        """Add a report to the analyzer."""
        self.reports.append(report)
        self._df = None  # Invalidate cache

    @property
    def dataframe(self) -> pd.DataFrame:
        """Get all results as a single DataFrame."""
        if self._df is None:
            frames = []
            for report in self.reports:
                df = results_to_dataframe(report)
                df["report_name"] = report.name
                df["target_type"] = report.target_type
                df["config"] = str(report.config)
                frames.append(df)
            self._df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
        return self._df

    def summary(self) -> pd.DataFrame:
        """Get summary statistics across all reports."""
        return aggregate_by_skill(self.reports)

    def by_outcome(self) -> pd.DataFrame:
        """Group results by outcome type."""
        df = self.dataframe
        if df.empty:
            return pd.DataFrame()
        return df.groupby("outcome").agg({
            "prompt": "count",
            "duration_ms": "mean",
        }).rename(columns={"prompt": "count", "duration_ms": "avg_duration"})

    def failures(self) -> pd.DataFrame:
        """Get all failure cases (FP and FN)."""
        df = self.dataframe
        if df.empty:
            return pd.DataFrame()
        return df[df["outcome"].isin(["fp", "fn"])].copy()

    def errors(self) -> pd.DataFrame:
        """Get all error cases."""
        df = self.dataframe
        if df.empty:
            return pd.DataFrame()
        return df[df["outcome"] == "error"].copy()

    def to_dict(self) -> dict[str, Any]:
        """Export all data as a dictionary."""
        return {
            "reports": [r.summary() for r in self.reports],
            "total_results": len(self.dataframe),
            "aggregate": self.summary().to_dict(orient="records"),
            "failures": self.failures().to_dict(orient="records"),
        }
