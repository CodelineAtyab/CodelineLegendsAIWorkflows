def analyze_text(count_words=True,count_spaces=True,count_uppercase_chars=True):
    def add_text_stats(func):
        def wrapper():
            text = func()
            word_count = len(text.split())
            spaces = text.count(' ')
            uppercase_count = sum(1 for char in text if char.isupper())
            
            
            if count_words == True and count_spaces == True and count_uppercase_chars == True:
                return f"[No. of Words: {word_count}, No. of Spaces: {spaces}, No. of Uppercase Chars: {uppercase_count}] {text}"
            
            elif count_words == True and count_spaces == False and count_uppercase_chars == True:
                return f"[No. of Words: {word_count}, No. of Uppercase Chars: {uppercase_count}] {text}"        
        
            elif count_words == False and count_spaces == False and count_uppercase_chars == True:
                return f"[ No. of Uppercase Chars: {uppercase_count}] {text}"
            
            elif count_words == False and count_spaces == False and count_uppercase_chars == False:
                            return f"[  {text}"

        return wrapper
    return add_text_stats


message = "The Codeline Legends team is learning Python decorators in Muscat this week."

@analyze_text(count_words=True, count_spaces=True, count_uppercase_chars=True )
def get_news():
    return message


@analyze_text(count_words=True, count_spaces=False, count_uppercase_chars=True )
def get_news2():
    return message


@analyze_text(count_words=False, count_spaces=False, count_uppercase_chars=True )
def get_news3():
    return message

@analyze_text(count_words=False, count_spaces=False, count_uppercase_chars=True )
def get_news3():
    return message

@analyze_text(count_words=False, count_spaces=False, count_uppercase_chars=False )
def get_news4():
    return message

print(get_news())
print(get_news2())
print(get_news3())
print(get_news4())





