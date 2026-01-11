"""Display utilities using rich.

Pretty-print eval results to the terminal.
"""

import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from ..core.models import EvalMetrics, EvalReport


console = Console()


def metric_style(value: float) -> str:
    """Get rich style based on metric value."""
    if value >= 0.85:
        return "green"
    elif value >= 0.70:
        return "yellow"
    else:
        return "red"


def display_confusion_matrix(metrics: EvalMetrics) -> None:
    """Display confusion matrix as a rich panel."""
    matrix = f"""
                    ACTUAL
                    Pass        Fail
                +-----------+-----------+
EXPECTED  Pass  |  TP: {metrics.tp:3d}  |  FN: {metrics.fn:3d}  |
                +-----------+-----------+
          Fail  |  FP: {metrics.fp:3d}  |  TN: {metrics.tn:3d}  |
                +-----------+-----------+
"""
    console.print(Panel(matrix, title="Confusion Matrix", border_style="dim"))


def display_metrics(metrics: EvalMetrics, title: str = "Metrics") -> None:
    """Display precision/recall/F1 metrics."""
    p_style = metric_style(metrics.precision)
    r_style = metric_style(metrics.recall)
    f1_style = metric_style(metrics.f1)

    text = Text()
    text.append("Precision: ", style="bold")
    text.append(f"{metrics.precision:.1%}", style=p_style)
    text.append("  Recall: ", style="bold")
    text.append(f"{metrics.recall:.1%}", style=r_style)
    text.append("  F1: ", style="bold")
    text.append(f"{metrics.f1:.1%}", style=f1_style)

    console.print(Panel(text, title=title, border_style="dim"))


def display_summary(report: EvalReport) -> None:
    """Display a full report summary."""
    metrics = report.metrics()

    # Header
    console.print(f"\n[bold]{report.name}[/bold]", style="blue")
    console.print(f"Type: {report.target_type}", style="dim")

    # Results table
    table = Table(title="Results")
    table.add_column("Prompt", style="dim", max_width=50)
    table.add_column("Expected")
    table.add_column("Outcome")

    for r in report.results[:10]:  # Limit to first 10
        prompt = r.test_case.prompt[:47] + "..." if len(r.test_case.prompt) > 50 else r.test_case.prompt
        expected = "pass" if r.test_case.expectation.value == "must_pass" else "fail"

        outcome_style = {
            "tp": "green", "tn": "green",
            "fp": "red", "fn": "red",
            "error": "red", "acceptable": "yellow",
        }.get(r.outcome.value, "white")

        table.add_row(
            prompt,
            expected,
            f"[{outcome_style}]{r.outcome.value.upper()}[/{outcome_style}]",
        )

    if len(report.results) > 10:
        table.add_row("...", "...", f"[dim]+{len(report.results) - 10} more[/dim]")

    console.print(table)

    # Metrics
    display_confusion_matrix(metrics)
    display_metrics(metrics)


def display_comparison(df: pd.DataFrame, title: str = "Comparison") -> None:
    """Display a pandas DataFrame as a rich table."""
    table = Table(title=title)

    # Add columns
    for col in df.columns:
        table.add_column(str(col))

    # Add rows
    for _, row in df.iterrows():
        cells = []
        for col in df.columns:
            val = row[col]
            if isinstance(val, float):
                if col in ("precision", "recall", "f1", "accuracy"):
                    style = metric_style(val)
                    cells.append(f"[{style}]{val:.1%}[/{style}]")
                else:
                    cells.append(f"{val:.2f}")
            else:
                cells.append(str(val))
        table.add_row(*cells)

    console.print(table)


def display_pass_at_k(pass_at_k: float, pass_hat_k: float, k: int = 3) -> None:
    """Display pass@k and pass^k metrics."""
    text = Text()
    text.append(f"pass@{k}: ", style="bold")
    text.append(f"{pass_at_k:.1%}", style=metric_style(pass_at_k))
    text.append(f"  pass^{k}: ", style="bold")
    text.append(f"{pass_hat_k:.1%}", style=metric_style(pass_hat_k))

    console.print(Panel(
        text,
        title="Stochastic Metrics",
        subtitle="pass@k = any success, pass^k = all succeed",
        border_style="dim",
    ))
