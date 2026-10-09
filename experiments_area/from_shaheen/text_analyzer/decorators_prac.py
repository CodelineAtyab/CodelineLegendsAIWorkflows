#Helper Functions
def words_num(text):
    return len(text.split())

def space_count(text):
    return text.count(" ")

def uppercase_char(text):
    counter = 0
    for char in text:
        if char.isupper():
            counter += 1
    return counter


#Part 1:
def add_text_stats(given_fun):
    def text_stats_func_call(*args, **kwargs):
        func = given_fun(*args, **kwargs)
        result = f"[No. of Words: {words_num(func)}, No. of Spaces: {space_count(func)}, No. of Uppercase Chars: {uppercase_char(func)}] {func}"
        return result
    return text_stats_func_call




@add_text_stats
def get_news(msg):
    return msg 

print(get_news("The Codeline Legends team is learning Python decorators in Muscat this week."))





#Part 2:
def analyze_text(count_words=True, count_spaces=True, count_uppercase_chars=True):
    def add_text_stats(given_fun):
        def text_stats_func_call(*args, **kwargs):          
            func = given_fun(*args, **kwargs)
            result = f"{func}"
            text = []

            if count_words:
                text.append(f"No. of Words: {words_num(func)}")

            if count_spaces:
                text.append(f"No. of Spaces: {space_count(func)}")

            if count_uppercase_chars:
                text.append(f"No. of Uppercase Chars: {uppercase_char(func)}")

            if not text:
                return result

            return f"[{', '.join(text)}] {result}"

        return text_stats_func_call

    return add_text_stats


@analyze_text()
def get_news1(msg):
    return msg


@analyze_text(count_words=False)
def get_news2(msg):
    return msg


@analyze_text(count_words=False, count_uppercase_chars=False)
def get_news3(msg):
    return msg


@analyze_text(count_words=False, count_spaces=False, count_uppercase_chars=False)
def get_news4(msg):
    return msg


@analyze_text(count_spaces=False)
def get_news5(msg):
    return msg


@analyze_text(count_words=False, count_spaces=False)
def get_news6(msg):
    return msg

message = "The Codeline Legends team is learning Python decorators in Muscat this week."


print("\n\n\n" + get_news1(message))

print("\n\n\n" + get_news2(message))

print("\n\n\n" + get_news3(message))

print("\n\n\n" + get_news4(message))

print("\n\n\n" + get_news5(message))

print("\n\n\n" + get_news6(message))
