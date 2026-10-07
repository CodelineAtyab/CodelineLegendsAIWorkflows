def add_text_stats(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        word_count = len(result.split())
        space_count = result.count(" ")
        upper_count= sum(1 for char in result if char.isupper())

        summary = (
            f"[No. of Words: {word_count}, "
            f"No. of Spaces: {space_count}, "
            f"No. of Uppercase Chars: {upper_count}] "
        )

        return summary + result

    return wrapper

    