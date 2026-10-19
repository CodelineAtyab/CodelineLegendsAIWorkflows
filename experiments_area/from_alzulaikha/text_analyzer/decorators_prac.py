def get_word_count(text):
    return len(text.split())


def get_space_count(text):
    return text.count(" ")


def get_uppercase_count(text):
    count = 0
    for char in text:
        if char.isupper():
            count += 1
    return count


# Part 1 - add_text_stats decorator
def add_text_stats(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        word_count = get_word_count(result)
        space_count = get_space_count(result)
        upper_count = get_uppercase_count(result)

        summary = (
            f"[No. of Words: {word_count}, "
            f"No. of Spaces: {space_count}, "
            f"No. of Uppercase Chars: {upper_count}] "
        )

        return summary + result

    return wrapper


# Part 2 - analyze_text decorator factory
def analyze_text(
    count_words=True,
    count_spaces=True,
    count_uppercase_chars=True
):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            parts = []

            if count_words:
                parts.append(
                    f"No. of Words: {get_word_count(result)}"
                )

            if count_spaces:
                parts.append(
                    f"No. of Spaces: {get_space_count(result)}"
                )

            if count_uppercase_chars:
                parts.append(
                    f"No. of Uppercase Chars: {get_uppercase_count(result)}"
                )

            if not parts:
                return result

            summary = "[" + ", ".join(parts) + "] "

            return summary + result

        return wrapper

    return decorator

    #Testing
@analyze_text()
def get_news_all():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

print(get_news_all())


@analyze_text(count_spaces=False)
def get_news_no_spaces():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

print(get_news_no_spaces())


@analyze_text(count_words=False, count_spaces=False)
def get_news_uppercase_only():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

print(get_news_uppercase_only())

@add_text_stats
def get_news():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."


print(get_news())


# Edge case

@analyze_text(
    count_words=False,
    count_spaces=False,
    count_uppercase_chars=False
)
def get_news_no_stats():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

print(get_news_no_stats())