# Helper functions


def get_word_count(text):
    return len(text.split())


def get_space_count(text):
    return text.count(" ")


def get_uppercase_count(text):
    return sum(1 for char in text if char.isupper())


# Part 1


def add_text_stats(func):
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        word_count = get_word_count(text)
        spaces = get_space_count(text)
        uppercase_count = get_uppercase_count(text)

        return f"[No. of Words: {word_count}, No. of Spaces: {spaces}, No. of Uppercase Chars: {uppercase_count}] {text}"

    return wrapper


# Part 2


def analyze_text(count_words=True, count_spaces=True, count_uppercase_chars=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)

            word_count = get_word_count(text)
            spaces = get_space_count(text)
            uppercase_count = get_uppercase_count(text)

            stats = []

            if count_words:
                stats.append(f"No. of Words: {word_count}")

            if count_spaces:
                stats.append(f"No. of Spaces: {spaces}")

            if count_uppercase_chars:
                stats.append(f"No. of Uppercase Chars: {uppercase_count}")

            if len(stats) == 0:
                return text

            return f"[{', '.join(stats)}] {text}"

        return wrapper

    return decorator


message = "The Codeline Legends team is learning Python decorators in Muscat this week."


@add_text_stats
def get_news():
    return message


@analyze_text(count_words=True, count_spaces=True, count_uppercase_chars=True)
def get_news2():
    return message


@analyze_text(count_words=True, count_spaces=False, count_uppercase_chars=True)
def get_news3():
    return message


@analyze_text(count_words=False, count_spaces=False, count_uppercase_chars=True)
def get_news4():
    return message


@analyze_text(count_words=False, count_spaces=False, count_uppercase_chars=False)
def get_news5():
    return message


print(get_news())
print(get_news2())
print(get_news3())
print(get_news4())
print(get_news5())
