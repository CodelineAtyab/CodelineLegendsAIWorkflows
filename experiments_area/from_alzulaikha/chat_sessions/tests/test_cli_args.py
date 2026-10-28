"""Unit tests for utils.cli_args."""

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
def test_parse_args(argv: list[str], expected: tuple[str | None, str | None]) -> None:
    """Recognize interactive, new-session and resumed-session arguments."""
    assert parse_args(argv) == expected


@pytest.mark.parametrize(
    "argv",
    [
        ["app.py", "a", "b", "c"],
        ["app.py", "   "],
        ["app.py", "oman_capital", "   "],
        ["app.py", "   ", "Hi there"],
    ],
)
def test_parse_args_rejects_bad_arguments(argv: list[str]) -> None:
    """Reject too many arguments, a blank question and a blank session name."""
    with pytest.raises(SystemExit, match="Error:"):
        parse_args(argv)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Oman Capital", "oman_capital"),
        ("oman capital city", "oman_capital"),
        ("", "new_session"),
        ("Oman_Capital", "oman_capital"),
        ("Oman", "new_session"),
    ],
)
def test_clean_session_name(raw: str, expected: str) -> None:
    """Turn a model answer into a short file name."""
    assert clean_session_name(raw) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("  QUIT ", True),
        ("hello", False),
        ("exit", True),
        ("EXIT", True),
        (" quit ", True),
        ("exit now", False),
    ],
)
def test_is_exit_word(text: str, expected: bool) -> None:
    """Recognize only exit and quit after removing outer spaces."""
    assert is_exit_word(text) is expected
