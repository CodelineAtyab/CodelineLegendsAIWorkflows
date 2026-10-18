"""Unit tests for utils.non_interactive_example.ask_ai."""

import pytest

from utils.non_interactive_example import ask_ai


@pytest.mark.parametrize(
    ("msg", "expected"),
    [
        ("", ""),
        (None, None),
        ("This is a question", "Hey! This is your message: This is a question"),
    ],
)
def test_ask_ai_echoes_text(msg, expected):
    """Non-numeric input is echoed back, with None and '' passed through."""
    assert ask_ai(msg) == expected


@pytest.mark.parametrize("number", [2, 3.5])
def test_ask_ai_rejects_numbers(number):
    """Numeric input raises TypeError instead of being echoed."""
    with pytest.raises(TypeError, match="Numbers are not allowed"):
        ask_ai(number)
