"""Reporter module for lab-1337.

Transforms analysis markdown into polished HTML reports.
Uses experience-designer principles for presentation.

The reporter focuses on presentation. For verification and accuracy,
use the analyst module.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

from rich.console import Console

console = Console()


@dataclass
class ParsedClaim:
    """A claim parsed from analysis markdown."""
    status: str  # VERIFIED, UNCERTAIN, UNVERIFIED
    text: str
    evidence: str
    budget_gap: float | None = None


@dataclass
class ParsedAnalysis:
    """Analysis parsed from markdown."""
    title: str
    timestamp: str
    verifier_model: str
    summary: str
    verified_claims: list[ParsedClaim] = field(default_factory=list)
    uncertain_claims: list[ParsedClaim] = field(default_factory=list)
    evidence_spans: dict[str, str] = field(default_factory=dict)
    verification_notes: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)


def parse_analysis_md(content: str) -> ParsedAnalysis:
    """Parse analysis markdown into structured data."""
    lines = content.split("\n")

    analysis = ParsedAnalysis(
        title="",
        timestamp="",
        verifier_model="",
        summary="",
    )

    current_section = None
    current_claim = None
    in_details = False

    for line in lines:
        line_stripped = line.strip()

        # Title
        if line.startswith("# "):
            analysis.title = line[2:].strip()
            continue

        # Metadata
        if line.startswith("**Generated:**"):
            analysis.timestamp = line.split("**Generated:**")[1].strip()
            continue
        if line.startswith("**Verification Model:**"):
            analysis.verifier_model = line.split("**Verification Model:**")[1].strip()
            continue

        # Section headers
        if line.startswith("## "):
            section = line[3:].strip()
            if section == "Executive Summary":
                current_section = "summary"
            elif section == "Verified Claims":
                current_section = "verified"
            elif section == "What Remains Uncertain":
                current_section = "uncertain"
            elif section == "Evidence Spans":
                current_section = "evidence"
            elif section == "Verification Notes":
                current_section = "notes"
            elif section == "Limitations":
                current_section = "limitations"
            else:
                current_section = None
            continue

        # Details tag handling
        if "<details>" in line:
            in_details = True
            continue
        if "</details>" in line:
            in_details = False
            continue
        if "<summary>" in line:
            continue

        # Parse claims
        if line.startswith("### ") and current_section in ("verified", "uncertain"):
            # Save previous claim
            if current_claim:
                if current_section == "verified":
                    analysis.verified_claims.append(current_claim)
                else:
                    analysis.uncertain_claims.append(current_claim)

            # Parse new claim
            claim_match = re.match(r"### \d+\. \[(\w+)\] (.+)", line)
            if claim_match:
                current_claim = ParsedClaim(
                    status=claim_match.group(1),
                    text=claim_match.group(2),
                    evidence="",
                )
            continue

        # Parse claim details
        if current_claim:
            if line.startswith("**Evidence:**"):
                current_claim.evidence = line.split("**Evidence:**")[1].strip()
            elif line.startswith("**Budget Gap:**"):
                gap_str = line.split("**Budget Gap:**")[1].strip()
                try:
                    current_claim.budget_gap = float(gap_str.replace(" bits", ""))
                except ValueError:
                    pass

        # Parse summary
        if current_section == "summary" and line_stripped and not line.startswith("**"):
            if analysis.summary:
                analysis.summary += " " + line_stripped
            else:
                analysis.summary = line_stripped

        # Parse evidence spans
        if current_section == "evidence" and line.startswith("- **S"):
            match = re.match(r"- \*\*(\w+):\*\* (.+)", line)
            if match:
                analysis.evidence_spans[match.group(1)] = match.group(2)

        # Parse notes
        if current_section == "notes" and line.startswith("- "):
            analysis.verification_notes.append(line[2:].strip())

        # Parse limitations
        if current_section == "limitations" and line.startswith("- "):
            analysis.limitations.append(line[2:].strip())

    # Don't forget last claim
    if current_claim:
        if current_section == "verified":
            analysis.verified_claims.append(current_claim)
        elif current_section == "uncertain":
            analysis.uncertain_claims.append(current_claim)

    return analysis


def generate_html_report(analysis: ParsedAnalysis) -> str:
    """Generate styled HTML report from parsed analysis."""

    def render_claim(claim: ParsedClaim) -> str:
        if claim.status == "VERIFIED":
            badge = '<span class="badge verified">VERIFIED</span>'
        elif claim.status == "UNCERTAIN":
            badge = '<span class="badge uncertain">UNCERTAIN</span>'
        else:
            badge = '<span class="badge">UNVERIFIED</span>'

        budget_html = ""
        if claim.budget_gap is not None:
            budget_html = f'<div class="budget">Budget Gap: {claim.budget_gap:.1f} bits</div>'

        return f"""
        <div class="claim">
          <h3>{badge} {claim.text}</h3>
          <div class="evidence">Evidence: {claim.evidence}</div>
          {budget_html}
        </div>
        """

    verified_html = "".join(render_claim(c) for c in analysis.verified_claims)
    uncertain_html = "".join(render_claim(c) for c in analysis.uncertain_claims)

    limitations_html = "".join(f"<li>{lim}</li>" for lim in analysis.limitations)
    notes_html = "".join(f"<li>{note}</li>" for note in analysis.verification_notes)

    evidence_html = ""
    if analysis.evidence_spans:
        evidence_items = "".join(
            f"<li><strong>{sid}:</strong> {text}</li>"
            for sid, text in analysis.evidence_spans.items()
        )
        evidence_html = f"""
        <details class="evidence-details">
          <summary>Evidence Spans</summary>
          <ul>{evidence_items}</ul>
        </details>
        """

    uncertain_section = ""
    if analysis.uncertain_claims:
        uncertain_section = f"""
        <section class="uncertain">
          <h2>What Remains Uncertain</h2>
          <p class="uncertain-note">These claims have high budget gaps, meaning the evidence doesn't directly support them.</p>
          {uncertain_html}
        </section>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{analysis.title}</title>
  <style>
    :root {{
      --color-verified: #2e7d32;
      --color-verified-bg: #e8f5e9;
      --color-uncertain: #ef6c00;
      --color-uncertain-bg: #fff3e0;
      --color-text: #1a1a1a;
      --color-text-secondary: #666;
      --color-bg: #fafafa;
      --color-card: white;
      --color-border: #e0e0e0;
      --color-summary-bg: #e3f2fd;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      line-height: 1.65;
      max-width: 900px;
      margin: 0 auto;
      padding: 2rem 1.5rem;
      color: var(--color-text);
      background: var(--color-bg);
    }}

    header {{
      margin-bottom: 2rem;
    }}

    h1 {{
      font-size: 1.75rem;
      font-weight: 600;
      margin-bottom: 0.5rem;
    }}

    .meta {{
      color: var(--color-text-secondary);
      font-size: 0.875rem;
    }}

    h2 {{
      font-size: 1.25rem;
      margin: 2rem 0 1rem;
      padding-bottom: 0.5rem;
      border-bottom: 2px solid var(--color-border);
    }}

    h3 {{
      font-size: 1rem;
      margin: 0;
      line-height: 1.4;
    }}

    .summary {{
      background: var(--color-summary-bg);
      padding: 1.5rem;
      border-radius: 8px;
      margin: 1.5rem 0;
    }}

    .summary p {{
      margin: 0;
    }}

    .badge {{
      display: inline-block;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 600;
      margin-right: 0.5rem;
      background: var(--color-border);
      vertical-align: middle;
    }}

    .badge.verified {{
      background: var(--color-verified-bg);
      color: var(--color-verified);
    }}

    .badge.uncertain {{
      background: var(--color-uncertain-bg);
      color: var(--color-uncertain);
    }}

    .claim {{
      background: var(--color-card);
      padding: 1rem 1.25rem;
      margin: 1rem 0;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }}

    .evidence {{
      font-size: 0.875rem;
      color: var(--color-text-secondary);
      margin-top: 0.5rem;
    }}

    .budget {{
      font-size: 0.8rem;
      color: #888;
      margin-top: 0.25rem;
    }}

    .uncertain-note {{
      color: var(--color-text-secondary);
      font-size: 0.9rem;
      margin-bottom: 1rem;
    }}

    .evidence-details {{
      margin: 2rem 0;
      padding: 1rem;
      background: var(--color-card);
      border-radius: 8px;
    }}

    .evidence-details summary {{
      cursor: pointer;
      font-weight: 600;
      color: var(--color-text-secondary);
    }}

    .evidence-details ul {{
      margin-top: 1rem;
      padding-left: 1.5rem;
    }}

    .evidence-details li {{
      margin: 0.5rem 0;
      font-size: 0.875rem;
      color: var(--color-text-secondary);
    }}

    section ul {{
      padding-left: 1.5rem;
    }}

    section li {{
      margin: 0.5rem 0;
    }}

    footer {{
      margin-top: 3rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--color-border);
      color: var(--color-text-secondary);
      font-size: 0.8rem;
      text-align: center;
    }}

    @media print {{
      body {{
        background: white;
        padding: 1rem;
      }}
      .claim {{
        box-shadow: none;
        border: 1px solid var(--color-border);
      }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>{analysis.title}</h1>
    <p class="meta">Generated: {analysis.timestamp}{f' | Verified with {analysis.verifier_model}' if analysis.verifier_model else ''}</p>
  </header>

  <section class="summary">
    <p>{analysis.summary}</p>
  </section>

  <section class="verified">
    <h2>Verified Claims</h2>
    {verified_html if verified_html else '<p>No claims verified.</p>'}
  </section>

  {uncertain_section}

  {evidence_html}

  {"<section class='notes'><h2>Verification Notes</h2><ul>" + notes_html + "</ul></section>" if notes_html else ""}

  {"<section class='limitations'><h2>Limitations</h2><ul>" + limitations_html + "</ul></section>" if limitations_html else ""}

  <footer>
    Verified with Strawberry | Lab-1337
  </footer>
</body>
</html>"""


def generate_report(
    analysis_path: Path,
    output_path: Path | None = None,
) -> Path:
    """Generate HTML report from analysis markdown.

    Args:
        analysis_path: Path to analysis markdown file
        output_path: Path for output HTML (default: same name with .html)

    Returns:
        Path to generated HTML file
    """
    content = analysis_path.read_text()
    analysis = parse_analysis_md(content)

    output_path = output_path or analysis_path.with_suffix(".html")
    html = generate_html_report(analysis)
    output_path.write_text(html)

    console.print(f"[green]Report written:[/green] {output_path}")

    return output_path
