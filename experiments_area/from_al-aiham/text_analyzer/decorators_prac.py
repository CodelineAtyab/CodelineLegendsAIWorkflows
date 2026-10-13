def no_of_words(text):
    return len(text.split(" "))


def no_of_spaces(text):
    return text.count(" ")


def no_of_uppercase(text):
    return sum(1 for letter in text if "A" <= letter <= "Z")


def add_text_stats(func):
    return analyze_text()(func)


def analyze_text(count_words=True, count_spaces=True, count_uppercase_chars=True):
    def add_text_status(func):
        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)

            W = no_of_words(text)
            S = no_of_spaces(text)
            U = no_of_uppercase(text)

            result = []

            if count_words:
                result.append(f"No. of Words: {W}")

            if count_spaces:
                result.append(f"No. of Spaces: {S}")

            if count_uppercase_chars:
                result.append(f"No. of Uppercase Chars: {U}")

            if not result:
                return text

            return f"[{', '.join(result)}] {text}"

        return wrapper

    return add_text_status


@add_text_stats
def get_news1():
    return (
        "The Codeline Legends team is learning Python decorators in Muscat this week."
    )


@analyze_text()
def get_news2():
    return (
        "The Codeline Legends team is learning Python decorators in Muscat this week."
    )


@analyze_text(count_spaces=False)
def get_news3():
    return (
        "The Codeline Legends team is learning Python decorators in Muscat this week."
    )


@analyze_text(count_words=False, count_spaces=False)
def get_news4():
    return (
        "The Codeline Legends team is learning Python decorators in Muscat this week."
    )


@analyze_text(False, False, False)
def get_news5():
    return (
        "The Codeline Legends team is learning Python decorators in Muscat this week."
    )


print(get_news1())
print(get_news2())
print(get_news3())
print(get_news4())
print(get_news5())


@analyze_text()
def greet_me(name):
    return f"Welcome Back {name}"


print(greet_me("Al-Aiham"))
