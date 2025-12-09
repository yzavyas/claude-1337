# claude-1337 Evals

Evaluation framework for testing skill effectiveness.

## Setup

```bash
cd evals
uv sync
```

## Running Tests

```bash
# All tests
uv run pytest

# Just trigger tests
uv run pytest tests/test_triggers.py

# Just content tests
uv run pytest tests/test_content.py

# Verbose output
uv run pytest -v
```

## Test Types

### Trigger Tests (`test_triggers.py`)

Tests whether skill descriptions contain the right keywords to trigger activation.

- Asks Claude: "Would this skill be relevant for this task?"
- Validates YES for related tasks, NO for unrelated

### Content Tests (`test_content.py`)

Tests whether skills provide correct, specific information.

- Loads skill content as system prompt
- Asks domain questions
- Validates expected keywords in response

## Adding Tests

Add test cases to the `*_CASES` lists in each test file:

```python
RUST_TRIGGER_CASES = [
    ("What HTTP server should I use in Rust?", "rust-1337", True),
    # (prompt, skill_name, should_trigger)
]
```

## Research Background

Based on:
- [Scott Spence's 200+ test study](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably) - 20% baseline ’ 84% with forced eval
- [Anthropic's eval-driven development](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## Cost

Tests use Claude API. Each test case = 1 API call.
- Trigger tests: ~10 tokens/call
- Content tests: ~200 tokens/call
