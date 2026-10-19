"""Unit tests for utils.cli_args (no OpenAI calls, no network)."""

import pytest

from utils.cli_args import parse_args


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["app.py"], (None, None)),
        (["app.py", "Hi there"], (None, "Hi there")),
        (
            ["app.py", "oman_capital", "And its population?"],
            ("oman_capital", "And its population?"),
        ),
    ],
)
def test_parse_args_valid(argv, expected):
    """0, 1 or 2 arguments give interactive, new-session or resume mode."""
    assert parse_args(argv) == expected
