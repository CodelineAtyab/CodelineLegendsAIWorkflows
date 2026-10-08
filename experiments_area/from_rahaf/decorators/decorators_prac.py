news_text = "The Codeline Legends team is learning Python decorators in Muscat this week."


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


# Part 1
def add_text_stats(func): # func will contain another function.
    # wrapper is the new function that will run instead of directly running the original function.
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        # *args - It collects extra positional arguments.
        # **kwargs - It collects extra keyword arguments.

        words = get_word_count(text)
        spaces = get_space_count(text)
        uppercase = get_uppercase_count(text)

        summary = (
            f"[No. of Words: {words}, "
            f"No. of Spaces: {spaces}, "
            f"No. of Uppercase Chars: {uppercase}] "
        )

        return summary + text

    return wrapper


@add_text_stats
def get_news():
    return news_text


print(get_news())


# Part 2
def analyze_text(
    count_words=True,
    count_spaces=True,
    count_uppercase_chars=True,
):

    def decorator(func):

        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)

            summary = []

            if count_words:
                summary.append(
                    f"No. of Words: {get_word_count(text)}"
                )

            if count_spaces:
                summary.append(
                    f"No. of Spaces: {get_space_count(text)}"
                )

            if count_uppercase_chars:
                summary.append(
                    f"No. of Uppercase Chars: {get_uppercase_count(text)}"
                )

            if len(summary) == 0:
                return text

            return "[" + ", ".join(summary) + "] " + text

        return wrapper

    return decorator


@analyze_text()
def get_news_all():
    return news_text


@analyze_text(count_spaces=False)
def get_news_without_spaces():
    return news_text


@analyze_text(
    count_words=False,
    count_spaces=False,
)
def get_news_uppercase():
    return news_text


@analyze_text(
    count_words=False,
    count_spaces=False,
    count_uppercase_chars=False,
)
def get_news_original():
    return news_text


print(get_news_all())
print(get_news_without_spaces())
print(get_news_uppercase())
print(get_news_original())