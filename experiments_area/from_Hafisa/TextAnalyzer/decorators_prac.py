
def get_word_count(text):
    return len(text.split())


def get_space_count(text):
    return text.count(" ")


def get_uppercase_count(text):
    return len(list(filter(lambda char: char.isupper(), text)))


def add_text_stats(func):

    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)

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
def get_news_part1():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."



def analyze_text(count_words=True, count_spaces=True, count_uppercase_chars=True):

    def decorator(func):

        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)
            summary_parts = []

            if count_words:
                summary_parts.append(f"No. of Words: {get_word_count(text)}")

            if count_spaces:
                summary_parts.append(f"No. of Spaces: {get_space_count(text)}")

            if count_uppercase_chars:
                summary_parts.append(f"No. of Uppercase Chars: {get_uppercase_count(text)}")

            if not summary_parts:
                return text

            summary = "[" + ", ".join(summary_parts) + "] "

            return summary + text

        return wrapper

    return decorator



@analyze_text()
def get_news():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."


@analyze_text(count_spaces=False)
def get_news_no_spaces():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."


@analyze_text(count_words=False, count_spaces=False)
def get_news_uppercase():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."


@analyze_text(count_words=False, count_spaces=False, count_uppercase_chars=False)
def get_news_without_stats():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."


# Print results
print(get_news_part1())
print(get_news())
print(get_news_no_spaces())
print(get_news_uppercase())
print(get_news_without_stats())
