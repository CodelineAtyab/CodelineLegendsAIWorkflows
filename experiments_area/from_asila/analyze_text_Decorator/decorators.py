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
    
    
def analyze_text(count_words=True, count_spaces=True, count_uppercase_chars=True,):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args,**kwargs)
            text_stats=[]
        
            if count_words:
                words = get_word_count(result)
                text_stats.append("No. of Words: " + str(words))
            
            if count_spaces:
                spaces = get_space_count(result)
                text_stats.append("No. of Spaces: " + str(spaces))
            
            if count_uppercase_chars:
                uppercase_chars = get_uppercase_count(result)
                text_stats.append("No. of Uppercase Chars: " + str(uppercase_chars))
                
                
            if len(text_stats) == 0:
                return result

                
            summary = ", ".join(text_stats)  #here join to combines all items in text_stats into one sentence with commas

            return "[" + summary + "] " + result
            
        return wrapper
        
    return decorator


@analyze_text()
def get_news_all():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."


@analyze_text(count_spaces=False) # output should be without number of uppercase
def get_news_without_spaces():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."


@analyze_text(count_words=False, count_spaces=False) # so the output should be only number of uppercase
def get_news_uppercase_only():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

# all three options are False
@analyze_text(
    count_words=False,
    count_spaces=False,
    count_uppercase_chars=False,
)
def get_news_empty():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

print(get_news_all())
print(get_news_without_spaces())
print(get_news_uppercase_only())
print(get_news_empty())