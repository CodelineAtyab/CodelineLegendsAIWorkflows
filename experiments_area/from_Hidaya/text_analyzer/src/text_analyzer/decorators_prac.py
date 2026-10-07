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
def count_words(text):
    words = 0
    for word in text.split(" "):
        if word:
            words += 1
    return words
def count_spaces(text):
    return text.count(" ")
def count_uppercase(text):
    uppercase = 0
    for char in text:
        if "A" <= char <= "Z":
            uppercase += 1
    return uppercase

#Do part 1 again and use the helper functions
def add_text_stats(func):
    def wrapper(*args , **kwargs):
        text = func(*args , **kwargs)
        words = count_words(text)
        spaces = count_spaces(text)
        uppercase = count_uppercase(text)
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
