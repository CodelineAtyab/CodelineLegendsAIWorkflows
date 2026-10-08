def no_of_words(text):
    return len(text.split(" "))

def no_of_spaces(text):
    return text.count(" ")

def no_of_uppercase(text):
    return sum(1 for letter in text if "A" <= letter <= "Z")

def analyze_text(count_words=True, count_spaces=True, count_uppercase=True):
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
            
            if count_uppercase:
                result.append(f"No. of Uppercase Chars: {U}")

            if not result:
                return text
            
            return f"[{", ".join(result)}]\n{text}"
        return wrapper
    return add_text_status


# @analyze_text(count_words=True , count_spaces=True)
# def get_news1():
#     return "The Codeline Legends team is learning Python decorators in Muscat this week."

# @analyze_text(count_words=True , count_spaces=False)
# def get_news2():
#     return "The Codeline Legends team is learning Python decorators in Muscat this week."

# @analyze_text(count_words=False , count_spaces=False)
# def get_news3():
#     return "The Codeline Legends team is learning Python decorators in Muscat this week."

# print(get_news1())
# print(get_news2())
# print(get_news3())



@analyze_text()
def greet_me(name):
    return f"Welcome Back {name}"

print(greet_me("Al-Aiham"))
