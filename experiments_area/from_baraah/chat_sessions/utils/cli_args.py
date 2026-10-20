import re


def parse_args(argv: list[str]) -> tuple[str | None, str | None]:
    """Return an optional session name and question from command-line args."""
    args = argv[1:]

    if not args:
        return None, None

    if len(args) > 2:
        raise SystemExit("Error: provide a question, or a session name and question.")

    question = args[-1].strip()
    if not question:
        raise SystemExit("Error: question cannot be blank.")

    session_name = None
    if len(args) == 2:
        session_name = args[0].strip()
        if not session_name:
            raise SystemExit("Error: session name cannot be blank.")

    return session_name, question


def clean_session_name(raw: str) -> str:
    """Return the first two words as a lowercase underscore-separated name."""
    words = re.findall(r"[^\W_]+", raw.lower())
    if len(words) < 2:
        return "new_session"
    return "_".join(words[:2])


def is_exit_word(text: str) -> bool:
    """Return whether text is exactly ``exit`` or ``quit``."""
    return text.strip().lower() in ("exit", "quit")
