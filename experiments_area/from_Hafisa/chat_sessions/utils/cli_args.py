def parse_args(argv: list[str]) -> tuple[str | None, str | None]:
    """Return the session name and question represented by command-line arguments."""
    arguments = argv[1:]

    if len(arguments) == 0:
        return None, None

    if len(arguments) > 2:
        raise SystemExit("Error: expected a question or a session name and question.")

    if not arguments[-1].strip():
        raise SystemExit("Error: question cannot be blank.")

    if len(arguments) == 1:
        return None, arguments[0]

    return arguments[0], arguments[1]


def clean_session_name(raw: str) -> str:
    """Convert a model naming reply into a short session filename."""
    words = [word.strip(".,!?;:\"'").lower() for word in raw.split()]
    words = [word for word in words if word]

    if not words:
        return "new_session"

    if len(words) == 1:
        words.append("session")

    return "_".join(words[:2])


def is_exit_word(text: str) -> bool:
    """Return whether text asks the chat loop to stop."""
    return text.strip().lower() in {"exit", "quit"}
