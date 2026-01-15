"""Ralph Iteration Effect Experiment Implementation."""

import time
from typing import Any

import anthropic
from pydantic import BaseModel


class TaskResult(BaseModel):
    """Result from a single task execution."""

    code: str
    iterations_used: int
    tokens_total: int
    duration_ms: int
    completed: bool


TASK_PROMPT = """Write a Python function called `is_palindrome` that checks if a string is a valid palindrome.

Requirements:
- Ignore case (treat 'A' and 'a' as equal)
- Ignore non-alphanumeric characters (spaces, punctuation, etc.)
- Return True if palindrome, False otherwise

Examples:
- is_palindrome("A man, a plan, a canal: Panama") -> True
- is_palindrome("race a car") -> False
- is_palindrome("Was it a car or a cat I saw?") -> True
- is_palindrome("") -> True

Return ONLY the Python function, no explanation."""


REVIEW_PROMPT = """Review the following code for the palindrome task.

Task requirements:
- Function named `is_palindrome`
- Ignores case
- Ignores non-alphanumeric characters
- Returns True/False

Code to review:
```python
{code}
```

If the code is correct and complete, respond with exactly: COMPLETE

If there are issues, provide the corrected code only (no explanation)."""


TEST_CASES = [
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


def extract_code(response: str) -> str:
    """Extract Python code from response."""
    # Handle markdown code blocks
    if "```python" in response:
        start = response.find("```python") + 9
        end = response.find("```", start)
        if end > start:
            return response[start:end].strip()
    if "```" in response:
        start = response.find("```") + 3
        end = response.find("```", start)
        if end > start:
            return response[start:end].strip()
    # Assume raw code
    return response.strip()


def test_code(code: str) -> tuple[bool, int, int]:
    """Test the code against test cases. Returns (all_pass, passed, total)."""
    try:
        # Create isolated namespace
        namespace = {}
        exec(code, namespace)

        if "is_palindrome" not in namespace:
            return False, 0, len(TEST_CASES)

        func = namespace["is_palindrome"]
        passed = 0

        for input_str, expected in TEST_CASES:
            try:
                result = func(input_str)
                if result == expected:
                    passed += 1
            except Exception:
                pass

        return passed == len(TEST_CASES), passed, len(TEST_CASES)

    except Exception:
        return False, 0, len(TEST_CASES)


class RalphExperiment:
    """Run the Ralph iteration effect experiment."""

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        self.model = model
        self.client = anthropic.Anthropic()

    def run_single(self) -> TaskResult:
        """Run single iteration (control)."""
        start = time.time()

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": TASK_PROMPT}]
        )

        code = extract_code(response.content[0].text)
        tokens = response.usage.input_tokens + response.usage.output_tokens
        all_pass, _, _ = test_code(code)

        duration = int((time.time() - start) * 1000)

        return TaskResult(
            code=code,
            iterations_used=1,
            tokens_total=tokens,
            duration_ms=duration,
            completed=all_pass,
        )

    def run_ralph(self, max_iterations: int) -> TaskResult:
        """Run Ralph-style iteration."""
        start = time.time()
        total_tokens = 0

        # Initial generation
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": TASK_PROMPT}]
        )

        code = extract_code(response.content[0].text)
        total_tokens += response.usage.input_tokens + response.usage.output_tokens
        iterations = 1

        # Check if already correct
        all_pass, _, _ = test_code(code)
        if all_pass:
            duration = int((time.time() - start) * 1000)
            return TaskResult(
                code=code,
                iterations_used=iterations,
                tokens_total=total_tokens,
                duration_ms=duration,
                completed=True,
            )

        # Iterate with self-review
        for i in range(max_iterations - 1):
            review_prompt = REVIEW_PROMPT.format(code=code)

            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": review_prompt}]
            )

            total_tokens += response.usage.input_tokens + response.usage.output_tokens
            iterations += 1

            response_text = response.content[0].text.strip()

            # Check for completion signal
            if response_text == "COMPLETE":
                break

            # Extract new code
            new_code = extract_code(response_text)
            if new_code:
                code = new_code

            # Check if now correct
            all_pass, _, _ = test_code(code)
            if all_pass:
                break

        duration = int((time.time() - start) * 1000)
        all_pass, _, _ = test_code(code)

        return TaskResult(
            code=code,
            iterations_used=iterations,
            tokens_total=total_tokens,
            duration_ms=duration,
            completed=all_pass,
        )
