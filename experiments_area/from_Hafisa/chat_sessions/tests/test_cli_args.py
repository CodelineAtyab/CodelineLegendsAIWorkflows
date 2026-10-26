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
def test_parse_args(argv, expected):
    assert parse_args(argv) == expected


@pytest.mark.parametrize(
    "argv",
    [
        ["app.py", "a", "b", "c"],
        ["app.py", " "],
    ],
)
def test_parse_args_rejects_invalid_arguments(argv):
    with pytest.raises(SystemExit, match="Error"):
        parse_args(argv)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Oman Capital", "oman_capital"),
        ("oman capital city", "oman_capital"),
        ("", "new_session"),
    ],
)
def test_clean_session_name(raw, expected):
    assert clean_session_name(raw) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [(" QUIT ", True), ("hello", False)],
)
def test_is_exit_word(text, expected):
    assert is_exit_word(text) is expected
