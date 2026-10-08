# Helper functions
def get_word_count(text):
    return len(text.split())


def get_space_count(text):
    return text.count(" ")


def get_uppercase_count(text):
    total = 0

    for char in text:
        if char.isupper():
            total += 1

    return total


# Part 1 - Count words, spaces, and uppercase letters
def add_text_stats(given_func):

    def wrapper(*args, **kwargs):
        text = given_func(*args, **kwargs)

        words = get_word_count(text)
        spaces = get_space_count(text)
        uppercase = get_uppercase_count(text)

        return f"[No. of Words: {words}, No. of Spaces: {spaces}, No. of Uppercase Chars: {uppercase}] {text}"

    return wrapper


# Part 2 - Choose what to count
def analyze_text(
    count_words=True,
    count_spaces=True,
    count_uppercase_chars=True,
):

    def decorator(given_func):

        def wrapper(*args, **kwargs):
            text = given_func(*args, **kwargs)
            summary = []

            if count_words:
                summary.append(f"No. of Words: {get_word_count(text)}")

            if count_spaces:
                summary.append(f"No. of Spaces: {get_space_count(text)}")

            if count_uppercase_chars:
                summary.append(
                    f"No. of Uppercase Chars: {get_uppercase_count(text)}"
                )

            if not summary:
                return text

            return "[" + ", ".join(summary) + "] " + text

        return wrapper

    return decorator


# Text used in all examples
sentence = "The Codeline Legends team is learning Python decorators in Muscat this week."


# Part 1 example
@add_text_stats
def get_sentence():
    return sentence


# Part 2 examples
@analyze_text()
def get_sentence_all():
    return sentence


@analyze_text(count_spaces=False)
def get_sentence_without_spaces():
    return sentence


@analyze_text(count_words=False, count_spaces=False)
def get_sentence_uppercase_only():
    return sentence


# Edge case
@analyze_text(
    count_words=False,
    count_spaces=False,
    count_uppercase_chars=False,
)
def get_sentence_no_stats():
    return sentence


# Print 
print(get_sentence())
print(get_sentence_all())
print(get_sentence_without_spaces())
print(get_sentence_uppercase_only())
print(get_sentence_no_stats())