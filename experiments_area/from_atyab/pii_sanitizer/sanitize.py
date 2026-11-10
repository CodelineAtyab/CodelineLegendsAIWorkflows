"""Mask PII in chat logs without loading the whole file into memory."""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterator, Sequence
from pathlib import Path

# Keep the domain so support staff can still tell providers apart.
EMAIL_PATTERN = re.compile(r"[\w.-]+@[\w.-]+\.[A-Za-z]{2,}")
# International-ish numbers: at least nine digits, optional separators.
PHONE_PATTERN = re.compile(r"\+?\d[\d\s\-()]{7,}\d")
# 12-16 digit card-like runs, optionally separated by spaces or dashes.
CARD_PATTERN = re.compile(r"\b\d{4}(?:[\s-]?\d{4}){2,3}\b")
DIGIT_PATTERN = re.compile(r"\d")


def read_lines(path: str | Path) -> Iterator[str]:
    """Yield the file line by line so memory use stays constant."""
    with open(path, encoding="utf-8") as handle:
        yield from handle


def mask_digits(value: str) -> str:
    """Replace every digit in ``value`` with ``*``."""
    return DIGIT_PATTERN.sub("*", value)


def mask_email(match: re.Match[str]) -> str:
    """Keep the domain and replace the whole local part with ``***``."""
    _, separator, domain = match.group(0).partition("@")
    if not separator:
        return match.group(0)
    return f"***@{domain}"


def mask_line(line: str) -> str:
    """Mask cards, phones, and emails in a single line of text.

    Cards are masked first so the broader phone pattern cannot swallow them.
    """
    masked = CARD_PATTERN.sub(lambda match: mask_digits(match.group(0)), line)
    masked = PHONE_PATTERN.sub(lambda match: mask_digits(match.group(0)), masked)
    return EMAIL_PATTERN.sub(mask_email, masked)


def sanitize_file(input_path: str | Path, output_path: str | Path) -> int:
    """Write a masked copy of ``input_path`` to ``output_path``.

    Returns the number of lines processed.
    """
    source = Path(input_path)
    if not source.is_file():
        raise FileNotFoundError(source)

    line_count = 0
    with open(output_path, "w", encoding="utf-8") as output:
        for line in read_lines(source):
            output.write(mask_line(line))
            line_count += 1
    return line_count


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        description="Mask emails, phone numbers, and card numbers in a text file."
    )
    parser.add_argument("--input", required=True, type=Path, help="file to read")
    parser.add_argument("--output", required=True, type=Path, help="file to write")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the sanitizer and return a process exit code."""
    args = build_parser().parse_args(argv)
    try:
        line_count = sanitize_file(args.input, args.output)
    except FileNotFoundError:
        print(f"Error: input file not found: {args.input}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    print(f"Sanitized {line_count} line(s) into {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
