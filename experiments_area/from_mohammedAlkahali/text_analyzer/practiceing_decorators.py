def add_text_stats(func):
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        word_count = len(text.split())
        space_count = text.count(" ")
        uppercase_count = sum(1 for char in text if char.isupper())
        summary = f"[No. of Words: {word_count}, No. of Spaces: {space_count}, No. of Uppercase Chars: {uppercase_count}]"
        return f"{summary} {text}"
    return wrapper


