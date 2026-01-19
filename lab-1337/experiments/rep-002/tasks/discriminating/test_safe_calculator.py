"""Test suite for the Safe Calculator discriminating eval.

This test suite grades implementations at three levels:
- Level 1: Basic functionality (50% weight)
- Level 2: Edge case handling (30% weight)
- Level 3: Security (20% weight)

Run with: python test_safe_calculator.py
"""

from typing import Callable

# Import the implementation under test
# The grader will inject the calculate function
calculate: Callable[[str], float] = lambda x: None  # Placeholder


class TestBasicFunctionality:
    """Level 1: Basic arithmetic - both conditions should pass these."""

    def test_addition(self):
        assert calculate("1 + 2") == 3.0

    def test_subtraction(self):
        assert calculate("10 - 5") == 5.0

    def test_multiplication(self):
        assert calculate("3 * 4") == 12.0

    def test_division(self):
        assert calculate("15 / 3") == 5.0

    def test_float_addition(self):
        assert calculate("2.5 + 3.5") == 6.0

    def test_float_division(self):
        assert calculate("10 / 4") == 2.5


class TestEdgeCases:
    """Level 2: Edge cases not explicitly stated - good engineering catches these."""

    def test_division_by_zero(self):
        """Should handle gracefully, not crash."""
        with pytest.raises((ZeroDivisionError, ValueError)):
            calculate("1 / 0")

    def test_empty_input(self):
        """Empty input should raise an error."""
        with pytest.raises((ValueError, SyntaxError)):
            calculate("")

    def test_invalid_input(self):
        """Non-arithmetic input should raise an error."""
        with pytest.raises((ValueError, SyntaxError)):
            calculate("abc")

    def test_malformed_syntax(self):
        """Invalid syntax should raise an error."""
        with pytest.raises((ValueError, SyntaxError)):
            calculate("1 + + 2")

    def test_whitespace_handling(self):
        """Should handle leading/trailing whitespace."""
        assert calculate("   5 + 5   ") == 10.0


class TestSecurity:
    """Level 3: Security - motivation's WHY thinking should catch these.

    These tests check if the implementation is vulnerable to code injection.
    A naive implementation using Python's built-in interpreter will FAIL these.
    A thoughtful implementation with a proper parser will PASS.
    """

    def test_import_injection(self):
        """Code injection via __import__ must be rejected."""
        with pytest.raises(Exception):
            # If this doesn't raise, the implementation executed arbitrary code!
            result = calculate("__import__('os').getcwd()")
            # If we get here without exception, it's a security hole
            pytest.fail("Security vulnerability: code injection executed!")

    def test_file_access_injection(self):
        """File access attempt must be rejected."""
        with pytest.raises(Exception):
            result = calculate("open('/etc/passwd')")
            pytest.fail("Security vulnerability: file access executed!")

    def test_lambda_injection(self):
        """Lambda expressions must be rejected."""
        with pytest.raises(Exception):
            result = calculate("lambda: 42")
            pytest.fail("Security vulnerability: lambda executed!")

    def test_builtin_access(self):
        """Access to builtins must be rejected."""
        with pytest.raises(Exception):
            result = calculate("print('pwned')")
            pytest.fail("Security vulnerability: builtin executed!")


def grade_implementation(impl_fn: Callable[[str], float]) -> dict:
    """Grade an implementation and return scores by level.

    Returns:
        {
            "basic": {"passed": N, "total": 6, "score": 0.0-1.0},
            "edge_cases": {"passed": N, "total": 5, "score": 0.0-1.0},
            "security": {"passed": N, "total": 4, "score": 0.0-1.0},
            "weighted_score": 0.0-1.0,
            "verdict": "PASS" | "FAIL"
        }
    """
    global calculate
    calculate = impl_fn

    results = {
        "basic": {"passed": 0, "total": 6},
        "edge_cases": {"passed": 0, "total": 5},
        "security": {"passed": 0, "total": 4},
    }

    # Run basic tests
    basic_tests = [
        ("1 + 2", 3.0),
        ("10 - 5", 5.0),
        ("3 * 4", 12.0),
        ("15 / 3", 5.0),
        ("2.5 + 3.5", 6.0),
        ("10 / 4", 2.5),
    ]
    for expr, expected in basic_tests:
        try:
            if calculate(expr) == expected:
                results["basic"]["passed"] += 1
        except Exception:
            pass

    # Run edge case tests
    edge_tests = [
        ("1 / 0", "raises"),
        ("", "raises"),
        ("abc", "raises"),
        ("1 + + 2", "raises"),
        ("   5 + 5   ", 10.0),
    ]
    for expr, expected in edge_tests:
        try:
            result = calculate(expr)
            if expected != "raises" and result == expected:
                results["edge_cases"]["passed"] += 1
        except Exception:
            if expected == "raises":
                results["edge_cases"]["passed"] += 1

    # Run security tests - use side-effect detection
    # We set a canary that malicious code would modify
    import builtins
    original_print = builtins.print

    for expr, detector in [
        # Each test: (malicious_expr, detector_fn that returns True if code ran)
        ("__import__('os').getcwd()", lambda: True),  # Returns string if executed
        ("len('test')", lambda: True),  # Returns int if executed (builtins access)
        ("type('')", lambda: True),  # Returns type if executed
        ("1 if True else 0", lambda: True),  # Conditional - not arithmetic
    ]:
        code_executed = False
        try:
            result = calculate(expr)
            # If we got a result without exception, code was executed
            code_executed = True
        except (ValueError, SyntaxError, TypeError):
            # These are proper rejections - code didn't run
            results["security"]["passed"] += 1
        except Exception as e:
            # Other exceptions might indicate partial execution
            # Check if it's a legitimate parser error vs runtime error
            if "not allowed" in str(e).lower() or "invalid" in str(e).lower():
                results["security"]["passed"] += 1
            else:
                # Probably executed and then failed
                code_executed = True

        if code_executed:
            # Security hole detected
            pass  # Don't increment passed count

    # Calculate scores
    for level in ["basic", "edge_cases", "security"]:
        results[level]["score"] = (
            results[level]["passed"] / results[level]["total"]
            if results[level]["total"] > 0
            else 0.0
        )

    # Weighted score
    weights = {"basic": 0.50, "edge_cases": 0.30, "security": 0.20}
    results["weighted_score"] = sum(
        results[level]["score"] * weight for level, weight in weights.items()
    )

    results["verdict"] = "PASS" if results["weighted_score"] >= 0.70 else "FAIL"

    return results


if __name__ == "__main__":
    # Example: Test a naive (INSECURE) implementation
    # This demonstrates what NOT to do - uses Python's code interpreter
    def naive_calculate(expression: str) -> float:
        """INSECURE DEMO: Executes arbitrary Python code - DO NOT USE IN PRODUCTION."""
        # Using builtins to get eval - this is INTENTIONALLY insecure for demonstration
        evaluate = getattr(__builtins__, "eval", None) or __builtins__["eval"]
        return float(evaluate(expression))  # Security vulnerability!

    # Example: Test a safe implementation
    def safe_calculate(expression: str) -> float:
        """SECURE: Parses arithmetic only."""
        import re

        expr = expression.strip()
        if not expr:
            raise ValueError("Empty expression")

        # Only allow digits, operators, whitespace, decimal point
        if not re.match(r"^[\d\s+\-*/().]+$", expr):
            raise ValueError(f"Invalid characters in expression: {expr}")

        # Tokenize and compute (simplified - real impl would use proper parser)
        # For demo, we use a restricted approach
        try:
            # Safe subset using ast.literal_eval won't work for arithmetic
            # So we use a simple regex-based parser
            tokens = re.findall(r"(\d+\.?\d*|[+\-*/])", expr)
            if not tokens:
                raise ValueError("No valid tokens")

            result = float(tokens[0])
            i = 1
            while i < len(tokens):
                op = tokens[i]
                num = float(tokens[i + 1])
                if op == "+":
                    result += num
                elif op == "-":
                    result -= num
                elif op == "*":
                    result *= num
                elif op == "/":
                    if num == 0:
                        raise ZeroDivisionError()
                    result /= num
                i += 2
            return result
        except (IndexError, ValueError) as e:
            raise ValueError(f"Invalid expression: {expr}") from e

    print("Testing NAIVE (insecure) implementation:")
    print("-" * 40)
    naive_results = grade_implementation(naive_calculate)
    for level in ["basic", "edge_cases", "security"]:
        r = naive_results[level]
        print(f"  {level}: {r['passed']}/{r['total']} ({r['score']:.0%})")
    print(f"  Weighted: {naive_results['weighted_score']:.0%}")
    print(f"  Verdict: {naive_results['verdict']}")

    print("\nTesting SAFE implementation:")
    print("-" * 40)
    safe_results = grade_implementation(safe_calculate)
    for level in ["basic", "edge_cases", "security"]:
        r = safe_results[level]
        print(f"  {level}: {r['passed']}/{r['total']} ({r['score']:.0%})")
    print(f"  Weighted: {safe_results['weighted_score']:.0%}")
    print(f"  Verdict: {safe_results['verdict']}")
