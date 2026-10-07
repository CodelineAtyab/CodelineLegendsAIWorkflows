def add_text_stats(given_fun):
    def text_stats_func_call(*args, **kwargs):
        words_num = len(given_fun(*args, **kwargs).split())
        space_count = given_fun(*args, **kwargs).count(" ")
        uppercase_char = 0
        for char in given_fun(*args, **kwargs):
            if char.isupper():
                uppercase_char += 1
        result = f"[No. of Words: {words_num}, No. of Spaces: {space_count}, No. of Uppercase Chars: {uppercase_char}] {given_fun(*args, **kwargs)}"
        return result
    return text_stats_func_call




@add_text_stats
def get_news(msg):
    return msg 

print(get_news("The Codeline Legends team is learning Python decorators in Muscat this week."))
