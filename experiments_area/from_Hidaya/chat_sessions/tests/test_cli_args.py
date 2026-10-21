import pytest

from utils.cli_args import clean_session_name, is_exit_word, parse_args


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["app.py"], (None, None)),
        (["app.py", "Hello"], (None, "Hello")),
        (["app.py", "Hi there"], (None, "Hi there")),
        (
            ["app.py", "What is the capital of Oman?"],
            (None, "What is the capital of Oman?"),
        ),
        (["app.py", "  spaced question  "], (None, "spaced question")),
        (
            ["app.py", "oman_capital", "Tell me more"],
            ("oman_capital", "Tell me more"),
        ),
        (
            ["app.py", "oman_capital", "And its population?"],
            ("oman_capital", "And its population?"),
        ),
    ],
)
def test_parse_args(
    argv: list[str],
    expected: tuple[str | None, str | None],
) -> None:
    """Test valid command-line arguments."""
    assert parse_args(argv) == expected


@pytest.mark.parametrize(
    "argv",
    [
        ["app.py", "a", "b", "c"],
        ["app.py", "one", "two", "three"],
        ["app.py", "   "],
        ["app.py", ""],
        ["app.py", "oman_capital", "   "],
        ["app.py", "oman_capital", ""],
        ["app.py", "", "Hello"],
        ["app.py", "   ", "Hello"],
    ],
)
def test_parse_args_invalid(argv: list[str]) -> None:
    """Test invalid command-line arguments."""
    with pytest.raises(SystemExit, match="Error:"):
        parse_args(argv)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Oman Capital", "oman_capital"),
        ("oman capital city", "oman_capital"),
        ("", "new_session"),
        ("   ", "new_session"),
        ("OneWord", "new_session"),
        ("Oman_Capital", "oman_capital"),
        ("Oman Capital 2024", "oman_capital"),
    ],
)
def test_clean_session_name(raw: str, expected: str) -> None:
    """Test cleaning the session name suggested by the AI."""
    assert clean_session_name(raw) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("  QUIT ", True),
        ("exit", True),
        ("EXIT", True),
        ("  quit ", True),
        ("hello", False),
        ("exit now", False),
        ("", False),
    ],
)
def test_is_exit_word(text: str, expected: bool) -> None:
    """Test the words that end the chat."""
    assert is_exit_word(text) is expected
