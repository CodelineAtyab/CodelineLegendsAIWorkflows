from email.mime import text

def num_words(text):
    return len(text.split())


def num_spaces(text):
    return text.count(" ")


def num_uppercase_chars(text):
    return sum(1 for char in text if char.isupper())

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
                data.append(f"No. of Uppercase Chars: {uppercase_chars}")

            summary = "[ " + ", ".join(data) + "] "

            return summary + news
        return wrapper
    return decorator

@text_analyzer()
def get_news(news):
    return news

print(get_news("The Codeline Legends team is learning Python decorators in Muscat this week.")  )