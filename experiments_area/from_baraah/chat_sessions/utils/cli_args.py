
import re


def parse_args(argv: list[str]) -> tuple[str | None, str | None]:
    """Return the session name and question from command-line arguments."""
    args = argv[1:]

    if not args:
        return None, None

    if len(args) > 2:
        raise SystemExit("Error: Too many arguments.")

    question = args[-1].strip()

    if not question:
        raise SystemExit("Error: Question cannot be blank.")

    session_name = None

    if len(args) == 2:
        session_name = args[0].strip()

        if not session_name:
            raise SystemExit("Error: Session name cannot be blank.")

    return session_name, question


def clean_session_name(raw: str) -> str:
    """Convert the first two words into a session name."""
    words = re.findall(r"[^\W_]+", raw.lower())

    if not words:
        return "new_session"

    return "_".join(words[:2])


def is_exit_word(text: str) -> bool:
    """Check whether the user typed exit or quit."""
    return text.strip().lower() in ("exit", "quit")
