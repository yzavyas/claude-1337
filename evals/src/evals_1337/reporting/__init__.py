"""Reporting and analysis utilities.

Uses pandas for data aggregation and rich for display.
"""

from .analysis import (
    EvalAnalyzer,
    results_to_dataframe,
    aggregate_by_skill,
    compare_modes,
    compare_runtimes,
)
from .display import (
    display_summary,
    display_comparison,
    display_confusion_matrix,
)
from .export import (
    export_json,
    export_csv,
    export_markdown,
)

__all__ = [
    "EvalAnalyzer",
    "results_to_dataframe",
    "aggregate_by_skill",
    "compare_modes",
    "compare_runtimes",
    "display_summary",
    "display_comparison",
    "display_confusion_matrix",
    "export_json",
    "export_csv",
    "export_markdown",
]
