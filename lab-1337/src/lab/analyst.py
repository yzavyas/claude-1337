"""Analyst module for lab-1337.

Uses Strawberry (pythea) for evidence-based verification of claims.
Produces verified markdown reports from experiment results.

The analyst focuses on accuracy and verification. For HTML presentation,
use the reporter module.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from rich.console import Console

console = Console()


@dataclass
class Claim:
    """A claim with evidence citations."""
    text: str
    evidence_ids: list[str]
    confidence: float = 0.95
    verified: bool | None = None
    budget_gap: float | None = None


@dataclass
class AnalysisReport:
    """Verified analysis report."""
    title: str
    summary: str
    claims: list[Claim] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    raw_data: dict = field(default_factory=dict)
    evidence_spans: dict = field(default_factory=dict)
    verification_notes: list[str] = field(default_factory=list)
    verifier_model: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


def extract_claims_from_results(results: dict) -> tuple[list[Claim], dict[str, str]]:
    """Extract verifiable claims and evidence spans from benchmark results.

    Returns (claims, evidence_spans) where evidence_spans maps IDs to text.
    """
    summary = results.get("summary", {})
    raw_results = results.get("results", [])

    # Build evidence spans from raw data
    evidence = {
        "S0": f"Benchmark metadata: model={results.get('model')}, num_problems={results.get('num_problems')}, max_iterations={results.get('max_iterations')}",
        "S1": f"Single-shot summary: total={summary.get('single-shot', {}).get('total')}, passed={summary.get('single-shot', {}).get('passed')}, pass_rate={summary.get('single-shot', {}).get('pass_rate')}, avg_tokens={summary.get('single-shot', {}).get('avg_tokens')}",
        "S2": f"Ralph-style summary: total={summary.get('ralph-style', {}).get('total')}, passed={summary.get('ralph-style', {}).get('passed')}, pass_rate={summary.get('ralph-style', {}).get('pass_rate')}, avg_tokens={summary.get('ralph-style', {}).get('avg_tokens')}, avg_iterations={summary.get('ralph-style', {}).get('avg_iterations')}",
    }

    # Find failures and recoveries
    single_shot_failures = []
    ralph_recoveries = []

    for r in raw_results:
        task_id = r.get("task_id")
        if r.get("strategy") == "single-shot" and not r.get("passed"):
            single_shot_failures.append(task_id)

    for r in raw_results:
        task_id = r.get("task_id")
        if r.get("strategy") == "ralph-style" and r.get("passed") and task_id in single_shot_failures:
            ralph_recoveries.append({
                "task_id": task_id,
                "iterations": r.get("iterations"),
                "tokens": r.get("tokens"),
            })

    evidence["S3"] = f"Single-shot failures: {single_shot_failures}"
    evidence["S4"] = f"Ralph recoveries: {ralph_recoveries}"

    # Build claims with citations
    ss = summary.get("single-shot", {})
    rs = summary.get("ralph-style", {})

    claims = [
        Claim(
            text=f"Single-shot achieved {ss.get('pass_rate', 0):.0%} pass rate ({ss.get('passed')}/{ss.get('total')} problems)",
            evidence_ids=["S1"],
        ),
        Claim(
            text=f"Ralph-style achieved {rs.get('pass_rate', 0):.0%} pass rate ({rs.get('passed')}/{rs.get('total')} problems)",
            evidence_ids=["S2"],
        ),
        Claim(
            text=f"Ralph-style uses {rs.get('avg_tokens', 0) / ss.get('avg_tokens', 1):.1f}x more tokens than single-shot",
            evidence_ids=["S1", "S2"],
        ),
    ]

    if single_shot_failures and ralph_recoveries:
        claims.append(Claim(
            text=f"Ralph-style recovered {len(ralph_recoveries)} problems that single-shot failed: {', '.join(single_shot_failures)}",
            evidence_ids=["S3", "S4"],
        ))

        # Check iteration usage for recoveries
        first_try_recoveries = [r for r in ralph_recoveries if r["iterations"] == 1]
        iteration_needed = [r for r in ralph_recoveries if r["iterations"] > 1]

        if first_try_recoveries:
            claims.append(Claim(
                text=f"{len(first_try_recoveries)} of {len(ralph_recoveries)} recovered problems passed on first ralph-style attempt (iterations=1)",
                evidence_ids=["S4"],
            ))

        if iteration_needed:
            claims.append(Claim(
                text=f"{len(iteration_needed)} problem(s) required multiple iterations to pass: {[r['task_id'] for r in iteration_needed]}",
                evidence_ids=["S4"],
            ))

    return claims, evidence


def verify_claims_with_strawberry(
    claims: list[Claim],
    evidence: dict[str, str],
    verifier_model: str = "gpt-4o-mini",
) -> list[Claim]:
    """Verify claims using Strawberry audit_trace_budget.

    Returns claims with verification results populated.
    """
    try:
        from strawberry.mcp_server import run_audit_trace_budget
    except ImportError:
        console.print("[yellow]Strawberry not available, skipping verification[/yellow]")
        return claims

    # Format steps for audit
    steps = [
        {
            "idx": i,
            "claim": claim.text,
            "cites": claim.evidence_ids,
            "confidence": claim.confidence,
        }
        for i, claim in enumerate(claims)
    ]

    # Format spans
    spans = [{"sid": sid, "text": text} for sid, text in evidence.items()]

    try:
        result = run_audit_trace_budget(
            steps=steps,
            spans=spans,
            verifier_model=verifier_model,
            default_target=0.95,
            units="bits",
        )

        # Update claims with verification results
        for detail in result.get("details", []):
            idx = detail.get("idx")
            if idx < len(claims):
                claims[idx].verified = not detail.get("flagged", False)
                budget_gap = detail.get("budget_gap", {})
                claims[idx].budget_gap = budget_gap.get("min", 0)

        return claims

    except Exception as e:
        console.print(f"[yellow]Verification failed: {e}[/yellow]")
        return claims


def generate_markdown_report(report: AnalysisReport) -> str:
    """Generate markdown report from analysis."""
    # Separate verified and uncertain claims
    verified_claims = [c for c in report.claims if c.verified]
    uncertain_claims = [c for c in report.claims if c.verified is False]
    unverified_claims = [c for c in report.claims if c.verified is None]

    lines = [
        f"# {report.title}",
        "",
        f"**Generated:** {report.timestamp}",
        f"**Verification Model:** {report.verifier_model}" if report.verifier_model else "",
        "",
        "## Executive Summary",
        "",
        report.summary,
        "",
        "## Verified Claims",
        "",
    ]

    # Verified claims
    for i, claim in enumerate(verified_claims):
        lines.append(f"### {i + 1}. [VERIFIED] {claim.text}")
        lines.append("")
        lines.append(f"**Evidence:** {', '.join(claim.evidence_ids)}")
        if claim.budget_gap is not None:
            lines.append(f"**Budget Gap:** {claim.budget_gap:.1f} bits")
        lines.append("")

    # Uncertain claims section
    if uncertain_claims:
        lines.extend([
            "## What Remains Uncertain",
            "",
            "These claims have high budget gaps (>2 bits), meaning the evidence doesn't directly support them.",
            "They may require calculation or inference beyond what's explicitly stated in the evidence.",
            "",
        ])
        for i, claim in enumerate(uncertain_claims):
            lines.append(f"### {i + 1}. [UNCERTAIN] {claim.text}")
            lines.append("")
            lines.append(f"**Evidence:** {', '.join(claim.evidence_ids)}")
            if claim.budget_gap is not None:
                lines.append(f"**Budget Gap:** {claim.budget_gap:.1f} bits")
            lines.append("")

    # Evidence spans
    if report.evidence_spans:
        lines.extend([
            "## Evidence Spans",
            "",
            "<details>",
            "<summary>Raw evidence (click to expand)</summary>",
            "",
        ])
        for sid, text in report.evidence_spans.items():
            lines.append(f"- **{sid}:** {text}")
        lines.extend(["", "</details>", ""])

    # Verification notes
    if report.verification_notes:
        lines.extend([
            "## Verification Notes",
            "",
        ])
        for note in report.verification_notes:
            lines.append(f"- {note}")
        lines.append("")

    # Limitations
    if report.limitations:
        lines.extend([
            "## Limitations",
            "",
        ])
        for lim in report.limitations:
            lines.append(f"- {lim}")
        lines.append("")

    return "\n".join(lines)


def generate_html_report(report: AnalysisReport) -> str:
    """Generate styled HTML report from analysis."""
    claims_html = []
    for i, claim in enumerate(report.claims):
        if claim.verified:
            badge = '<span class="badge verified">VERIFIED</span>'
        elif claim.verified is False:
            badge = '<span class="badge uncertain">UNCERTAIN</span>'
        else:
            badge = '<span class="badge">UNVERIFIED</span>'

        budget_info = ""
        if claim.budget_gap is not None:
            budget_info = f'<div class="budget">Budget Gap: {claim.budget_gap:.1f} bits</div>'

        claims_html.append(f"""
        <div class="claim">
          <h3>{badge} {claim.text}</h3>
          <div class="evidence">Evidence: {', '.join(claim.evidence_ids)}</div>
          {budget_info}
        </div>
        """)

    limitations_html = "".join(f"<li>{lim}</li>" for lim in report.limitations)
    notes_html = "".join(f"<li>{note}</li>" for note in report.verification_notes)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{report.title}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      line-height: 1.65;
      max-width: 900px;
      margin: 0 auto;
      padding: 2rem 1.5rem;
      color: #1a1a1a;
      background: #fafafa;
    }}
    h1 {{ font-size: 1.75rem; font-weight: 600; margin-bottom: 0.5rem; }}
    h2 {{ font-size: 1.25rem; margin: 2rem 0 1rem; padding-bottom: 0.5rem; border-bottom: 2px solid #e0e0e0; }}
    h3 {{ font-size: 1rem; margin: 0; }}
    .meta {{ color: #666; font-size: 0.875rem; margin-bottom: 2rem; }}
    .summary {{ background: #e3f2fd; padding: 1.5rem; border-radius: 8px; margin: 1.5rem 0; }}
    .badge {{
      display: inline-block;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 600;
      margin-right: 0.5rem;
      background: #e0e0e0;
    }}
    .badge.verified {{ background: #e8f5e9; color: #2e7d32; }}
    .badge.uncertain {{ background: #fff3e0; color: #ef6c00; }}
    .claim {{
      background: white;
      padding: 1rem 1.25rem;
      margin: 1rem 0;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }}
    .evidence {{ font-size: 0.875rem; color: #666; margin-top: 0.5rem; }}
    .budget {{ font-size: 0.8rem; color: #888; margin-top: 0.25rem; }}
    ul {{ padding-left: 1.5rem; }}
    li {{ margin: 0.5rem 0; }}
    footer {{
      margin-top: 3rem;
      padding-top: 1.5rem;
      border-top: 1px solid #e0e0e0;
      color: #666;
      font-size: 0.8rem;
      text-align: center;
    }}
  </style>
</head>
<body>
  <h1>{report.title}</h1>
  <p class="meta">Generated: {report.timestamp}</p>

  <div class="summary">
    <p>{report.summary}</p>
  </div>

  <h2>Verified Claims</h2>
  {"".join(claims_html)}

  {"<h2>Verification Notes</h2><ul>" + notes_html + "</ul>" if notes_html else ""}

  {"<h2>Limitations</h2><ul>" + limitations_html + "</ul>" if limitations_html else ""}

  <footer>
    Verified with Strawberry (pythea) &bull; Lab-1337
  </footer>
</body>
</html>"""


def analyze_results(
    results_path: Path,
    output_dir: Path | None = None,
    verify: bool = True,
    verifier_model: str = "gpt-4o-mini",
) -> AnalysisReport:
    """Analyze experiment results and produce verified markdown report.

    Args:
        results_path: Path to results JSON file
        output_dir: Directory for output reports (default: same as results)
        verify: Whether to use Strawberry verification
        verifier_model: Model for Strawberry verification

    Returns:
        AnalysisReport with verified claims
    """
    results = json.loads(results_path.read_text())
    output_dir = output_dir or results_path.parent

    # Extract claims and evidence
    claims, evidence = extract_claims_from_results(results)

    # Verify with Strawberry if enabled
    if verify:
        console.print("[cyan]Verifying claims with Strawberry...[/cyan]")
        claims = verify_claims_with_strawberry(claims, evidence, verifier_model)

    # Build report
    summary = results.get("summary", {})
    ss = summary.get("single-shot", {})
    rs = summary.get("ralph-style", {})

    report = AnalysisReport(
        title=f"Experiment Analysis: {results_path.stem}",
        summary=f"Ralph-style achieved {rs.get('pass_rate', 0):.0%} pass rate vs {ss.get('pass_rate', 0):.0%} for single-shot, "
               f"recovering {rs.get('passed', 0) - ss.get('passed', 0)} failures at {rs.get('avg_tokens', 0) / ss.get('avg_tokens', 1):.1f}x token cost.",
        claims=claims,
        evidence_spans=evidence,
        verifier_model=verifier_model if verify else "",
        limitations=[
            f"Sample size: {results.get('num_problems')} problems",
            f"Single model: {results.get('model')}",
            "Single run per strategy (no confidence intervals)",
        ],
        raw_data=results,
    )

    # Add verification notes
    verified_count = sum(1 for c in claims if c.verified)
    uncertain_count = sum(1 for c in claims if c.verified is False)

    if verify:
        report.verification_notes.append(
            f"Strawberry audit: {verified_count} claims verified, {uncertain_count} uncertain"
        )

    # Write markdown report only (reporter handles HTML)
    md_path = output_dir / f"{results_path.stem}-analysis.md"
    md_path.write_text(generate_markdown_report(report))

    console.print(f"[green]Analysis written:[/green] {md_path}")

    return report
