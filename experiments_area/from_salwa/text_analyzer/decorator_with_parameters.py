# Part 2: analyze_text decorator with parameters


def get_word_count(text):
    return len(text.split())


def get_space_count(text):
    return text.count(" ")

  
def  get_uppercase_count(text):
     return sum(1 for char in text if char.isupper())





def analyze_text(
    count_words=True,
    count_spaces=True,
    count_uppercase_chars=True
):



    def decorator(func):

        def wrapper(*args, **kwargs):

            text = func(*args, **kwargs)

            summary_parts = []

            if count_words:
                words = get_word_count(text)
                summary_parts.append(f"No. of Words: {words}")

            if count_spaces:
                spaces = get_space_count(text)
                summary_parts.append(f"No. of Spaces: {spaces}")

            if count_uppercase_chars:
                uppercase = get_uppercase_count(text)
                summary_parts.append(
                    f"No. of Uppercase Chars: {uppercase}"
                )

            # If all three are False
            if not summary_parts:
                return text

            summary = "[" + ", ".join(summary_parts) + "]"

            return summary + " " + text

        return wrapper

    return decorator


# Example 1
@analyze_text()
def get_news_1():
    return "The Codeline Legends team is learning Python"


# Example 2
@analyze_text(count_spaces=False)
def get_news_2():
    return "The Codeline Legends team is learning Python"


# Example 3
@analyze_text(count_words=False, count_spaces=False)
def get_news_3():
    return "The Codeline Legends team is learning Python"


# Example 4
@analyze_text(
    count_words=False,
    count_spaces=False,
    count_uppercase_chars=False
)
def get_news_4():
    return "The Codeline Legends team is learning Python"


print(get_news_1())
print(get_news_2())
print(get_news_3())
print(get_news_4())