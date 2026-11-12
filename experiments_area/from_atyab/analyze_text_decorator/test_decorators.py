"""Tests for the analyze_text decorator."""

import pytest

from decorators import analyze_text


def test_all_metrics_for_hello_alice(capsys: pytest.CaptureFixture[str]) -> None:
    @analyze_text(words=True, vowels=True, spaces=True)
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    assert greet("Alice") == "Hello, Alice!"
    assert capsys.readouterr().out == "Words: 2\nVowels: 5\nSpaces: 1\n"


def test_no_metrics_prints_nothing(capsys: pytest.CaptureFixture[str]) -> None:
    @analyze_text()
    def greet() -> str:
        return "Hello"

    assert greet() == "Hello"
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize(
    ("kwargs", "expected"),
    [
        ({"words": True}, "Words: 3\n"),
        ({"vowels": True}, "Vowels: 5\n"),
        ({"spaces": True}, "Spaces: 2\n"),
    ],
)
def test_single_metric(
    kwargs: dict[str, bool],
    expected: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    @analyze_text(**kwargs)
    def message() -> str:
        return "one two three"

    assert message() == "one two three"
    assert capsys.readouterr().out == expected


def test_empty_string(capsys: pytest.CaptureFixture[str]) -> None:
    @analyze_text(words=True, vowels=True, spaces=True)
    def empty() -> str:
        return ""

    assert empty() == ""
    assert capsys.readouterr().out == "Words: 0\nVowels: 0\nSpaces: 0\n"


def test_punctuation_and_non_ascii(capsys: pytest.CaptureFixture[str]) -> None:
    @analyze_text(words=True, vowels=True, spaces=True)
    def phrase() -> str:
        return "Héllo, Alice!"

    assert phrase() == "Héllo, Alice!"
    assert capsys.readouterr().out == "Words: 2\nVowels: 4\nSpaces: 1\n"


def test_multiline_and_tabs(capsys: pytest.CaptureFixture[str]) -> None:
    @analyze_text(words=True, vowels=True, spaces=True)
    def text() -> str:
        return "one two\nthree\tfour"

    assert text() == "one two\nthree\tfour"
    assert capsys.readouterr().out == "Words: 4\nVowels: 7\nSpaces: 1\n"


def test_spaces_counts_only_space_characters(
    capsys: pytest.CaptureFixture[str],
) -> None:
    @analyze_text(spaces=True)
    def text() -> str:
        return "a b\tc\nd"

    assert text() == "a b\tc\nd"
    assert capsys.readouterr().out == "Spaces: 1\n"


def test_vowels_are_case_insensitive(capsys: pytest.CaptureFixture[str]) -> None:
    @analyze_text(vowels=True)
    def text() -> str:
        return "AEIOU aeiou"

    assert text() == "AEIOU aeiou"
    assert capsys.readouterr().out == "Vowels: 10\n"


def test_forwards_arguments_and_preserves_metadata(
    capsys: pytest.CaptureFixture[str],
) -> None:
    @analyze_text(words=True)
    def surround(text: str, prefix: str = "", suffix: str = "") -> str:
        """Wrap text."""
        return f"{prefix}{text}{suffix}"

    assert surround("Hi", prefix="<", suffix=">") == "<Hi>"
    assert capsys.readouterr().out == "Words: 1\n"
    assert surround.__name__ == "surround"
    assert surround.__doc__ == "Wrap text."
