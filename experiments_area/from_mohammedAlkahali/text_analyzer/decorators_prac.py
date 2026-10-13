def word_count(text: str) -> int:
    """Number of words, split on whitespace."""
    return len(text.split())


def space_count(text: str) -> int:
    """Number of literal ' ' characters."""
    return text.count(" ")


def uppercase_count(text: str) -> int:
    """Number of uppercase letters."""
    return len(list(filter(lambda c: c.isupper(), text)))


def build_summary(
    text: str, show_words: bool, show_spaces: bool, show_upper: bool
) -> str:
    """
    Build the '[...]' summary for the enabled options only.
    Returns an empty string when nothing is enabled.
    """
    parts: list[str] = []

    if show_words:
        parts.append(f"No. of Words: {word_count(text)}")
    if show_spaces:
        parts.append(f"No. of Spaces: {space_count(text)}")
    if show_upper:
        parts.append(f"No. of Uppercase Chars: {uppercase_count(text)}")

    if not parts:
        return ""

    return f"[{', '.join(parts)}]"


def add_text_stats(func):
    """Prepend all three counts to the text the wrapped function returns."""

    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        summary = build_summary(text, True, True, True)
        return f"{summary} {text}"

    return wrapper


def analyze_text(count_words=True, count_spaces=True, count_uppercase_chars=True):
    """
    Returns a decorator. Three layers:
      analyze_text(...)  -> holds the settings
      decorator(func)    -> receives the function
      wrapper(*a, **kw)  -> runs at call time
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)
            summary = build_summary(
                text, count_words, count_spaces, count_uppercase_chars
            )

            if not summary:
                return text

            return f"{summary} {text}"

        return wrapper

    return decorator


NEWS = "The Codeline Legends team is learning Python decorators in Muscat this week."


@add_text_stats
def get_news_part1() -> str:
    return NEWS


@analyze_text()
def get_news_all() -> str:
    return NEWS


@analyze_text(count_spaces=False)
def get_news_no_spaces() -> str:
    return NEWS


@analyze_text(count_words=False, count_spaces=False)
def get_news_upper_only() -> str:
    return NEWS


@analyze_text(count_words=False, count_spaces=False, count_uppercase_chars=False)
def get_news_nothing() -> str:
    return NEWS


print("Part 1 - add_text_stats:")
print(get_news_part1())

print("\nPart 2 - analyze_text with parameters:")
print(get_news_all())
print(get_news_no_spaces())
print(get_news_upper_only())
print(get_news_nothing())
