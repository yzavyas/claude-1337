"""Test skill content quality - does the skill provide correct information?

These tests verify that skills provide accurate, specific information
that Claude wouldn't know from training alone.
"""

import pytest


# Test cases: (question, skill_content_fixture, expected_keywords)
RUST_CONTENT_CASES = [
    (
        "What's the string ownership rule?",
        ["95%", "String", "&str", "Cow"],
    ),
    (
        "What HTTP server should I use?",
        ["axum"],
    ),
    (
        "What's wrong with lazy_static?",
        ["LazyLock", "deprecated", "1.80"],
    ),
    (
        "How do I handle errors in a library?",
        ["thiserror"],
    ),
    (
        "How do I handle errors in an application?",
        ["anyhow"],
    ),
    (
        "What's the danger with mutex in async?",
        ["await", "deadlock", "drop"],
    ),
]

TERMINAL_CONTENT_CASES = [
    (
        "What should I use instead of grep?",
        ["rg", "ripgrep"],
    ),
    (
        "What should I use instead of find?",
        ["fd"],
    ),
    (
        "What should I use instead of cat?",
        ["bat"],
    ),
    (
        "What should I use instead of curl?",
        ["xh"],
    ),
]


def get_skill_answer(client, question: str, skill_content: str) -> str:
    """Ask Claude a question with skill content loaded."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        system=f"You have access to this skill:\n\n{skill_content}\n\nUse it to answer questions.",
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
    )
    return response.content[0].text


@pytest.mark.parametrize("question,expected_keywords", RUST_CONTENT_CASES)
def test_rust_content(client, rust_skill_content, question, expected_keywords):
    """Test rust-1337 provides correct information."""
    answer = get_skill_answer(client, question, rust_skill_content)
    answer_lower = answer.lower()

    for keyword in expected_keywords:
        assert keyword.lower() in answer_lower, (
            f"Expected '{keyword}' in answer to '{question}'\n"
            f"Got: {answer}"
        )


@pytest.mark.parametrize("question,expected_keywords", TERMINAL_CONTENT_CASES)
def test_terminal_content(client, terminal_skill_content, question, expected_keywords):
    """Test terminal-1337 provides correct information."""
    answer = get_skill_answer(client, question, terminal_skill_content)
    answer_lower = answer.lower()

    for keyword in expected_keywords:
        assert keyword.lower() in answer_lower, (
            f"Expected '{keyword}' in answer to '{question}'\n"
            f"Got: {answer}"
        )
