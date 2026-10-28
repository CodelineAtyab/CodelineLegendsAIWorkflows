import re


def parse_args(argv: list[str]) -> tuple[str | None, str | None]:
    """Return the session name and question from the supplied argument list."""
    args = argv[1:]

    if not args:
        return None, None

    if len(args) > 2:
        raise SystemExit("Error: give a question, or a session name and a question.")

    question = args[-1].strip()

    if not question:
        raise SystemExit("Error: question cannot be blank.")

    session_name: str | None = None

    if len(args) == 2:
        session_name = args[0].strip()

        if not session_name:
            raise SystemExit("Error: session name cannot be blank.")

    return session_name, question


def clean_session_name(raw: str) -> str:
    """Return two lowercase words joined by an underscore, or new_session."""
    words = re.findall(r"[^\W_]+", raw.lower())

    if len(words) < 2:
        return "new_session"

    return "_".join(words[:2])


def is_exit_word(text: str) -> bool:
    """Recognize exit and quit regardless of capitalization or outer spaces."""
    return text.strip().lower() in ("exit", "quit")
