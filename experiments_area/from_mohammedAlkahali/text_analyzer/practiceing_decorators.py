def add_text_stats(func):
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        word_count = len(text.split())
        space_count = text.count(" ")
        uppercase_count = sum(1 for char in text if char.isupper())
        summary = f"[No. of Words: {word_count}, No. of Spaces: {space_count}, No. of Uppercase Chars: {uppercase_count}]"
        return f"{summary} {text}"
    return wrapper

@add_text_stats
def get_news():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

print(get_news())
