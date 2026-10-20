import pytest

from utils import cli_args


@pytest.mark.parametrize(
    "argv, expected",
    [
        (['app.py'], (None, None)),
        (['app.py', 'Hi there'], (None, 'Hi there')),
        (['app.py', 'oman_capital', 'And its population?'], ('oman_capital', 'And its population?')),
    ]
)
def test_parse_args_valid(argv, expected):
    assert cli_args.parse_args(argv) == expected

@pytest.mark.parametrize(
    "argv",
    [
        ['app.py', 'oman_capital', 'And its population?', 'extra'],
        ['app.py', ''],
        ['app.py', '   '],
        ['app.py', 'oman_capital', '   '],
    ]
)
def test_parse_args_errors(argv):
    with pytest.raises(SystemExit, match="Error"):
        cli_args.parse_args(argv)

@pytest.mark.parametrize(
    "raw, expected",
    [
        ("Oman Capital", "oman_capital"),
        ("oman capital city", "oman_capital"),
        ("", "new_session"),
        ("   ", "new_session"),
        ("Single", "single"),
    ]
)
def test_clean_session_name(raw, expected):
    assert cli_args.clean_session_name(raw) == expected

@pytest.mark.parametrize(
    "text, expected",
    [
        ("exit", True),
        ("Exit", True),
        ("QUIT", True),
        (" quit ", True),
        ("no", False),
        ("continue", False),
        ("", False),
    ]
)
def test_is_exit_word(text, expected):
    assert cli_args.is_exit_word(text) == expected
