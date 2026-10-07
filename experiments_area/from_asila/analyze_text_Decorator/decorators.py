#here the functions for count words, spaces, and capital letters in the text and both decorators use them to create the text summary.
def get_word_count(text):
    return len(text.split())


def get_space_count(text):
    return text.count(" ")


def get_uppercase_count(text):
    uppercase_count = 0

    for character in text:
        if character in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            uppercase_count = uppercase_count + 1

    return uppercase_count

#This decorator uses a function inside another function to run the get_news()
# so it count the text details, and add the summary before the text.
def add_text_stats(func):
    def wrapper(*args, **kwargs):
        result =func(*args,**kwargs)
        
        words = get_word_count(result)
        spaces = get_space_count(result)
        uppercase_chars = get_uppercase_count(result)
        
        summary =  ( "[No. of Words: "
            + str(words)
            + ", No. of Spaces: "
            + str(spaces)
            + ", No. of Uppercase Chars: "
            + str(uppercase_chars)
            + "] "
        )
        
        return summary + result

    return wrapper


#applies the decorator to get_news() , so it calls add_text_stats and passes the get_news function to it.
@add_text_stats #decorator is a function that adds extra behavior to another functionwithout changing the code inside it.
def get_news():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

print(get_news())    
    