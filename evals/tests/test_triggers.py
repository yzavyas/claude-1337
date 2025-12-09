"""Test skill triggering - does Claude activate skills for relevant prompts?

These tests verify that skill descriptions contain the right keywords
to trigger activation. We test by asking Claude if a skill would be
relevant for a given task.
"""

import pytest


# Test cases: (prompt, expected_skill, should_trigger)
RUST_TRIGGER_CASES = [
    ("What HTTP server should I use in Rust?", "rust-1337", True),
    ("How do I handle errors in a Rust CLI?", "rust-1337", True),
    ("What's the best way to do async in Rust?", "rust-1337", True),
    ("Help me build a Tauri app", "rust-1337", True),
    ("What's the 95% rule for String ownership?", "rust-1337", True),
    ("Write me a Python script", "rust-1337", False),
    ("How do I use React hooks?", "rust-1337", False),
]

TERMINAL_TRIGGER_CASES = [
    ("Search for TODO comments in my code", "terminal-1337", True),
    ("Find all TypeScript files", "terminal-1337", True),
    ("Show me the contents of config.json", "terminal-1337", True),
    ("List files in this directory", "terminal-1337", True),
    ("Test this API endpoint", "terminal-1337", True),
    ("Write a Rust function", "terminal-1337", False),
    ("Explain this algorithm", "terminal-1337", False),
]


def skill_would_trigger(client, prompt: str, skill_description: str) -> bool:
    """Ask Claude if a skill would be relevant for a prompt."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=10,
        messages=[
            {
                "role": "user",
                "content": f"""Given this skill description:
---
{skill_description}
---

Would this skill be relevant for the following task? Answer only YES or NO.

Task: {prompt}""",
            }
        ],
    )
    answer = response.content[0].text.strip().upper()
    return answer == "YES"


@pytest.mark.parametrize("prompt,skill,should_trigger", RUST_TRIGGER_CASES)
def test_rust_triggers(client, rust_skill_content, prompt, skill, should_trigger):
    """Test rust-1337 triggers on Rust-related prompts."""
    # Extract just the description from SKILL.md
    lines = rust_skill_content.split("\n")
    for line in lines:
        if line.startswith("description:"):
            description = line.replace("description:", "").strip().strip('"')
            break

    triggered = skill_would_trigger(client, prompt, description)

    if should_trigger:
        assert triggered, f"Expected {skill} to trigger for: {prompt}"
    else:
        assert not triggered, f"Expected {skill} NOT to trigger for: {prompt}"


@pytest.mark.parametrize("prompt,skill,should_trigger", TERMINAL_TRIGGER_CASES)
def test_terminal_triggers(client, terminal_skill_content, prompt, skill, should_trigger):
    """Test terminal-1337 triggers on CLI-related prompts."""
    # Extract just the description from SKILL.md
    lines = terminal_skill_content.split("\n")
    for line in lines:
        if line.startswith("description:"):
            description = line.replace("description:", "").strip().strip('"')
            break

    triggered = skill_would_trigger(client, prompt, description)

    if should_trigger:
        assert triggered, f"Expected {skill} to trigger for: {prompt}"
    else:
        assert not triggered, f"Expected {skill} NOT to trigger for: {prompt}"
