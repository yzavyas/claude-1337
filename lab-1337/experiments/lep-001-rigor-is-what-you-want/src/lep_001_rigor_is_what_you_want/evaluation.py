"""Ground truth evaluation for palindrome task.

This module provides the test suite used to verify correctness of generated code.
The test cases are the "ground truth" - they define what correct behavior means.
"""

import re
import tempfile
import subprocess
from pathlib import Path
from dataclasses import dataclass


# Ground truth test cases from IMP-001
TEST_CASES: list[tuple[str, bool]] = [
    ("A man, a plan, a canal: Panama", True),
    ("race a car", False),
    ("Was it a car or a cat I saw?", True),
    ("", True),
    ("a", True),
    ("ab", False),
    ("Madam", True),
    ("No 'x' in Nixon", True),
    ("hello", False),
    ("12321", True),
]


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


def extract_function(code: str) -> str | None:
    """Extract the is_palindrome function from generated code.

    Handles various formats:
    - Raw function definition
    - Code wrapped in markdown code blocks
    - Multiple functions (takes first is_palindrome)
    """
    # Remove markdown code blocks if present
    code = re.sub(r"```python\s*", "", code)
    code = re.sub(r"```\s*", "", code)

    # Find function definition
    pattern = r"(def is_palindrome\s*\([^)]*\)\s*(?:->.*?)?:\s*(?:\"\"\".*?\"\"\"\s*)?(?:\n(?:[ \t]+.+\n?)+|\n[ \t]+pass))"
    match = re.search(pattern, code, re.DOTALL)

    if match:
        return match.group(1)

    # Fallback: try to find any function and assume it's the implementation
    if "def is_palindrome" in code:
        # Extract from def to next def or end
        lines = code.split("\n")
        in_function = False
        function_lines = []
        indent_level = None

        for line in lines:
            if line.strip().startswith("def is_palindrome"):
                in_function = True
                indent_level = len(line) - len(line.lstrip())
                function_lines.append(line)
            elif in_function:
                if line.strip() == "":
                    function_lines.append(line)
                elif line.strip().startswith("def "):
                    break  # Next function
                elif len(line) - len(line.lstrip()) > indent_level or line.strip() == "":
                    function_lines.append(line)
                elif line.strip() and len(line) - len(line.lstrip()) <= indent_level:
                    break

        if function_lines:
            return "\n".join(function_lines)

    return None


def evaluate_code(code: str) -> EvaluationResult:
    """Evaluate generated palindrome checker code against test suite.

    Args:
        code: The generated Python code containing is_palindrome function

    Returns:
        EvaluationResult with pass/fail counts and details
    """
    errors: list[str] = []
    details: list[dict] = []

    # Extract the function
    function_code = extract_function(code)
    if not function_code:
        return EvaluationResult(
            passed=0,
            failed=len(TEST_CASES),
            total=len(TEST_CASES),
            correctness=False,
            errors=["Could not extract is_palindrome function from code"],
            details=[{"input": tc[0], "expected": tc[1], "actual": None, "passed": False, "error": "No function"} for tc in TEST_CASES]
        )

    # Create test harness
    test_code = f'''
{function_code}

# Test harness
import json
results = []
test_cases = {TEST_CASES!r}

for input_str, expected in test_cases:
    try:
        actual = is_palindrome(input_str)
        passed = actual == expected
        results.append({{"input": input_str, "expected": expected, "actual": actual, "passed": passed, "error": None}})
    except Exception as e:
        results.append({{"input": input_str, "expected": expected, "actual": None, "passed": False, "error": str(e)}})

print(json.dumps(results))
'''

    # Execute in isolated subprocess
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(test_code)
        temp_path = Path(f.name)

    try:
        result = subprocess.run(
            ["python", str(temp_path)],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            errors.append(f"Execution failed: {result.stderr}")
            return EvaluationResult(
                passed=0,
                failed=len(TEST_CASES),
                total=len(TEST_CASES),
                correctness=False,
                errors=errors,
                details=[{"input": tc[0], "expected": tc[1], "actual": None, "passed": False, "error": result.stderr[:200]} for tc in TEST_CASES]
            )

        import json
        details = json.loads(result.stdout)

    except subprocess.TimeoutExpired:
        errors.append("Execution timed out (10s)")
        return EvaluationResult(
            passed=0,
            failed=len(TEST_CASES),
            total=len(TEST_CASES),
            correctness=False,
            errors=errors,
            details=[{"input": tc[0], "expected": tc[1], "actual": None, "passed": False, "error": "Timeout"} for tc in TEST_CASES]
        )
    except json.JSONDecodeError as e:
        errors.append(f"Failed to parse results: {e}")
        return EvaluationResult(
            passed=0,
            failed=len(TEST_CASES),
            total=len(TEST_CASES),
            correctness=False,
            errors=errors,
            details=[{"input": tc[0], "expected": tc[1], "actual": None, "passed": False, "error": "Parse error"} for tc in TEST_CASES]
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
        details=details
    )


# For direct testing
if __name__ == "__main__":
    # Test with a correct implementation
    correct_code = '''
def is_palindrome(s: str) -> bool:
    """Check if string is palindrome, ignoring case and non-alphanumeric."""
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
'''

    result = evaluate_code(correct_code)
    print(f"Correct implementation: {result.passed}/{result.total} passed")
    print(f"Correctness: {result.correctness}")

    # Test with incorrect implementation
    incorrect_code = '''
def is_palindrome(s: str) -> bool:
    """Incorrect - doesn't handle case or non-alphanumeric."""
    return s == s[::-1]
'''

    result = evaluate_code(incorrect_code)
    print(f"\nIncorrect implementation: {result.passed}/{result.total} passed")
    print(f"Correctness: {result.correctness}")
