def count_words(text):
    return len(text.split())

def count_spaces(text):
    return text.count(' ')

def count_uppercase_chars(text):
    return sum(1 for c in text if c.isupper())
    #return len(list(filter(lambda c: c.isupper(), text)))

def add_text_stats(func):
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        words_num = count_words(text)
        spaces_num = count_spaces(text)
        uppercase_num = count_uppercase_chars(text)
        return f"[No. of Words: {words_num}, No. of Spaces: {spaces_num}, No. of Uppercase Chars: {uppercase_num}] {text}"
    return wrapper



@add_text_stats
def get_news():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

print(get_news())

print("\n")

    