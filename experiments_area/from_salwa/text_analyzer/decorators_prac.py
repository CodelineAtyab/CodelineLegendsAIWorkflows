# Part 1: add_text_stats decorator

def get_word_count(text):
    return len(text.split())
def get_space_count(text):
    return text.count(" ")
def get_uppercase_count(text):
    count = 0
    for char in text:
        if char.isupper():
            count = count + 1
    return count
# function receives the original function
def add_text_stats(func):

    # function runs the original function
    def wrapper(*args, **kwargs):

        text = func(*args, **kwargs)

        words = get_word_count(text)
        spaces = get_space_count(text)
        uppercase = get_uppercase_count(text)

        summary = f"[No. of Words: {words}, "
        summary += f"No. of Spaces: {spaces}, "
        summary += f"No. of Uppercase Chars: {uppercase}]"

        result = summary + " " + text

        return result

    return wrapper

@add_text_stats
def get_news():
    return (
        "The Codeline Legends team is learning Python decorators in Muscat this week."
    )

print(get_news())

# Part 2: analyze_text decorator with paramet
def analyze_text(count_words=True, count_spaces=True, count_uppercase_chars=True):

    def decorator(func):

        def wrapper(*args, **kwargs):

            text = func(*args, **kwargs)

            summary_parts = []

            if count_words:
                words = get_word_count(text)
                summary_parts.append(f"No. of Words: {words}")

            if count_spaces:
                spaces = get_space_count(text)
                summary_parts.append(f"No. of Spaces: {spaces}")

            if count_uppercase_chars:
                uppercase = get_uppercase_count(text)
                summary_parts.append(f"No. of Uppercase Chars: {uppercase}")

            # If all three are False
            if not summary_parts:
                return text

            summary = "[" + ", ".join(summary_parts) + "]"

            return summary + " " + text

        return wrapper

    return decorator


# Example 1
@analyze_text()
def get_news_1():
    return (
        "The Codeline Legends team is learning Python decorators in Muscat this week."
    )


# Example 2
@analyze_text(count_spaces=False)
def get_news_2():
    return (
        "The Codeline Legends team is learning Python decorators in Muscat this week."
    )


# Example 3
@analyze_text(count_words=False, count_spaces=False)
def get_news_3():
    return (
        "The Codeline Legends team is learning Python decorators in Muscat this week."
    )


# Example 4
@analyze_text(count_words=False, count_spaces=False, count_uppercase_chars=False)
def get_news_4():
    return (
        "The Codeline Legends team is learning Python decorators in Muscat this week."
    )

print(get_news_1())
print(get_news_2())
print(get_news_3())
print(get_news_4())
