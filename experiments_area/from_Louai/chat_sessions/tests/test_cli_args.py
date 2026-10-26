import pytest

from utils.cli_args import clean_session_name, is_exit_word, parse_args


@pytest.mark.parametrize(
    "argv, expected",
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
    assert parse_args(argv) == expected


def test_no_arguments_means_interactive():
    assert parse_args(["app.py"]) == (None, None)


def test_too_many_arguments():
    with pytest.raises(SystemExit, match="Error"):
        parse_args(["app.py", "a", "b", "c"])


def test_blank_question():
    with pytest.raises(SystemExit, match="Error"):
        parse_args(["app.py", "   "])


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("Oman Capital", "oman_capital"),
        ("oman capital city", "oman_capital"),
        ("", "new_session"),
    ],
)
def test_clean_session_name(raw, expected):
    assert clean_session_name(raw) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("  QUIT ", True),
        ("hello", False),
        ("exit", True),
        ("EXIT", True),
    ],
)
def test_is_exit_word(text, expected):
    assert is_exit_word(text) == expected
