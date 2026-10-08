#Part 1 – decorator
#def add_text_stats(func):
    #def wrapper(*args , **kwargs):
        #text = func(*args , **kwargs)
        #words = 0
        #for word in text.split(" "):
            #if word:
            #    words += 1
        #spaces = text.count(" ")
        #uppercase = 0
        #for char in text:
            #if "A" <= char <= "Z":
                #uppercase += 1
        #return (
            #f"[No. of Words: {words}, "
            #f"No. of Spaces: {spaces}, "
            #f"No. of Uppercase Chars: {uppercase}] {text}"
           #)   
    #return wrapper


#Do helper functions to use it in part 1 and part 2
def get_word_count(text):
    words = 0
    for word in text.split(" "):
        if word:
            words += 1
    return words
def get_count_spaces(text):
    return text.count(" ")
def get_count_uppercase(text):
    uppercase = 0
    for char in text:
        if "A" <= char <= "Z":
            uppercase += 1
    return uppercase

#Do part 1 again and use the helper functions
def add_text_stats(func):
    def wrapper(*args, **kwargs):
        text = func(*args, **kwargs)
        words = get_word_count(text)
        spaces = get_count_spaces(text)
        uppercase = get_count_uppercase(text)
        return (
            f"[No. of Words: {words}, "
            f"No. of Spaces: {spaces}, "
            f"No. of Uppercase Chars: {uppercase}] {text}"
           )   
    return wrapper
@add_text_stats
def get_news():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."
print(get_news())

#Part 2 – decorator with parameters 
def analyze_text(count_words=True, count_spaces=True, count_uppercase_chars=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)
            if not count_words and not count_spaces and not count_uppercase_chars:
                return text
            result = ""
            if count_words:
                result += f"No. of Words: {get_word_count(text)}, "
            if count_spaces:
                result += f"No. of Spaces: {get_count_spaces(text)}, "
            if count_uppercase_chars:
                result += f"No. of Uppercase Chars: {get_count_uppercase(text)}, "
            return f"[{result[:-2]}] {text}"
        return wrapper
    return decorator

# Example that forwards positional and keyword arguments
@analyze_text(count_spaces=False)
def get_news_without_spaces():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."
print(get_news_without_spaces())

@analyze_text(count_words=False, count_spaces=False)
def get_news_uppercase_only():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."
print(get_news_uppercase_only())
    
@analyze_text(count_words=False, count_spaces=False, count_uppercase=False)
def get_news_without_stats():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."
print(get_news_without_stats())
@analyze_text()
def greet(name, message="Welcome"):
    return f"{message} {name}!"
print(greet("Hidaya", message="Hello"))
    