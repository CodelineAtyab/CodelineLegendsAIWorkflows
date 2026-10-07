def analyze_text(words = True, spaces = True, uppercase = True):   
    def add_text_stats(given_fun):
        def text_stats_func_call(*args, **kwargs):
            result = f"{given_fun(*args, **kwargs)}"
            words_num = len(given_fun(*args, **kwargs).split())
            space_count = given_fun(*args, **kwargs).count(" ")
            uppercase_char = 0
            for char in given_fun(*args, **kwargs):
                if char.isupper():
                    uppercase_char += 1
            text = []

            if(words):
                text.append(f"No. of Words: {words_num}")

            if(spaces):
                text.append(f"No. of Spaces: {space_count}")

            if(uppercase):
                text.append(f"No. of Uppercase Chars: {uppercase_char}")

            if(not text):
                return result

            return f"[{', '.join(text)}] {result}"
        return text_stats_func_call
    return add_text_stats

@analyze_text()
def get_news1(msg):
    return msg 


@analyze_text(words= False)
def get_news2(msg):
    return msg 


@analyze_text(words= False, uppercase= False)
def get_news3(msg):
    return msg 

@analyze_text(words = False,spaces = False, uppercase = False)
def get_news4(msg):
    return msg 

message = "The Codeline Legends team is learning Python decorators in Muscat this week."


print("\n\n\n" + get_news1(message))

print("\n\n\n" + get_news2(message))

print("\n\n\n" + get_news3(message))

print("\n\n\n" + get_news4(message))
