"""Minimal example of a testable helper; tests live in tests/test_non_interactive_example.py."""


def ask_ai(msg: str | None) -> str | None:
    """Echo a message back with a prefix; numbers raise TypeError; None/'' pass through."""
    # 1. Reject numbers first so they cannot be silently echoed as text.
    if isinstance(msg, (int, float)):
        raise TypeError("Numbers are not allowed")

    # 2. Pass missing or empty input straight through.
    if not msg:
        return msg

    # 3. Echo the text back with the standard prefix.
    return f"Hey! This is your message: {msg}"
