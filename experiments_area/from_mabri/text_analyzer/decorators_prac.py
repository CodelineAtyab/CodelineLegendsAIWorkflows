def get_word_count(text):
    return len(text.split())


def get_space_count(text):
    return text.count(" ")


def get_uppercase_count(text):
    return sum(1 for c in text if c.isupper())
    # return len(list(filter(lambda c: c.isupper(), text)))


# Part 1: Basic Decorator
def add_text_stats(func):
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        words_num = get_word_count(text)
        spaces_num = get_space_count(text)
        uppercase_num = get_uppercase_count(text)
        return f"[No. of Words: {words_num}, No. of Spaces: {spaces_num}, No. of Uppercase Chars: {uppercase_num}] {text}"

    return wrapper


# Part 2: Parameterized Decorator
def analyze_text(count_words=True, count_spaces=True, count_uppercase_chars=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)
            stats = []
            if count_words:
                stats.append(f"No. of Words: {get_word_count(text)}")
            if count_spaces:
                stats.append(f"No. of Spaces: {get_space_count(text)}")
            if count_uppercase_chars:
                stats.append(f"No. of Uppercase Chars: {get_uppercase_count(text)}")
            if not stats:
                return text
            return f"[{', '.join(stats)}] {text}"

        return wrapper

    return decorator


NEWS_TEXT = (
    "The Codeline Legends team is learning Python decorators in Muscat this week."
)


# Part 1: the plain decorator always shows all three counts
@add_text_stats
def get_news_with_all_stats():
    return NEWS_TEXT


# Part 2: every option defaults to True, so this matches Part 1
@analyze_text()
def get_news_with_defaults():
    return NEWS_TEXT


# Part 2: spaces switched off
@analyze_text(count_spaces=False)
def get_news_without_spaces():
    return NEWS_TEXT


# Part 2: only uppercase chars left on
@analyze_text(count_words=False, count_spaces=False)
def get_news_uppercase_only():
    return NEWS_TEXT


# Part 2 edge case: all options off, so the text comes back unchanged
@analyze_text(count_words=False, count_spaces=False, count_uppercase_chars=False)
def get_news_without_stats():
    return NEWS_TEXT


print(get_news_with_all_stats())
print(get_news_with_defaults())
print(get_news_without_spaces())
print(get_news_uppercase_only())
print(get_news_without_stats())
