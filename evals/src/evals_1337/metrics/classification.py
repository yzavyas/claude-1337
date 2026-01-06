"""Classification metrics formatting and display."""

from ..core.models import EvalMetrics


def format_metrics(m: EvalMetrics) -> str:
    """Format metrics as a readable string."""
    return (
        f"Precision: {m.precision:.1%}  "
        f"Recall: {m.recall:.1%}  "
        f"F1: {m.f1:.1%}"
    )


def format_confusion_matrix(m: EvalMetrics) -> str:
    """Format confusion matrix as ASCII art."""
    return f"""
                    ACTUAL
                    Pass        Fail
                +-----------+-----------+
EXPECTED  Pass  |  TP: {m.tp:3d}  |  FN: {m.fn:3d}  |
                +-----------+-----------+
          Fail  |  FP: {m.fp:3d}  |  TN: {m.tn:3d}  |
                +-----------+-----------+
"""


def metric_indicator(value: float) -> str:
    """Return indicator based on metric value."""
    if value >= 0.85:
        return "[green]✓[/green]"
    elif value >= 0.70:
        return "[yellow]~[/yellow]"
    else:
        return "[red]✗[/red]"
