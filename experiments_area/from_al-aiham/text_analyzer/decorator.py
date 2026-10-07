def analyze_text(count_words=True, count_spaces=True, count_uppercase=True):
    def display_news(func):
        def wrapper():
            text = func()
            list_of_text = text.strip().split(" ")
            W = len(list_of_text)
            S = len(list_of_text) - 1
            U = 0

            for word in list_of_text:
                for latter in word:
                    if latter == latter.upper() and latter != ".":
                        U += 1

            if count_words == True and count_spaces == True and count_uppercase == True: 
                return f"\n[No. of Words: <{W}>, No. of Spaces: <{S}>, No. of Uppercase Chars: <{U}>] \n\n {text.strip()}\n"
            
            elif count_words == True and count_spaces == False and count_uppercase == True:
                return f"\n[No. of Words: <{W}>, No. of Uppercase Chars: <{U}>] \n\n {text.strip()}\n"
            
            elif count_words == False and count_spaces == False and count_uppercase == True:
                return f"\n[No. of Uppercase Chars: <{U}>] \n\n {text.strip()}\n"
            
        return wrapper
    return display_news


@analyze_text(count_words=True , count_spaces=True)
def get_news1():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

@analyze_text(count_words=True , count_spaces=False)
def get_news2():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

@analyze_text(count_words=False , count_spaces=False)
def get_news3():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

print(get_news1())
print(get_news2())
print(get_news3())