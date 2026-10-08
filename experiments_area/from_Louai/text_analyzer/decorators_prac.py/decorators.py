from functools import wraps

# Helper Functions 
def get_stats(text: str) -> dict[str, int]:
    words_count = len(text.split())
    spaces_count = text.count(" ")
    uppercase_count = sum(1 for char in text if char.isupper())
    return {
        "words": words_count,
        "spaces": spaces_count,
        "uppercase": uppercase_count,
    }


# Part 1: add_text_stats Decorator
# 
def add_text_stats(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        original_text = func(*args, **kwargs)
        stats = get_stats(original_text)
        summary = f"[No. of Words: {stats['words']}, No. of Spaces: {stats['spaces']}, No. of Uppercase Chars: {stats['uppercase']}]"
        return f"{summary} {original_text}"

    return wrapper


# Part 2: analyze_text Decorator with Parameters
def analyze_text(
    count_words: bool = True,
    count_spaces: bool = True,
    count_uppercase_chars: bool = True,
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            original_text = func(*args, **kwargs)

            if not any([count_words, count_spaces, count_uppercase_chars]):
                return original_text

            stats = get_stats(original_text)
            parts = []

            if count_words:
                parts.append(f"No. of Words: {stats['words']}")
            if count_spaces:
                parts.append(f"No. of Spaces: {stats['spaces']}")
            if count_uppercase_chars:
                parts.append(f"No. of Uppercase Chars: {stats['uppercase']}")

            summary_str = ", ".join(parts)
            return f"[{summary_str}] {original_text}"

        return wrapper

    return decorator


# Examples Demonstration 
if __name__ == "__main__":
    text_data = "The Codeline Legends team is learning Python decorators in Muscat this week."

    print("--- Part 1 Example ---")

    @add_text_stats
    def get_news_p1():
        return text_data

    print(get_news_p1())
    print("\n--- Part 2 Examples ---")

    # Example 1: All defaults (True)
    @analyze_text()
    def get_news_ex1():
        return text_data

    print(get_news_ex1())

    # Example 2: count_spaces=False
    @analyze_text(count_spaces=False)
    def get_news_ex2():
        return text_data

    print(get_news_ex2())

    # Example 3: count_words=False, count_spaces=False
    @analyze_text(count_words=False, count_spaces=False)
    def get_news_ex3():
        return text_data

    print(get_news_ex3())

    # Example 4: All options False (Edge case)
    @analyze_text(
        count_words=False, count_spaces=False, count_uppercase_chars=False
    )
    def get_news_ex4():
        return text_data

    print(get_news_ex4())