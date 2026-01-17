"""Ground truth evaluation for coding tasks.

This module provides the test runner used to verify correctness of generated code.
Test cases come from the TaskConfig - they define what correct behavior means.
"""

import re
import json
import tempfile
import subprocess
from pathlib import Path
from dataclasses import dataclass

from .config import TaskConfig, TestCase


@dataclass
class EvaluationResult:
    """Result of evaluating generated code against test suite."""

    passed: int
    failed: int
    total: int
    correctness: bool  # All tests passed
    errors: list[str]  # Any execution errors
    details: list[dict]  # Per-test results

    @property
    def success_rate(self) -> float:
        """Proportion of tests that passed."""
        return self.passed / self.total if self.total > 0 else 0.0


def extract_code(code: str, function_name: str) -> str | None:
    """Clean up code from generated response.

    Handles:
    - Code wrapped in markdown code blocks
    - Verifies target function exists

    Returns all code as-is (preserving helper functions).
    """
    # Remove markdown code blocks if present
    cleaned = re.sub(r"```python\s*", "", code)
    cleaned = re.sub(r"```\s*", "", cleaned)

    # Verify target function exists
    if f"def {function_name}" not in cleaned:
        return None

    return cleaned.strip()


def evaluate_code(code: str, task: TaskConfig) -> EvaluationResult:
    """Evaluate generated code against task's test suite.

    Args:
        code: The generated Python code
        task: TaskConfig with function_name and test_cases

    Returns:
        EvaluationResult with pass/fail counts and details
    """
    errors: list[str] = []
    test_cases = task.test_cases

    # Extract the code (including helper functions)
    function_code = extract_code(code, task.function_name)
    if not function_code:
        return EvaluationResult(
            passed=0,
            failed=len(test_cases),
            total=len(test_cases),
            correctness=False,
            errors=[f"Could not extract {task.function_name} function from code"],
            details=[
                {"input": str(tc.input), "expected": str(tc.expected), "actual": None, "passed": False, "error": "No function"}
                for tc in test_cases
            ],
        )

    # Build test cases list for the harness
    test_cases_repr = [(tc.input, tc.expected) for tc in test_cases]

    # Create test harness
    test_code = f'''
{function_code}

# Test harness
import json
results = []
test_cases = {test_cases_repr!r}

for input_data, expected in test_cases:
    try:
        # Handle both single-arg and multi-arg functions
        if isinstance(input_data, list) and len(input_data) > 0 and not isinstance(input_data[0], list):
            # If input is a flat list (not list of lists), unpack as args
            # e.g., ["text", 10] becomes function("text", 10)
            # but [[1,2],[3,4]] stays as function([[1,2],[3,4]])
            actual = {task.function_name}(*input_data)
        else:
            actual = {task.function_name}(input_data)
        # Normalize for comparison (handle lists of lists)
        if isinstance(actual, list) and actual and isinstance(actual[0], list):
            actual_sorted = sorted([sorted(x) for x in actual])
            expected_sorted = sorted([sorted(x) for x in expected]) if expected else []
        else:
            actual_sorted = actual
            expected_sorted = expected
        passed = actual_sorted == expected_sorted
        results.append({{"input": str(input_data), "expected": str(expected), "actual": str(actual), "passed": passed, "error": None}})
    except Exception as e:
        results.append({{"input": str(input_data), "expected": str(expected), "actual": None, "passed": False, "error": str(e)}})

print(json.dumps(results))
'''

    # Execute in isolated subprocess
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(test_code)
        temp_path = Path(f.name)

    try:
        result = subprocess.run(["python", str(temp_path)], capture_output=True, text=True, timeout=10)

        if result.returncode != 0:
            errors.append(f"Execution failed: {result.stderr}")
            return EvaluationResult(
                passed=0,
                failed=len(test_cases),
                total=len(test_cases),
                correctness=False,
                errors=errors,
                details=[
                    {"input": str(tc.input), "expected": str(tc.expected), "actual": None, "passed": False, "error": result.stderr[:200]}
                    for tc in test_cases
                ],
            )

        details = json.loads(result.stdout)

    except subprocess.TimeoutExpired:
        errors.append("Execution timed out (10s)")
        return EvaluationResult(
            passed=0,
            failed=len(test_cases),
            total=len(test_cases),
            correctness=False,
            errors=errors,
            details=[
                {"input": str(tc.input), "expected": str(tc.expected), "actual": None, "passed": False, "error": "Timeout"}
                for tc in test_cases
            ],
        )
    except json.JSONDecodeError as e:
        errors.append(f"Failed to parse results: {e}")
        return EvaluationResult(
            passed=0,
            failed=len(test_cases),
            total=len(test_cases),
            correctness=False,
            errors=errors,
            details=[
                {"input": str(tc.input), "expected": str(tc.expected), "actual": None, "passed": False, "error": "Parse error"}
                for tc in test_cases
            ],
        )
    finally:
        temp_path.unlink(missing_ok=True)

    passed = sum(1 for d in details if d["passed"])
    failed = len(details) - passed

    return EvaluationResult(
        passed=passed,
        failed=failed,
        total=len(details),
        correctness=passed == len(details),
        errors=errors,
        details=details,
    )
