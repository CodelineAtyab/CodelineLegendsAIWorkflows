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
    """Check interactive, single-question, and resumed-session arguments."""
    assert parse_args(argv) == expected


@pytest.mark.parametrize(
    "argv",
    [
        ["app.py", "one", "two", "three"],
        ["app.py", "   "],
        ["app.py", "oman_capital", "   "],
        ["app.py", "   ", "Hi there"],
    ],
)
def test_parse_args_invalid(argv: list[str]) -> None:
    """Ensure invalid args raise SystemExit with clear Error messages."""
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
    """Check normalization into two lowercase words or fallback."""
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
    """Check recognition of quit/exit words regardless of casing."""
    assert is_exit_word(text) is expected
