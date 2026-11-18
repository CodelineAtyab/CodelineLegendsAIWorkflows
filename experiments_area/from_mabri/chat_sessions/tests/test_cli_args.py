"""Unit tests for utils.cli_args (no OpenAI calls, no network)."""

import pytest

from utils.cli_args import clean_session_name, is_exit_word, parse_args


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


@pytest.mark.parametrize(
    "argv",
    [
        ["app.py", "a", "b", "c"],
        ["app.py", "   "],
    ],
)
def test_parse_args_rejects_bad_input(argv):
    """Too many arguments or empty question raises SystemExit."""
    with pytest.raises(SystemExit, match="Error"):
        parse_args(argv)


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["app.py", "   Hi there   "], (None, "Hi there")),
        (
            ["app.py", "oman_capital", "   And its population?   "],
            ("oman_capital", "And its population?"),
        ),
    ],
)
def test_parse_args_strips_question(argv, expected):
    """Leading/trailing whitespace is stripped from the question."""
    assert parse_args(argv) == expected


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Oman Capital", "oman_capital"),
        ("oman capital city", "oman_capital"),
        ("", "new_session"),
    ],
)
def test_clean_session_name(raw, expected):
    """The model's reply becomes two lower-case words joined by '_', or the fallback."""
    assert clean_session_name(raw) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("exit", True),
        ("quit", True),
        ("  Exit  ", True),
        ("  QUIT ", True),
        ("hello", False),
        ("exiting", False),
    ],
)
def test_is_exit_word(text, expected):
    """is_exit_word returns True for exit commands, False otherwise."""
    assert is_exit_word(text) == expected
