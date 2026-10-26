def parse_args(argv: list[str]) -> tuple[str | None, str | None]:
    """Return the session name and the question from the command-line arguments."""
    args = argv[1:]

    if not args:
        return None, None

    if len(args) > 2:
        raise SystemExit("Error: pass a question, or a session name and a question.")

    question = args[-1].strip()

    if not question:
        raise SystemExit("Error: the question cannot be empty.")

    if len(args) == 1:
        return None, question

    session_name = args[0].strip()

    if not session_name:
        raise SystemExit("Error: the session name cannot be empty.")

    return session_name, question


def clean_session_name(raw: str) -> str:
    """Turn the model's naming reply into a two-word session name."""
    cleaned = "".join(char if char.isalnum() else " " for char in raw.lower())
    words = cleaned.split()[:2]

    if len(words) < 2:
        return "new_session"

    return "_".join(words)


def is_exit_word(text: str) -> bool:
    """Check whether the user wants to end the chat."""
    return text.strip().lower() in ("exit", "quit")
