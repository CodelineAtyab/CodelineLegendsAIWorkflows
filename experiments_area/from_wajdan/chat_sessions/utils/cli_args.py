import re


def parse_args(argv: list[str]) -> tuple[str | None, str | None]:
    """Parse command-line session and question arguments."""
    arguments = argv[1:]
    if len(arguments) > 2:
        raise SystemExit("Error: expected a question and optional session name.")
    if not arguments:
        return None, None
    if len(arguments) == 1:
        question = arguments[0].strip()
        if not question.strip():
            raise SystemExit("Error: question cannot be blank.")
        return None, question
    session_name = arguments[0].strip()
    question = arguments[1].strip()
    if not session_name:
        raise SystemExit("Error: session name cannot be blank.")
    if not question:
        raise SystemExit("Error: question cannot be blank.")
    return session_name, question


def clean_session_name(raw: str) -> str:
    """Make a safe session filename from up to two words."""
    words = re.findall(r"[a-z0-9]+", raw.lower())[:2]
    return "_".join(words) or "new_session"


def is_exit_word(text: str) -> bool:
    """Return whether text is an exit command."""
    return text.strip().lower() in {"exit", "quit"}
