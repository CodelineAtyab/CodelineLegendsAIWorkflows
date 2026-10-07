def add_text_stats(func):
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        words_num = len(text.split())
        spaces_num = text.count(' ')
        uppercase_num = sum(1 for c in text if c.isupper())
        ##uppercase_num = len(list(filter(lambda c: c.isupper(), text)))
        return f"[No. of Words: {words_num}, No. of Spaces: {spaces_num}, No. of Uppercase Chars: {uppercase_num}] {text}"
    return wrapper

@add_text_stats
def get_news():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

print(get_news())