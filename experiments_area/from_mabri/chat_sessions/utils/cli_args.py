"""Argument parsing and name helpers for app.py; tests live in tests/test_cli_args.py."""

FALLBACK_SESSION_NAME = "new_session"
EXIT_COMMANDS = ("exit", "quit")


def is_exit_word(text: str) -> bool:
    """Return True if the text is an exit command."""
    return text.strip().lower() in EXIT_COMMANDS


def clean_session_name(raw_name: str) -> str:
    """Turn the model's reply into exactly two lower-case words joined by '_'."""
    without_apostrophes = raw_name.lower().replace("'", "").replace("’", "")
    letters_only = "".join(
        char if char.isascii() and char.isalnum() else " "
        for char in without_apostrophes
    )
    words = letters_only.split()[:2]
    if not words:
        return FALLBACK_SESSION_NAME
    return "_".join(words)


def parse_args(argv: list[str]) -> tuple[str | None, str | None]:
    """Return (session_name, question) from argv; (None, None) means interactive mode."""
    args = argv[1:]
    if len(args) > 2:
        raise SystemExit(
            'Error: too many arguments. Usage: app.py [session_name] "question"'
        )
    if len(args) == 0:
        return (None, None)

    if len(args) == 1:
        session_name, question = None, args[0]
    else:
        session_name, question = args[0], args[1]

    if question.strip() == "":
        raise SystemExit("Error: Invalid empty question.")
    return (session_name, question.strip())
