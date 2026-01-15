"""Report generation with visual templates."""

import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from jinja2 import Template
from rich.console import Console

from lab_1337.core.experiment import ExperimentResult

console = Console()


REPORT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        :root {
            --bg: #0d1117;
            --fg: #c9d1d9;
            --accent: #58a6ff;
            --success: #3fb950;
            --warning: #d29922;
            --error: #f85149;
            --border: #30363d;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--fg);
            margin: 0;
            padding: 2rem;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: var(--accent);
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.5rem;
        }
        h2 {
            color: var(--fg);
            margin-top: 2rem;
        }
        .meta {
            color: #8b949e;
            font-size: 0.9rem;
        }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }
        .summary-card {
            background: #161b22;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 1rem;
        }
        .summary-card h3 {
            margin: 0 0 0.5rem 0;
            color: var(--accent);
            font-size: 1rem;
        }
        .summary-card .value {
            font-size: 2rem;
            font-weight: bold;
        }
        .success { color: var(--success); }
        .warning { color: var(--warning); }
        .error { color: var(--error); }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }
        th, td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }
        th {
            background: #161b22;
            color: var(--accent);
        }
        .chart {
            margin: 2rem 0;
            background: #161b22;
            border-radius: 6px;
            padding: 1rem;
        }
        .footer {
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
            color: #8b949e;
            font-size: 0.8rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ title }}</h1>
        <p class="meta">
            Generated: {{ generated_at }}<br>
            Duration: {{ duration }}<br>
            Model: {{ model }}
        </p>

        <h2>Summary</h2>
        <div class="summary-grid">
            {% for condition, stats in summary.items() %}
            <div class="summary-card">
                <h3>{{ condition }}</h3>
                <div class="value {% if stats.success_rate >= 0.8 %}success{% elif stats.success_rate >= 0.5 %}warning{% else %}error{% endif %}">
                    {{ "%.1f" | format(stats.success_rate * 100) }}%
                </div>
                <div class="meta">
                    {{ stats.runs }} runs, {{ stats.successes }} passed<br>
                    {{ "%.0f" | format(stats.avg_tokens) }} avg tokens
                </div>
            </div>
            {% endfor %}
        </div>

        <h2>Success Rate Comparison</h2>
        <div class="chart" id="success-chart"></div>

        <h2>Token Usage</h2>
        <div class="chart" id="tokens-chart"></div>

        <h2>Detailed Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Condition</th>
                    <th>Run</th>
                    <th>Status</th>
                    <th>Tokens</th>
                    <th>Duration</th>
                </tr>
            </thead>
            <tbody>
                {% for r in results %}
                <tr>
                    <td>{{ r.condition }}</td>
                    <td>{{ r.run + 1 }}</td>
                    <td class="{% if r.success %}success{% else %}error{% endif %}">
                        {{ "pass" if r.success else "fail" }}
                    </td>
                    <td>{{ r.tokens_used }}</td>
                    <td>{{ r.duration_ms }}ms</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <div class="footer">
            1337 Experiments Lab | Rigorous experiments for the agentic era
        </div>
    </div>

    <script>
        // Success rate chart
        var successData = {{ success_chart_data | safe }};
        Plotly.newPlot('success-chart', successData.data, successData.layout, {responsive: true});

        // Token usage chart
        var tokensData = {{ tokens_chart_data | safe }};
        Plotly.newPlot('tokens-chart', tokensData.data, tokensData.layout, {responsive: true});
    </script>
</body>
</html>
"""


class ReportGenerator:
    """Generate visual HTML reports from experiment results."""

    def __init__(self, result: ExperimentResult):
        self.result = result
        self.df = self._to_dataframe()

    def _to_dataframe(self) -> pd.DataFrame:
        """Convert results to pandas DataFrame."""
        records = []
        for r in self.result.condition_results:
            records.append({
                "condition": r.condition,
                "run": r.run_index,
                "success": r.success,
                "tokens_used": r.tokens_used,
                "duration_ms": r.duration_ms,
                **r.metrics,
            })
        return pd.DataFrame(records)

    def _success_chart(self) -> dict:
        """Generate success rate bar chart data."""
        summary = self.result.summary()
        conditions = list(summary.keys())
        rates = [summary[c]["success_rate"] * 100 for c in conditions]
        colors = [
            "#3fb950" if r >= 80 else "#d29922" if r >= 50 else "#f85149"
            for r in rates
        ]

        return {
            "data": [{
                "type": "bar",
                "x": conditions,
                "y": rates,
                "marker": {"color": colors},
                "text": [f"{r:.1f}%" for r in rates],
                "textposition": "auto",
            }],
            "layout": {
                "paper_bgcolor": "#161b22",
                "plot_bgcolor": "#161b22",
                "font": {"color": "#c9d1d9"},
                "yaxis": {"title": "Success Rate (%)", "range": [0, 100]},
                "xaxis": {"title": "Condition"},
                "margin": {"t": 20},
            }
        }

    def _tokens_chart(self) -> dict:
        """Generate token usage box plot data."""
        traces = []
        for condition in self.df["condition"].unique():
            cond_data = self.df[self.df["condition"] == condition]
            traces.append({
                "type": "box",
                "name": condition,
                "y": cond_data["tokens_used"].tolist(),
                "boxpoints": "all",
                "jitter": 0.3,
                "pointpos": -1.8,
            })

        return {
            "data": traces,
            "layout": {
                "paper_bgcolor": "#161b22",
                "plot_bgcolor": "#161b22",
                "font": {"color": "#c9d1d9"},
                "yaxis": {"title": "Tokens Used"},
                "showlegend": False,
                "margin": {"t": 20},
            }
        }

    def generate(self, output_path: Path | None = None) -> str:
        """Generate HTML report."""
        template = Template(REPORT_TEMPLATE)

        # Calculate duration
        if self.result.completed_at and self.result.started_at:
            duration = self.result.completed_at - self.result.started_at
            duration_str = f"{duration.total_seconds():.1f}s"
        else:
            duration_str = "unknown"

        html = template.render(
            title=f"Experiment: {self.result.config.name}",
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            duration=duration_str,
            model=self.result.config.model,
            summary=self.result.summary(),
            results=self.result.condition_results,
            success_chart_data=json.dumps(self._success_chart()),
            tokens_chart_data=json.dumps(self._tokens_chart()),
        )

        if output_path:
            output_path = Path(output_path)
            output_path.write_text(html)
            console.print(f"[green]Report saved to: {output_path}[/green]")

        return html
