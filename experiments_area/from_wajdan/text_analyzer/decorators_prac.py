# Shared counting logic
def get_text_stats(text):
    words = len(text.split())
    spaces = text.count(" ")

    uppercase = 0
    for char in text:
        if "A" <= char <= "Z":
            uppercase += 1

    return words, spaces, uppercase


# Part 1: Decorator
def add_text_stats(given_fun):
    def decorated_func(*args, **kwargs):
        text = given_fun(*args, **kwargs)
        words, spaces, uppercase = get_text_stats(text)

        final_msg = (
            f"[No. of Words: {words}, "
            f"No. of Spaces: {spaces}, "
            f"No. of Uppercase Chars: {uppercase}] "
        )
        final_msg = final_msg + text
        return final_msg

    return decorated_func


# Part 2: Decorator with parameters
def analyze_text(
    count_words=True,
    count_spaces=True,
    count_uppercase_chars=True,
):
    def decorator(given_fun):
        def decorated_func(*args, **kwargs):
            text = given_fun(*args, **kwargs)
            words, spaces, uppercase = get_text_stats(text)

            stats = []
            
            if count_words:
                stats.append(f"No. of Words: {words}")

            if count_spaces:
                stats.append(f"No. of Spaces: {spaces}")
                
            if count_uppercase_chars:
                stats.append(f"No. of Uppercase Chars: {uppercase}")

            if not stats:
                return text

            final_msg = "[" + ", ".join(stats) + "] "
            final_msg = final_msg + text
            return final_msg

        return decorated_func

    return decorator


# Example 1: Part 1
@add_text_stats
def get_message(message):
    return message


# Example 2: All counts enabled
@analyze_text()
def get_all_stats(message):
    return message


# Example 3: Without spaces
@analyze_text(count_spaces=False)
def get_custom_message(message):
    return message


# Example 4: Only uppercase characters
@analyze_text(count_words=False, count_spaces=False)
def get_uppercase_only(message):
    return message


# Example 5: Original text without a summary
@analyze_text(
    count_words=False,
    count_spaces=False,
    count_uppercase_chars=False,
)
def get_original_message(message):
    return message


message = (
    "The Codeline Legends team is learning Python decorators "
    "in Muscat this week."
)

print(get_message(message))
print(get_all_stats(message=message))
print(get_custom_message(message))
print(get_uppercase_only(message))
print(get_original_message(message))