import pytest

from utils.cli_args import clean_session_name, is_exit_word, parse_args


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["app.py"], (None, None)),
        (
            ["app.py", "What is the capital of Oman?"],
            (
                None,
                "What is the capital of Oman?",
            ),
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
        ["app.py", "one", "two", "three"],
        ["app.py", "   "],
        ["app.py", "oman_capital", "   "],
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
    ],
)
def test_clean_session_name(raw: str, expected: str) -> None:
    """Test cleaning session names."""
    assert clean_session_name(raw) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("exit", True),
        ("  QUIT ", True),
        ("hello", False),
        ("", False),
    ],
)
def test_is_exit_word(text: str, expected: bool) -> None:
    """Test exit commands."""
    assert is_exit_word(text) is expected
