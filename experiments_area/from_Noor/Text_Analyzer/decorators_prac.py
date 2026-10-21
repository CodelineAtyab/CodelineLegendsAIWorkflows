
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



# Example 1: Part 1 - Standalone decorator
@add_text_stats
def get_news_part1(news):
    return news


# Example 2: Default analyze_text()
@analyze_text()
def get_news_all(news):
    return news


# Example 3: Do not count spaces
@analyze_text(count_spaces=False)
def get_news_no_spaces(news):
    return news


# Example 4: Do not count words or spaces
@analyze_text(count_words=False, count_spaces=False)
def get_news_uppercase_only(news):
    return news


news = (
    "The Codeline Legends team is learning Python decorators "
    "in Muscat this week."
)

print("Example 1: Part 1")
print(get_news_part1(news))

print("\nExample 2: @analyze_text()")
print(get_news_all(news))

print("\nExample 3: count_spaces=False")
print(get_news_no_spaces(news))

print("\nExample 4: count_words=False, count_spaces=False")
print(get_news_uppercase_only(news))
