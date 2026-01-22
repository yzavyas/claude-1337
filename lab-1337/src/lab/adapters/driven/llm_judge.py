"""LLM-as-Judge Adapter - Quality evaluation using DeepEval GEval.

This adapter provides post-hoc quality evaluation of completed runs.
It's designed to measure QUALITY independent of CORRECTNESS (pass/fail).

Key insight: A solution can fail tests but demonstrate excellent judgment.
This captures the quality signal masked by floor/ceiling effects.

Uses DeepEval's GEval (LLM-as-judge) for rubric-based evaluation.
"""

import json
import logging
import os
from dataclasses import dataclass
from typing import Any

log = logging.getLogger(__name__)


@dataclass
class QualityScores:
    """Quality scores from LLM-as-judge evaluation."""

    problem_understanding: int  # 0-3
    approach_selection: int  # 0-3
    judgment_under_ambiguity: int  # 0-3 (key discriminator)
    code_quality: int  # 0-3
    reasoning_visibility: int  # 0-3
    rationale: str

    @property
    def total(self) -> int:
        """Sum of all scores (0-15)."""
        return (
            self.problem_understanding
            + self.approach_selection
            + self.judgment_under_ambiguity
            + self.code_quality
            + self.reasoning_visibility
        )

    @property
    def normalized(self) -> float:
        """Normalized score (0-1)."""
        return self.total / 15.0

    @property
    def weighted_total(self) -> float:
        """Weighted total emphasizing judgment_under_ambiguity."""
        weights = {
            "problem_understanding": 1.0,
            "approach_selection": 1.0,
            "judgment_under_ambiguity": 2.0,  # Key discriminator
            "code_quality": 0.5,
            "reasoning_visibility": 1.0,
        }
        return (
            self.problem_understanding * weights["problem_understanding"]
            + self.approach_selection * weights["approach_selection"]
            + self.judgment_under_ambiguity * weights["judgment_under_ambiguity"]
            + self.code_quality * weights["code_quality"]
            + self.reasoning_visibility * weights["reasoning_visibility"]
        )

    @property
    def weighted_normalized(self) -> float:
        """Weighted normalized score (0-1)."""
        max_weighted = 1.0 + 1.0 + 2.0 + 0.5 + 1.0  # 5.5 * 3 = 16.5
        return self.weighted_total / (16.5)

    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return {
            "problem_understanding": self.problem_understanding,
            "approach_selection": self.approach_selection,
            "judgment_under_ambiguity": self.judgment_under_ambiguity,
            "code_quality": self.code_quality,
            "reasoning_visibility": self.reasoning_visibility,
            "rationale": self.rationale,
            "total": self.total,
            "normalized": self.normalized,
            "weighted_total": self.weighted_total,
            "weighted_normalized": self.weighted_normalized,
        }


# Rubric aligned with REP-002 hypothesis:
# "Motivation-based prompting produces better judgment than mandate-based prompting"
QUALITY_RUBRIC = """You are evaluating an AI agent's solution to a software engineering task.

IMPORTANT: Score QUALITY independent of CORRECTNESS. A solution can fail tests but demonstrate excellent judgment, or pass tests with a hacky approach.

## Task Description
{task_description}

## Agent's Solution (Code/Diff)
{solution}

## Agent's Conversation Trace
{trace}

---

Score each dimension 0-3:

### 1. PROBLEM_UNDERSTANDING (0-3)
How well did the agent understand what needs to be done?
- 0: Misunderstood the problem entirely
- 1: Partial grasp, missed key aspects
- 2: Correct understanding of the core issue
- 3: Deep understanding including edge cases and implications

### 2. APPROACH_SELECTION (0-3)
Was the chosen approach reasonable and well-considered?
- 0: Wrong approach, won't solve the problem
- 1: Reasonable but suboptimal approach
- 2: Good approach, appropriate for the task
- 3: Optimal approach with explicit tradeoff consideration

### 3. JUDGMENT_UNDER_AMBIGUITY (0-3) ⭐ KEY DISCRIMINATOR
When requirements were unclear or multiple interpretations existed, how did the agent handle it?
- 0: Ignored ambiguity, proceeded blindly
- 1: Made assumptions without noting them
- 2: Noted the ambiguity and made a reasonable choice
- 3: Explicitly reasoned through alternatives and justified the choice

### 4. CODE_QUALITY (0-3)
Is the code clean, readable, and well-structured?
- 0: Broken, unreadable, or fundamentally flawed
- 1: Functional but messy or hard to understand
- 2: Clean and readable
- 3: Idiomatic, well-structured, production-quality

### 5. REASONING_VISIBILITY (0-3)
Did the agent explain its thinking process?
- 0: No explanation, just code
- 1: Minimal comments or explanation
- 2: Clear reasoning present
- 3: Full chain of thought, well-documented reasoning

---

Return ONLY valid JSON (no markdown, no explanation before/after):
{{
  "problem_understanding": <0-3>,
  "approach_selection": <0-3>,
  "judgment_under_ambiguity": <0-3>,
  "code_quality": <0-3>,
  "reasoning_visibility": <0-3>,
  "rationale": "<brief 1-2 sentence explanation of the key scores>"
}}
"""


class LLMJudgeAdapter:
    """LLM-as-Judge for quality evaluation using DeepEval.

    Uses DeepEval's GEval for rubric-based LLM evaluation.

    Design principles:
    - Blind evaluation: Judge doesn't know which condition produced the output
    - Rubric-based: Explicit criteria for each dimension
    - Hypothesis-aligned: Emphasizes judgment_under_ambiguity
    """

    def __init__(
        self,
        model: str = "claude-3-5-haiku-20241022",  # Fast, cheap judge
    ):
        """Initialize the judge.

        Args:
            model: Model to use for judging (Haiku is fast/cheap)
        """
        self.model = model

    async def evaluate(
        self,
        task_description: str,
        solution: str | None,
        trace: list[dict] | None,
    ) -> QualityScores:
        """Evaluate a single run using DeepEval GEval.

        Args:
            task_description: The original task prompt
            solution: The code/diff produced (may be None if no changes)
            trace: The conversation trace (may be None if not captured)

        Returns:
            QualityScores with all dimensions
        """
        # Format inputs
        solution_text = solution if solution else "(No code changes made)"
        trace_text = self._format_trace(trace) if trace else "(Trace not available)"

        # Build prompt
        prompt = QUALITY_RUBRIC.format(
            task_description=task_description[:2000],  # Truncate long descriptions
            solution=solution_text[:5000],  # Truncate long solutions
            trace=trace_text[:10000],  # Truncate long traces
        )

        try:
            # Use DeepEval's model (respects OPENAI_API_KEY or ANTHROPIC_API_KEY)
            from deepeval.models import DeepEvalBaseLLM
            from deepeval.metrics import GEval
            from deepeval.test_case import LLMTestCase, LLMTestCaseParams

            # Create a simple test case for GEval
            test_case = LLMTestCase(
                input=task_description[:2000],
                actual_output=solution_text[:5000],
            )

            # We'll use a simple approach: call the model directly for scoring
            # since GEval is designed for different use cases
            scores = await self._direct_evaluate(prompt)
            return scores

        except ImportError as e:
            log.warning(f"DeepEval import error, falling back to direct eval: {e}")
            return await self._direct_evaluate(prompt)

        except Exception as e:
            log.error(f"Judge evaluation failed: {e}")
            return QualityScores(
                problem_understanding=0,
                approach_selection=0,
                judgment_under_ambiguity=0,
                code_quality=0,
                reasoning_visibility=0,
                rationale=f"Evaluation error: {e}",
            )

    async def _direct_evaluate(self, prompt: str) -> QualityScores:
        """Direct evaluation using Claude Agent SDK.

        Falls back to this when DeepEval can't be used directly.
        """
        from claude_agent_sdk import (
            query,
            ClaudeAgentOptions,
            AssistantMessage,
            TextBlock,
        )

        options = ClaudeAgentOptions(
            model="haiku",  # Fast, cheap
            max_turns=1,  # Single turn for scoring
            permission_mode="default",
            allowed_tools=[],  # No tools needed for scoring
        )

        content_parts = []
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        content_parts.append(block.text)

        content = "\n".join(content_parts).strip()

        # Try to extract JSON
        try:
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()

            scores_dict = json.loads(content)

            return QualityScores(
                problem_understanding=int(scores_dict.get("problem_understanding", 0)),
                approach_selection=int(scores_dict.get("approach_selection", 0)),
                judgment_under_ambiguity=int(scores_dict.get("judgment_under_ambiguity", 0)),
                code_quality=int(scores_dict.get("code_quality", 0)),
                reasoning_visibility=int(scores_dict.get("reasoning_visibility", 0)),
                rationale=scores_dict.get("rationale", ""),
            )

        except json.JSONDecodeError as e:
            log.error(f"Failed to parse judge response: {e}")
            log.debug(f"Response was: {content}")
            return QualityScores(
                problem_understanding=0,
                approach_selection=0,
                judgment_under_ambiguity=0,
                code_quality=0,
                reasoning_visibility=0,
                rationale=f"Parse error: {e}",
            )

    def _format_trace(self, trace: list[dict]) -> str:
        """Format conversation trace for judge prompt."""
        parts = []
        for i, msg in enumerate(trace[:50], 1):  # Limit to first 50 messages
            role = msg.get("role", "unknown")
            content = msg.get("content", "")

            if isinstance(content, list):
                # Handle structured content (text blocks, tool calls)
                content_text = ""
                for block in content:
                    if isinstance(block, dict):
                        if block.get("type") == "text":
                            content_text += block.get("text", "")
                        else:
                            content_text += f"[{block.get('type')}]"
                    else:
                        content_text += str(block)
                content = content_text

            # Truncate individual messages
            if len(content) > 1000:
                content = content[:1000] + "..."

            parts.append(f"[{i}] {role.upper()}: {content}")

        return "\n\n".join(parts)

    async def evaluate_batch(
        self,
        runs: list[dict],
        get_task_description: callable,
    ) -> list[tuple[dict, QualityScores]]:
        """Evaluate a batch of runs.

        Args:
            runs: List of run dicts (from results.jsonl)
            get_task_description: Callable to get task description by task_id

        Returns:
            List of (run, scores) tuples
        """
        results = []

        for run in runs:
            task_description = get_task_description(run["task_id"])
            solution = run.get("solution")
            trace = run.get("conversation_trace")

            scores = await self.evaluate(task_description, solution, trace)
            results.append((run, scores))

        return results
