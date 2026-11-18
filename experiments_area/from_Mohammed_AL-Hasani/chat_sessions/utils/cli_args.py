def parse_args(argv: list[str]) -> tuple[str | None, str | None]:
    """Return the session name and question from command-line arguments."""
    args = argv[1:]

    if len(args) > 2:
        raise SystemExit("Error: Too many arguments.")

    if not args:
        return None, None

    if len(args) == 1:
        question = args[0].strip()

        if not question:
            raise SystemExit("Error: Question cannot be blank.")

        return None, question

    session_name = args[0].strip()
    question = args[1].strip()

    if not session_name:
        raise SystemExit("Error: Session name cannot be blank.")

    if not question:
        raise SystemExit("Error: Question cannot be blank.")

    return session_name, question


def clean_session_name(raw: str) -> str:
    """Convert text into a simple lowercase session name."""
    words = raw.strip().lower().split()[:2]

    if not words:
        return "new_session"

    return "_".join(words)


def is_exit_word(text: str) -> bool:
    """Check whether the user wants to exit the chat."""
    return text.strip().lower() in ("exit", "quit")
