# Helpers for parsing chatbot command-line arguments.

# distinguishes interactive mode, a single question, and a session name plus question. Invalid input raises SystemExit
def parse_args(argv):
    # Return the session name and question from command-line arguments.
    args = argv[1:]

    if len(args) == 0:
        return None, None

    if len(args) > 2:
        raise SystemExit("Error: Too many arguments.")

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


# lowercases the generated name and joins the first two words with _. If the model returns an empty string, it uses new_session
def clean_session_name(raw):
    # Convert a model-generated name into two lowercase words.
    words = raw.strip().lower().split()

    if not words:
        return "new_session"

    return "_".join(words[:2])


# recognizes exit and quit, regardless of capitalization or surrounding spaces.
def is_exit_word(text):
    # Return True if the text is exit or quit, ignoring case and spaces.
    return text.strip().lower() in ("exit", "quit")
