from email.mime import text

def num_words(text):
    return len(text.split())


def num_spaces(text):
    return text.count(" ")


def num_uppercase_chars(text):
    return sum(1 for char in text if char.isupper())


# Criterion 2 (Part 1): Standalone decorator
def add_text_stats(func):
    def wrapper(*args, **kwargs):
        news = func(*args, **kwargs)

        words = num_words(news)
        spaces = num_spaces(news)
        uppercase_chars = num_uppercase_chars(news)

        summary = (
            f"[No. of Words: {words}, "
            f"No. of Spaces: {spaces}, "
            f"No. of Uppercase Chars: {uppercase_chars}] "
        )

        return summary + news

    return wrapper


# Criterion 3: Decorator with parameters
def analyze_text(
    count_words=True,
    count_spaces=True,
    count_uppercase_chars=True
):
def text_analyzer(count_words=True, count_spaces=True, count_uppercase_chars=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            news = func(*args, **kwargs)
            data = []

            if count_words:
                words = num_words(news)
                data.append(f"No. of Words: {words}")

            if count_spaces:
                spaces = num_spaces(news)
                data.append(f"No. of Spaces: {spaces}")

            if count_uppercase_chars:
                uppercase_chars = num_uppercase_chars(news)
                data.append(
                    f"No. of Uppercase Chars: {uppercase_chars}"
                )

            # Return the original text if no statistics are selected
            if not data:
                return news

            summary = "[ " + ", ".join(data) + " ] "
            return summary + news

        return wrapper

    return decorator


# Example 1: Using the standalone decorator
@add_text_stats
def get_news(news):
    return news


# Example 2: Using the parameterized decorator
@analyze_text(
    count_words=True,
    count_spaces=False,
    count_uppercase_chars=True
)
def get_news_filtered(news):
    return news


news = (
    "The Codeline Legends team is learning Python decorators "
    "in Muscat this week."
)

print(get_news(news))
print(get_news_filtered(news))
            if count_words:
                words = num_words(news)
                data.append(f"No. of Words: {words}")
            if count_spaces:
                spaces = num_spaces(news)
                data.append(f"No. of Spaces: {spaces}")
            if count_uppercase_chars:
                uppercase_chars = num_uppercase_chars(news)
                data.append(f"No. of Uppercase Chars: {uppercase_chars}")
            else:
                return news
               
            summary = "[ " + ", ".join(data) + "] "

            return summary + news
        return wrapper
    return decorator

@text_analyzer()
def get_news(news):
    return news

print(get_news("The Codeline Legends team is learning Python decorators in Muscat this week.")  )
