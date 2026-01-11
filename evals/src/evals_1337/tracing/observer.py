"""Simple observability for evals.

Shows what's being sent to Claude and what comes back.
Helps debug why evals aren't producing expected results.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from ..ports.runtime import EvalConfig, RuntimeResult


@dataclass
class EvalTrace:
    """Trace of a single eval run."""

    config_name: str
    prompt: str
    config: EvalConfig
    result: RuntimeResult | None = None
    error: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "config_name": self.config_name,
            "prompt": self.prompt,
            "system_prompt_length": len(self.config.build_system_prompt()),
            "model": self.config.model,
            "timestamp": self.timestamp.isoformat(),
            "result": {
                "response_length": len(self.result.response) if self.result else 0,
                "tool_calls": self.result.tool_calls if self.result else [],
                "skills_activated": self.result.skills_activated if self.result else [],
                "tokens_used": self.result.tokens_used if self.result else 0,
                "duration_ms": self.result.duration_ms if self.result else 0,
            } if self.result else None,
            "error": self.error,
        }


class EvalObserver:
    """Observer that records and displays eval traces."""

    def __init__(self, verbose: bool = False, output_dir: Path | None = None):
        """Initialize observer.

        Args:
            verbose: If True, print detailed output during eval
            output_dir: If provided, save traces to JSON files
        """
        self.verbose = verbose
        self.output_dir = output_dir
        self.traces: list[EvalTrace] = []
        self.console = Console()

        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)

    def on_eval_start(self, config_name: str, prompt: str, config: EvalConfig):
        """Called when an eval starts."""
        if self.verbose:
            self.console.print(f"\n[bold blue]━━━ {config_name} ━━━[/bold blue]")
            self.console.print(f"[dim]Prompt:[/dim] {prompt[:100]}...")
            self.console.print(f"[dim]System prompt:[/dim] {len(config.build_system_prompt())} chars")

    def on_eval_complete(
        self,
        config_name: str,
        prompt: str,
        config: EvalConfig,
        result: RuntimeResult,
    ):
        """Called when an eval completes successfully."""
        trace = EvalTrace(
            config_name=config_name,
            prompt=prompt,
            config=config,
            result=result,
        )
        self.traces.append(trace)

        if self.verbose:
            self.console.print(f"[green]✓[/green] Response: {len(result.response)} chars")
            self.console.print(f"[dim]  Tools called:[/dim] {result.tool_calls}")
            self.console.print(f"[dim]  Skills activated:[/dim] {result.skills_activated}")
            self.console.print(f"[dim]  Duration:[/dim] {result.duration_ms}ms")

            # Show response preview
            if result.response:
                preview = result.response[:200] + "..." if len(result.response) > 200 else result.response
                self.console.print(Panel(preview, title="Response Preview", border_style="dim"))

    def on_eval_error(self, config_name: str, prompt: str, config: EvalConfig, error: str):
        """Called when an eval fails."""
        trace = EvalTrace(
            config_name=config_name,
            prompt=prompt,
            config=config,
            error=error,
        )
        self.traces.append(trace)

        if self.verbose:
            self.console.print(f"[red]✗[/red] Error: {error}")

    def print_summary(self):
        """Print summary table of all traces."""
        table = Table(title="Eval Traces Summary")
        table.add_column("Config")
        table.add_column("Prompt", max_width=30)
        table.add_column("System", justify="right")
        table.add_column("Response", justify="right")
        table.add_column("Tools")
        table.add_column("Duration", justify="right")

        for trace in self.traces:
            prompt_preview = trace.prompt[:27] + "..." if len(trace.prompt) > 30 else trace.prompt
            sys_len = len(trace.config.build_system_prompt())

            if trace.result:
                resp_len = len(trace.result.response)
                tools = ", ".join(trace.result.skills_activated) or "-"
                duration = f"{trace.result.duration_ms}ms"
                status = "[green]"
            else:
                resp_len = 0
                tools = "-"
                duration = "-"
                status = "[red]"

            table.add_row(
                f"{status}{trace.config_name}[/]",
                prompt_preview,
                f"{sys_len:,}",
                f"{resp_len:,}",
                tools,
                duration,
            )

        self.console.print(table)

    def save_traces(self, filename: str = "traces.json"):
        """Save all traces to JSON file."""
        if not self.output_dir:
            return

        output_path = self.output_dir / filename
        data = {
            "timestamp": datetime.now().isoformat(),
            "traces": [t.to_dict() for t in self.traces],
        }

        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        self.console.print(f"[dim]Traces saved to {output_path}[/dim]")

    def print_response_comparison(self):
        """Print side-by-side response comparison across configs."""
        # Group traces by prompt
        by_prompt: dict[str, list[EvalTrace]] = {}
        for trace in self.traces:
            if trace.prompt not in by_prompt:
                by_prompt[trace.prompt] = []
            by_prompt[trace.prompt].append(trace)

        for prompt, traces in by_prompt.items():
            self.console.print(f"\n[bold]Prompt:[/bold] {prompt[:80]}...")
            self.console.print()

            for trace in traces:
                if trace.result:
                    preview = trace.result.response[:300] if trace.result.response else "(empty)"
                    self.console.print(Panel(
                        preview,
                        title=f"{trace.config_name} ({len(trace.result.response)} chars)",
                        border_style="blue" if "skill" in trace.config_name else "dim",
                    ))
