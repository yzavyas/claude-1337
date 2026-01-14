#!/usr/bin/env python3
"""
Eval harness for eval-1337 skill.

Uses Claude Agent SDK to test actual skill activation.

Usage:
    python run_eval.py activation    # Run activation (Level 1) eval
    python run_eval.py methodology   # Run methodology (Level 2) eval
    python run_eval.py all           # Run both

    # Options
    --trials N    Number of trials per case (default: 5)
    --dry-run     Run without API calls (mock results)
"""

import asyncio
import json
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

# Try imports
try:
    from claude_agent_sdk import query, ClaudeAgentOptions
    from claude_agent_sdk.types import AssistantMessage, ToolUseBlock
    HAS_SDK = True
except ImportError:
    HAS_SDK = False

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


@dataclass
class ActivationResult:
    case_id: str
    prompt: str
    expectation: str
    activation_rate: float
    correct: bool


@dataclass
class MethodologyResult:
    case_id: str
    prompt: str
    scores: dict
    total_score: float
    passed: bool


def load_suite(name: str) -> dict:
    """Load a test suite JSON file."""
    path = Path(__file__).parent / f"{name}.json"
    with open(path) as f:
        return json.load(f)


async def test_skill_activation(prompt: str, expected_skill: str = "build-eval") -> bool:
    """
    Test if a skill activates for a given prompt.

    Uses Claude Agent SDK to observe actual Skill tool calls.
    """
    if not HAS_SDK:
        return False

    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(allowed_tools=["Skill"])
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    if block.name == "Skill":
                        # Check if it's calling our skill
                        skill_name = block.input.get("skill", "")
                        if expected_skill in skill_name or "eval" in skill_name.lower():
                            return True
    return False


async def run_activation_eval(suite: dict, n_trials: int = 5, dry_run: bool = False) -> dict:
    """
    Run Level 1 (activation) evaluation.

    Tests whether the skill activates on the right prompts.
    """
    results = []

    for case in suite["cases"]:
        if case["expectation"] == "acceptable":
            continue  # Skip edge cases for F1 calculation

        if dry_run:
            # Simulate based on expectation
            activation_rate = 0.9 if case["expectation"] == "must_trigger" else 0.1
        else:
            # Run actual trials
            activations = []
            for trial in range(n_trials):
                try:
                    activated = await test_skill_activation(case["prompt"])
                    activations.append(activated)
                except Exception as e:
                    print(f"  Error on {case['id']}: {e}")
                    activations.append(False)

            activation_rate = sum(activations) / len(activations) if activations else 0

        # Majority vote
        activated = activation_rate > 0.5
        expected_activation = case["expectation"] == "must_trigger"
        correct = activated == expected_activation

        results.append(ActivationResult(
            case_id=case["id"],
            prompt=case["prompt"][:50] + "...",
            expectation=case["expectation"],
            activation_rate=activation_rate,
            correct=correct
        ))

        status = "OK" if correct else "FAIL"
        print(f"  {case['id']}: {status} (rate={activation_rate:.0%})")

    # Calculate metrics
    must_trigger = [r for r in results if r.expectation == "must_trigger"]
    should_not = [r for r in results if r.expectation == "should_not_trigger"]

    tp = sum(1 for r in must_trigger if r.activation_rate > 0.5)
    fn = sum(1 for r in must_trigger if r.activation_rate <= 0.5)
    fp = sum(1 for r in should_not if r.activation_rate > 0.5)
    tn = sum(1 for r in should_not if r.activation_rate <= 0.5)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "results": results,
        "metrics": {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "tp": tp, "fp": fp, "fn": fn, "tn": tn
        },
        "interpretation": interpret_activation(precision, recall, f1)
    }


def interpret_activation(precision: float, recall: float, f1: float) -> dict:
    """Interpret activation metrics and suggest tuning."""
    issues = []
    suggestions = []

    if recall < 0.8:
        issues.append("Low recall - skill not activating enough")
        suggestions.append("Broaden skill description keywords")
        suggestions.append("Add more trigger phrases to description")

    if precision < 0.8:
        issues.append("Low precision - skill activating too much")
        suggestions.append("Tighten skill description to be more specific")
        suggestions.append("Add exclusion phrases")

    if f1 >= 0.85:
        status = "excellent"
    elif f1 >= 0.70:
        status = "good"
    elif f1 >= 0.50:
        status = "needs_work"
    else:
        status = "poor"

    return {
        "status": status,
        "issues": issues,
        "suggestions": suggestions
    }


async def run_methodology_eval(rubric: dict, n_trials: int = 1, dry_run: bool = False) -> dict:
    """
    Run Level 2 (methodology adherence) evaluation.

    Tests whether responses follow eval-1337 methodology when activated.
    Uses LLM-as-judge to score against rubric.
    """
    if not HAS_ANTHROPIC and not dry_run:
        print("Warning: anthropic not installed. Running in dry-run mode.")
        dry_run = True

    client = anthropic.Anthropic() if HAS_ANTHROPIC else None
    results = []

    for case in rubric["test_cases"]:
        if dry_run:
            # Mock scores
            scores = {c["name"]: 2.0 for c in rubric["rubric"]["criteria"]}
        else:
            # Get response and score it
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,
                messages=[{"role": "user", "content": case["prompt"]}]
            )
            response_text = response.content[0].text
            scores = await score_methodology(client, response_text, case, rubric["rubric"])

        # Calculate weighted total
        total = sum(
            scores[c["name"]] / 3 * c["weight"]  # Normalize to 0-1
            for c in rubric["rubric"]["criteria"]
        )

        results.append(MethodologyResult(
            case_id=case["id"],
            prompt=case["prompt"][:50] + "...",
            scores=scores,
            total_score=total,
            passed=total >= case["min_score"]
        ))

        status = "PASS" if total >= case["min_score"] else "FAIL"
        print(f"  {case['id']}: {status} (score={total:.0%})")

    # Aggregate
    avg_total = sum(r.total_score for r in results) / len(results)
    pass_rate = sum(1 for r in results if r.passed) / len(results)

    # Find weak criteria
    criterion_avgs = {}
    for criterion in rubric["rubric"]["criteria"]:
        name = criterion["name"]
        criterion_avgs[name] = sum(r.scores[name] for r in results) / len(results)

    weak_criteria = [
        name for name, avg in criterion_avgs.items()
        if avg < 2.0  # Below "good" threshold
    ]

    return {
        "results": results,
        "metrics": {
            "avg_score": avg_total,
            "pass_rate": pass_rate,
            "criterion_averages": criterion_avgs
        },
        "interpretation": {
            "status": "excellent" if avg_total >= 0.85 else "good" if avg_total >= 0.70 else "needs_work",
            "weak_criteria": weak_criteria,
            "suggestions": generate_methodology_suggestions(weak_criteria)
        }
    }


async def score_methodology(client, response: str, case: dict, rubric: dict) -> dict:
    """Use LLM-as-judge to score methodology adherence."""

    criteria_text = "\n".join(
        f"- {c['name']}: {c['description']}\n  Levels: {json.dumps(c['levels'])}"
        for c in rubric["criteria"]
    )

    judge_prompt = f"""Score this response on eval methodology adherence.

PROMPT: {case['prompt']}

RESPONSE:
{response[:2000]}

CRITERIA:
{criteria_text}

For each criterion, output a score 0-3 based on the levels defined.
Output JSON only: {{"metric_selection": N, "failure_modes": N, "non_determinism": N, "framework_guidance": N, "pitfall_awareness": N, "actionability": N}}
"""

    judge_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[{"role": "user", "content": judge_prompt}]
    )

    try:
        text = judge_response.content[0].text
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
    except:
        pass

    # Fallback: neutral scores
    return {c["name"]: 1.5 for c in rubric["criteria"]}


def generate_methodology_suggestions(weak_criteria: list) -> list:
    """Generate tuning suggestions based on weak criteria."""
    suggestions = {
        "metric_selection": "Add more explicit metric recommendations to SKILL.md tables",
        "failure_modes": "Emphasize dual failure mode thinking in core sections",
        "non_determinism": "Make pass@k/pass^k guidance more prominent",
        "framework_guidance": "Expand framework decision matrix with more use cases",
        "pitfall_awareness": "Add more entries to the common pitfalls table",
        "actionability": "Include more code examples in references"
    }
    return [suggestions.get(c, f"Review {c} section") for c in weak_criteria]


def print_results(eval_type: str, results: dict):
    """Pretty print evaluation results."""
    print(f"\n{'='*60}")
    print(f"  {eval_type.upper()} EVALUATION RESULTS")
    print(f"{'='*60}\n")

    if eval_type == "activation":
        m = results["metrics"]
        print(f"Precision: {m['precision']:.1%}")
        print(f"Recall:    {m['recall']:.1%}")
        print(f"F1:        {m['f1']:.1%}")
        print(f"\nConfusion Matrix:")
        print(f"  TP={m['tp']} FP={m['fp']}")
        print(f"  FN={m['fn']} TN={m['tn']}")

        interp = results["interpretation"]
        print(f"\nStatus: {interp['status'].upper()}")
        if interp["issues"]:
            print("\nIssues:")
            for issue in interp["issues"]:
                print(f"  - {issue}")
        if interp["suggestions"]:
            print("\nSuggestions:")
            for sug in interp["suggestions"]:
                print(f"  - {sug}")

    elif eval_type == "methodology":
        m = results["metrics"]
        print(f"Average Score: {m['avg_score']:.1%}")
        print(f"Pass Rate:     {m['pass_rate']:.1%}")
        print(f"\nCriterion Averages (0-3 scale):")
        for name, avg in m["criterion_averages"].items():
            status = "OK" if avg >= 2.0 else "WEAK"
            print(f"  {name}: {avg:.1f} [{status}]")

        interp = results["interpretation"]
        print(f"\nStatus: {interp['status'].upper()}")
        if interp["weak_criteria"]:
            print("\nWeak Areas:")
            for weak in interp["weak_criteria"]:
                print(f"  - {weak}")
        if interp["suggestions"]:
            print("\nSuggestions:")
            for sug in interp["suggestions"]:
                print(f"  - {sug}")


async def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    eval_type = sys.argv[1].lower()

    # Parse options
    n_trials = 5
    dry_run = False

    for i, arg in enumerate(sys.argv):
        if arg == "--trials" and i + 1 < len(sys.argv):
            n_trials = int(sys.argv[i + 1])
        if arg == "--dry-run":
            dry_run = True

    if not HAS_SDK and not dry_run:
        print("Warning: claude_agent_sdk not installed.")
        print("Install with: pip install claude-agent-sdk")
        print("Or run with --dry-run for mock results.\n")

    if eval_type in ("activation", "all"):
        suite = load_suite("activation-suite")
        print(f"Running activation eval ({len(suite['cases'])} cases, {n_trials} trials)...")
        results = await run_activation_eval(suite, n_trials, dry_run)
        print_results("activation", results)

    if eval_type in ("methodology", "all"):
        rubric = load_suite("methodology-rubric")
        print(f"\nRunning methodology eval ({len(rubric['test_cases'])} cases)...")
        results = await run_methodology_eval(rubric, n_trials=1, dry_run=dry_run)
        print_results("methodology", results)

    if eval_type not in ("activation", "methodology", "all"):
        print(f"Unknown eval type: {eval_type}")
        print("Use: activation, methodology, or all")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
