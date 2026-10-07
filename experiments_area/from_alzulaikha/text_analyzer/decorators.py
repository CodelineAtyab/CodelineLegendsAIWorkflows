def get_word_count(text):
    return len(text.split())

def get_space_count(text):
    return text.count(" ")

def get_uppercase_count(text):
    return sum(1 for char in text if char.isupper())


def add_text_stats(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        word_count = get_word_count(result)
        space_count = get_space_count(result)
        upper_count = get_uppercase_count(result)

        summary = (
            f"[No. of Words: {word_count}, "
            f"No. of Spaces: {space_count}, "
            f"No. of Uppercase Chars: {upper_count}] "
        )

         return summary + result

     return wrapper
