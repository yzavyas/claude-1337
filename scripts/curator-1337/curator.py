#!/usr/bin/env python3
"""
curator-1337: Evolutionary skill curator

Monitors for deprecations, finds new best-in-class options, and creates
PRs with evidence-based updates.

Usage:
    python curator.py [--check rust|terminal|all] [--dry-run]
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Agent SDK imports (will be available when running in GHA)
try:
    from anthropic import Anthropic
except ImportError:
    print("⚠️  Anthropic SDK not installed. Run: pip install -r requirements.txt")
    sys.exit(1)


class CuratorAgent:
    """Evolutionary curator for claude-1337 skills"""

    def __init__(self, api_key: str, dry_run: bool = False):
        self.client = Anthropic(api_key=api_key)
        self.dry_run = dry_run
        self.repo_root = Path(__file__).parent.parent.parent
        self.findings: List[Dict] = []

    def run_check(self, check_type: str) -> None:
        """Run specified check type"""
        print(f"\n🔍 Running {check_type} check...")

        if check_type == "rust":
            self.check_rust_ecosystem()
        elif check_type == "terminal":
            self.check_terminal_tools()
        elif check_type == "all":
            self.check_rust_ecosystem()
            self.check_terminal_tools()
        else:
            print(f"❌ Unknown check type: {check_type}")
            return

        self.summarize_findings()

    def check_rust_ecosystem(self) -> None:
        """Check for Rust crate deprecations and new best-in-class options"""
        print("  → Checking Rust ecosystem...")

        rust_skill = self.repo_root / "plugins" / "rust-1337" / "SKILL.md"
        skill_content = rust_skill.read_text()

        prompt = self._load_prompt("detect-rust-updates.md")
        prompt = prompt.replace("{SKILL_CONTENT}", skill_content)

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )

        self._parse_findings(response.content[0].text, "rust-1337")

    def check_terminal_tools(self) -> None:
        """Check for terminal tool updates and new alternatives"""
        print("  → Checking terminal tools...")

        terminal_skill = self.repo_root / "plugins" / "terminal-1337" / "skills" / "SKILL.md"
        skill_content = terminal_skill.read_text()

        prompt = self._load_prompt("detect-tool-updates.md")
        prompt = prompt.replace("{SKILL_CONTENT}", skill_content)

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )

        self._parse_findings(response.content[0].text, "terminal-1337")

    def _load_prompt(self, filename: str) -> str:
        """Load prompt template"""
        prompt_path = Path(__file__).parent / "prompts" / filename
        if not prompt_path.exists():
            print(f"⚠️  Prompt not found: {filename}")
            return ""
        return prompt_path.read_text()

    def _parse_findings(self, response: str, plugin: str) -> None:
        """Parse agent response and extract findings"""
        # Look for structured findings in response
        if "NO UPDATES NEEDED" in response.upper():
            print(f"    ✅ {plugin}: up to date")
            return

        # Extract findings (simplified - in production, use structured output)
        lines = response.split("\n")
        current_finding = None

        for line in lines:
            if line.startswith("## FINDING:"):
                if current_finding:
                    self.findings.append(current_finding)
                current_finding = {"plugin": plugin, "type": "", "description": "", "evidence": []}
            elif current_finding:
                if line.startswith("TYPE:"):
                    current_finding["type"] = line.replace("TYPE:", "").strip()
                elif line.startswith("DESCRIPTION:"):
                    current_finding["description"] = line.replace("DESCRIPTION:", "").strip()
                elif line.startswith("EVIDENCE:"):
                    current_finding["evidence"].append(line.replace("EVIDENCE:", "").strip())

        if current_finding:
            self.findings.append(current_finding)
            print(f"    ⚠️  {plugin}: {len(self.findings)} update(s) found")

    def summarize_findings(self) -> None:
        """Summarize and report findings"""
        print("\n" + "=" * 60)
        print(f"📊 CURATOR SUMMARY ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
        print("=" * 60)

        if not self.findings:
            print("✅ All skills are up to date. No action needed.")
            return

        print(f"\n⚠️  Found {len(self.findings)} update(s):\n")
        for i, finding in enumerate(self.findings, 1):
            print(f"{i}. [{finding['plugin']}] {finding['type']}")
            print(f"   {finding['description']}")
            if finding["evidence"]:
                print(f"   Evidence: {', '.join(finding['evidence'][:2])}")
            print()

        if not self.dry_run:
            self.create_pr()
        else:
            print("🏃 Dry run mode - no PR created")

    def create_pr(self) -> None:
        """Create PR with findings"""
        print("\n📝 Creating pull request...")

        # Create a branch
        branch_name = f"curator/updates-{datetime.now().strftime('%Y%m%d')}"

        try:
            subprocess.run(["git", "checkout", "-b", branch_name], check=True, cwd=self.repo_root)

            # Apply updates (in production, actually modify files based on findings)
            pr_body = self._generate_pr_body()

            # For now, just create a summary file
            summary_path = self.repo_root / "curator-findings.md"
            summary_path.write_text(pr_body)

            subprocess.run(["git", "add", "curator-findings.md"], check=True, cwd=self.repo_root)
            subprocess.run(
                ["git", "commit", "-m", f"curator: skill updates {datetime.now().strftime('%Y-%m-%d')}"],
                check=True,
                cwd=self.repo_root,
            )

            print(f"✅ Created branch: {branch_name}")
            print("   Run 'git push' and create PR manually, or configure GH_TOKEN for automation")

        except subprocess.CalledProcessError as e:
            print(f"❌ Git operation failed: {e}")

    def _generate_pr_body(self) -> str:
        """Generate PR description"""
        body = "# Curator-1337: Skill Updates\n\n"
        body += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
        body += "## Findings\n\n"

        for finding in self.findings:
            body += f"### {finding['plugin']}: {finding['type']}\n\n"
            body += f"{finding['description']}\n\n"
            if finding["evidence"]:
                body += "**Evidence**:\n"
                for ev in finding["evidence"]:
                    body += f"- {ev}\n"
                body += "\n"

        body += "---\n\n"
        body += "*This PR was automatically generated by curator-1337*\n"

        return body


def main():
    parser = argparse.ArgumentParser(description="curator-1337: Evolutionary skill curator")
    parser.add_argument(
        "--check",
        choices=["rust", "terminal", "all"],
        default="all",
        help="Type of check to run",
    )
    parser.add_argument("--dry-run", action="store_true", help="Run without creating PR")
    args = parser.parse_args()

    # Get API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set")
        sys.exit(1)

    # Run curator
    curator = CuratorAgent(api_key=api_key, dry_run=args.dry_run)
    curator.run_check(args.check)


if __name__ == "__main__":
    main()
