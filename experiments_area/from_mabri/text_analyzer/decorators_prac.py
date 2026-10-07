def get_word_count(text):
    return len(text.split())

def get_space_count(text):
    return text.count(' ')

def get_uppercase_count(text):
    return sum(1 for c in text if c.isupper())
    #return len(list(filter(lambda c: c.isupper(), text)))

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

@analyze_text()
def get_news():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

print(get_news() + "\n")

@analyze_text(count_spaces=False)
def get_news():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

print(get_news() + "\n")

@analyze_text(count_words=False, count_spaces=False)
def get_news():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

print(get_news() + "\n")

@analyze_text(count_words=False, count_spaces=False, count_uppercase_chars=False)
def get_news():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

print(get_news() + "\n")    