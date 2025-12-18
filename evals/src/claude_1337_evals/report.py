"""Markdown report generator for activation test results.

Generates reports with rigorous metrics (precision, recall, F1)
rather than just raw activation rate.
"""

from .models import ActivationReport, EvalMetrics, Outcome, RunStatus


def _format_percent(value: float) -> str:
    """Format a float as a percentage."""
    return f"{value * 100:.1f}%"


def _metric_indicator(value: float, thresholds: tuple[float, float] = (0.8, 0.5)) -> str:
    """Return indicator based on metric value."""
    good, ok = thresholds
    if value >= good:
        return "+"
    elif value >= ok:
        return "~"
    return "-"


def generate_markdown_report(report: ActivationReport) -> str:
    """Generate a GitHub-friendly markdown report with rigorous metrics.

    Args:
        report: The activation test report

    Returns:
        Markdown string suitable for PRs/issues
    """
    metrics = report.compute_metrics()
    config = report.config_description or "default"

    lines = [
        f"# Skill Activation Report: {report.suite_name}",
        "",
        f"**Date**: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Configuration**: {config}",
        f"**Total Runs**: {report.total_runs}",
        "",
        "## Overall Metrics",
        "",
        "| Metric | Value | Interpretation |",
        "|--------|-------|----------------|",
        f"| Precision | {_format_percent(metrics.precision)} | When skill activates, is it correct? |",
        f"| Recall | {_format_percent(metrics.recall)} | When skill should activate, does it? |",
        f"| F1 Score | {_format_percent(metrics.f1_score)} | Harmonic mean (balanced metric) |",
        f"| Accuracy | {_format_percent(metrics.accuracy)} | Overall correctness |",
        "",
        "## Confusion Matrix",
        "",
        "```",
        "                    ACTUAL ACTIVATION",
        "                    Yes         No",
        "                +-----------+-----------+",
        f"SHOULD    Yes   |  TP: {metrics.true_positives:3d}  |  FN: {metrics.false_negatives:3d}  |",
        "ACTIVATE        +-----------+-----------+",
        f"          No    |  FP: {metrics.false_positives:3d}  |  TN: {metrics.true_negatives:3d}  |",
        "                +-----------+-----------+",
        "```",
        "",
    ]

    if metrics.acceptable > 0 or metrics.errors > 0:
        lines.extend([
            f"**Excluded**: {metrics.acceptable} acceptable (ambiguous), {metrics.errors} errors",
            "",
        ])

    lines.extend([
        "## Per-Skill Breakdown",
        "",
        "| Skill | Precision | Recall | F1 | TP | FP | TN | FN |",
        "|-------|-----------|--------|----|----|----|----|-----|",
    ])

    skill_metrics = report.skill_metrics()
    for skill_name, sm in sorted(skill_metrics.items()):
        if skill_name == "__none__":
            skill_name = "(negative cases)"
        indicator = _metric_indicator(sm.f1_score)
        lines.append(
            f"| {skill_name} | {_format_percent(sm.precision)} | {_format_percent(sm.recall)} | "
            f"{indicator}{_format_percent(sm.f1_score)} | {sm.true_positives} | {sm.false_positives} | "
            f"{sm.true_negatives} | {sm.false_negatives} |"
        )

    lines.extend([
        "",
        "## Detailed Results",
        "",
    ])

    # Group by outcome for easier scanning
    by_outcome = {
        Outcome.FALSE_NEGATIVE: [],
        Outcome.FALSE_POSITIVE: [],
        Outcome.TRUE_POSITIVE: [],
        Outcome.TRUE_NEGATIVE: [],
        Outcome.ACCEPTABLE: [],
        Outcome.ERROR: [],
    }

    for run in report.runs:
        by_outcome[run.outcome].append(run)

    # Show failures first (most actionable)
    if by_outcome[Outcome.FALSE_NEGATIVE]:
        lines.extend([
            "### False Negatives (Missed Activations)",
            "",
            "These prompts SHOULD have triggered the skill but didn't:",
            "",
        ])
        for run in by_outcome[Outcome.FALSE_NEGATIVE][:10]:  # Limit to 10
            prompt_preview = run.prompt[:60] + "..." if len(run.prompt) > 60 else run.prompt
            lines.append(f"- `{prompt_preview}` (expected: {run.skill_name})")
        if len(by_outcome[Outcome.FALSE_NEGATIVE]) > 10:
            lines.append(f"- ... and {len(by_outcome[Outcome.FALSE_NEGATIVE]) - 10} more")
        lines.append("")

    if by_outcome[Outcome.FALSE_POSITIVE]:
        lines.extend([
            "### False Positives (Incorrect Activations)",
            "",
            "These prompts should NOT have triggered the skill but did:",
            "",
        ])
        for run in by_outcome[Outcome.FALSE_POSITIVE][:10]:
            prompt_preview = run.prompt[:60] + "..." if len(run.prompt) > 60 else run.prompt
            skills = ", ".join(run.skills_activated) if run.skills_activated else "unknown"
            lines.append(f"- `{prompt_preview}` (activated: {skills})")
        if len(by_outcome[Outcome.FALSE_POSITIVE]) > 10:
            lines.append(f"- ... and {len(by_outcome[Outcome.FALSE_POSITIVE]) - 10} more")
        lines.append("")

    if by_outcome[Outcome.ERROR]:
        lines.extend([
            "### Errors",
            "",
        ])
        for run in by_outcome[Outcome.ERROR][:5]:
            prompt_preview = run.prompt[:40] + "..." if len(run.prompt) > 40 else run.prompt
            error_preview = run.error[:60] if run.error else "unknown"
            lines.append(f"- `{prompt_preview}`: {error_preview}")
        lines.append("")

    # Summary of successes (collapsed)
    tp_count = len(by_outcome[Outcome.TRUE_POSITIVE])
    tn_count = len(by_outcome[Outcome.TRUE_NEGATIVE])
    lines.extend([
        f"### Successes: {tp_count} true positives, {tn_count} true negatives",
        "",
    ])

    lines.extend([
        "---",
        "",
        "## Methodology",
        "",
        "Tests run using Claude Agent SDK with labeled expectations.",
        "",
        "**Metrics explained**:",
        "- **Precision**: TP / (TP + FP) - avoids false activations",
        "- **Recall**: TP / (TP + FN) - catches valid triggers",
        "- **F1**: Harmonic mean - balances both concerns",
        "",
        "**Ground truth labels**:",
        "- `must_activate`: Skill should definitely fire",
        "- `should_not_activate`: Skill should NOT fire",
        "- `acceptable`: Either outcome is reasonable (excluded from metrics)",
        "",
        "*Generated by claude-1337-evals*",
    ])

    return "\n".join(lines)


def generate_comparison_report(
    reports: dict[str, ActivationReport],
) -> str:
    """Generate a comparison report across multiple configurations.

    Args:
        reports: Dict mapping config name to ActivationReport

    Returns:
        Markdown comparison report
    """
    first_report = next(iter(reports.values()))

    lines = [
        "# Skill Activation Comparison Report",
        "",
        f"**Date**: {first_report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Configurations tested**: {', '.join(reports.keys())}",
        "",
        "## Overall Comparison",
        "",
    ]

    # Build header
    header = "| Metric |"
    separator = "|--------|"
    for config in reports.keys():
        header += f" {config} |"
        separator += "--------|"
    lines.append(header)
    lines.append(separator)

    # Compute metrics for each config
    all_metrics = {name: report.compute_metrics() for name, report in reports.items()}

    # Add metric rows
    for metric_name, getter in [
        ("Precision", lambda m: m.precision),
        ("Recall", lambda m: m.recall),
        ("F1 Score", lambda m: m.f1_score),
        ("Accuracy", lambda m: m.accuracy),
        ("Activation Rate", lambda m: m.activation_rate),
    ]:
        row = f"| {metric_name} |"
        for config, metrics in all_metrics.items():
            value = getter(metrics)
            row += f" {_format_percent(value)} |"
        lines.append(row)

    lines.extend([
        "",
        "## Confusion Matrices",
        "",
    ])

    for config, metrics in all_metrics.items():
        lines.extend([
            f"### {config}",
            "",
            f"| | Activated | Not Activated |",
            f"|---|-----------|---------------|",
            f"| Should Activate | TP: {metrics.true_positives} | FN: {metrics.false_negatives} |",
            f"| Should Not | FP: {metrics.false_positives} | TN: {metrics.true_negatives} |",
            "",
        ])

    # Analysis
    lines.extend([
        "## Analysis",
        "",
    ])

    # Find best config by F1
    best_config = max(all_metrics.keys(), key=lambda c: all_metrics[c].f1_score)
    best_f1 = all_metrics[best_config].f1_score

    if "baseline" in all_metrics and "forced" in all_metrics:
        baseline_f1 = all_metrics["baseline"].f1_score
        forced_f1 = all_metrics["forced"].f1_score
        improvement = forced_f1 - baseline_f1

        if improvement > 0.1:
            lines.append(f"Forced evaluation improves F1 by {_format_percent(improvement)}.")
        elif improvement > 0:
            lines.append(f"Forced evaluation provides modest improvement ({_format_percent(improvement)}).")
        else:
            lines.append("Forced evaluation shows no improvement over baseline.")

        # Check for precision/recall tradeoff
        baseline_prec = all_metrics["baseline"].precision
        forced_prec = all_metrics["forced"].precision
        if forced_prec < baseline_prec - 0.1:
            lines.append("")
            lines.append(
                f"**Warning**: Forced mode has lower precision ({_format_percent(forced_prec)} vs "
                f"{_format_percent(baseline_prec)}), indicating more false activations."
            )

    lines.extend([
        "",
        f"**Best configuration**: {best_config} (F1: {_format_percent(best_f1)})",
        "",
        "---",
        "*Generated by claude-1337-evals*",
    ])

    return "\n".join(lines)
