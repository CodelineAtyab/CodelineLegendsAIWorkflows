def add_text_stats(func):
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        word_count = len(text.split())
        space_count = text.count(" ")
        uppercase_count = len(list(filter(lambda c: c.isupper(), text)))
        summary = f"[No. of Words: {word_count}, No. of Spaces: {space_count}, No. of Uppercase Chars: {uppercase_count}]"
        return f"{summary} {text}"
    return wrapper

@add_text_stats
def get_news():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

print(get_news())



def analyze_text(count_words=True, count_spaces=True, count_uppercase_chars=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)
            summary_parts = []
            if count_words:
                word_count = len(text.split())
                summary_parts.append(f"No. of Words: {word_count}")
            if count_spaces:
                space_count = text.count(" ")
                summary_parts.append(f"No. of Spaces: {space_count}")
            if count_uppercase_chars:
                uppercase_count = len(list(filter(lambda c: c.isupper(), text)))
                summary_parts.append(f"No. of Uppercase Chars: {uppercase_count}")
            summary = f"[{', '.join(summary_parts)}]"
            return f"{summary} {text}"
        return wrapper
    return decorator

@analyze_text()
def get_news1():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

@analyze_text(count_spaces=False)
def get_news2():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

@analyze_text(count_words=False, count_spaces=False)
def get_news3():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

print(get_news1())
print(get_news2())
print(get_news3())