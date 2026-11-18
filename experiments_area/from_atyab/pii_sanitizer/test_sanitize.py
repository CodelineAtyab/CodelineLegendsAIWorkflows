"""Tests for the PII sanitizer."""

from pathlib import Path

import pytest

from sanitize import main, mask_line, read_lines, sanitize_file


def test_email_local_part_is_masked() -> None:
    assert mask_line("john.doe@example.com") == "***@example.com"


def test_phone_digits_are_masked() -> None:
    assert mask_line("Call +1 (555) 123-4567") == "Call +* (***) ***-****"


def test_card_digits_are_masked() -> None:
    assert mask_line("4111 1111 1111 1111") == "**** **** **** ****"


def test_file_round_trip_keeps_line_count(tmp_path: Path) -> None:
    source = tmp_path / "sample.txt"
    source.write_text("a@b.com\ncall 1234567890\n", encoding="utf-8")
    target = tmp_path / "cleaned.txt"

    assert sanitize_file(source, target) == 2
    assert target.read_text(encoding="utf-8") == "***@b.com\ncall **********\n"


def test_read_lines_is_lazy(tmp_path: Path) -> None:
    source = tmp_path / "three.txt"
    source.write_text("one\ntwo\nthree\n", encoding="utf-8")

    lines = read_lines(source)

    assert next(lines) == "one\n"
    assert list(lines) == ["two\n", "three\n"]


def test_missing_input_returns_exit_code_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = main(
        [
            "--input",
            str(tmp_path / "missing.txt"),
            "--output",
            str(tmp_path / "cleaned.txt"),
        ]
    )

    assert exit_code == 1
    assert "input file not found" in capsys.readouterr().err
