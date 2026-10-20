

def parse_args(argv: list[str]) -> tuple[str | None, str | None]:
    """Parse CLI arguments into a session name and question or raise SystemExit on error."""
    if len(argv) == 1:
        return None, None
    if len(argv) == 2:
        question = argv[1].strip()
        if not question:
            raise SystemExit("Error: Question cannot be blank or whitespace.")
        return None, question
    if len(argv) == 3:
        session_name = clean_session_name(argv[1])
        question = argv[2].strip()
        if not question:
            raise SystemExit("Error: Question cannot be blank or whitespace.")
        return session_name, question
    raise SystemExit("Error: Too many arguments provided.")


def clean_session_name(raw: str) -> str:
    """Turn the model's naming reply into a lowercase two-word name like oman_capital."""
    words = [w.strip(".,!?;:\"'").lower() for w in raw.split()]
    words = [w for w in words if w]
    if not words:
        return "new_session"
    if len(words) == 1:
        return words[0]
    return f"{words[0]}_{words[1]}"


def is_exit_word(text: str) -> bool:
    """Determine if text is an exit word (exit or quit) ignoring case and surrounding spaces."""
    return text.strip().lower() in {"exit", "quit"}
