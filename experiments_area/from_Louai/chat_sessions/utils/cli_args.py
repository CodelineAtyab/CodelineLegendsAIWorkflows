def parse_args(argv: list[str]) -> tuple[str | None, str | None]:
    """Turn the argument list into (session_name, question)."""
    args = argv[1:]

    if len(args) == 0:
        return None, None

    if len(args) > 2:
        raise SystemExit(
            'Error: too many arguments. Use: app.py [session_name] "question"'
        )

    question = args[-1].strip()
    if question == "":
        raise SystemExit("Error: the question cannot be blank.")

    if len(args) == 1:
        return None, question

    return args[0], question


def clean_session_name(raw: str) -> str:
    """Turn the model's naming reply into a two-word, lower-case name."""
    cleaned = ""
    for ch in raw.lower():
        if ch.isalnum():
            cleaned += ch
        else:
            cleaned += " "

    words = cleaned.split()[:2]
    if not words:
        return "new_session"
    return "_".join(words)


def is_exit_word(text: str) -> bool:
    """Return True if text is exit or quit, in any capitalisation."""
    return text.strip().lower() in ("exit", "quit")
