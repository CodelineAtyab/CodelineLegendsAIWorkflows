import pytest

from app import clean_session_name, is_exit_word, parse_args


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        ([], (None, None)),
        (["What is the capital of Oman?"], (None, "What is the capital of Oman?")),
        (
            ["oman_capital", "And its population?"],
            ("oman_capital", "And its population?"),
        ),
        (["  spaced question  "], (None, "spaced question")),
    ],
)
def test_parse_args(
    args: list[str],
    expected: tuple[str | None, str | None],
) -> None:
    """Test valid command-line arguments."""
    assert parse_args(args) == expected


@pytest.mark.parametrize(
    "args",
    [
        ["one", "two", "three"],
        ["   "],
        ["oman_capital", "   "],
        [""],
        ["oman_capital", ""],
        ["", "Hello"],
        ["   ", "Hello"],
    ],
)
def test_parse_args_invalid(args: list[str]) -> None:
    """Test invalid command-line arguments."""
    with pytest.raises(SystemExit, match="Error:"):
        parse_args(args)


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Oman Capital", "oman_capital"),
        ("oman capital city", "oman_capital"),
        ("", "new_session"),
        ("   ", "new_session"),
        ("OneWord", "new_session"),
    ],
)
def test_clean_session_name(name: str, expected: str) -> None:
    """Test cleaning the session name suggested by the AI."""
    assert clean_session_name(name) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
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
