sentence = "The Codeline Legends team is learning Python decorators in Muscat this week."


def words(text):
    return len(text.split())


def spaces(text):
    return text.count(" ")


def uppercase(text):
    return len(list(filter(lambda char: char.isupper(), text)))


def add_text_stats(func):

    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)

        return (
            f"[No. of Words: {words(text)}, "
            f"No. of Spaces: {spaces(text)}, "
            f"No. of Uppercase Chars: {uppercase(text)}] "
            + text
        )

    return wrapper


def analyze_text(
    count_words=True,
    count_spaces=True,
    count_uppercase_chars=True
):

    def decorator(func):

        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)
            result = []

            if count_words:
                result.append(f"No. of Words: {words(text)}")

            if count_spaces:
                result.append(f"No. of Spaces: {spaces(text)}")

            if count_uppercase_chars:
                result.append(f"No. of Uppercase Chars: {uppercase(text)}")

            if len(result) == 0:
                return text

            return f"[{', '.join(result)}] {text}"

        return wrapper

    return decorator


@add_text_stats
def get_news():
    return sentence


@analyze_text()
def get_news_all():
    return sentence


@analyze_text(count_spaces=False)
def get_news_no_spaces():
    return sentence


@analyze_text(
    count_words=False,
    count_spaces=False
)
def get_news_uppercase():
    return sentence


@analyze_text(
    count_words=False,
    count_spaces=False,
    count_uppercase_chars=False
)
def get_news_original():
    return sentence


print(get_news())
print(get_news_all())
print(get_news_no_spaces())
print(get_news_uppercase())
print(get_news_original())