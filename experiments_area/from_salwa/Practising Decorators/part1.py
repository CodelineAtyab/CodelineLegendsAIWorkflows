# Part 1: add_text_stats decorator
# function to count word
def get_word_count(text):
    return len(text.split())
# function to count space
def get_space_count(text):
    return text.count(" ")
# function to count uppercase
def  get_uppercase_count(text):
     return sum(1 for char in text if char.isupper())

# function receives the original function
def  add_text_stats(func):
# function runs the original function
 def wrapper(*args, **kwargs):

        text = func(*args, **kwargs)
  # Count words, spaces, and uppercase characters
        words = get_word_count(text)
        spaces = get_space_count(text)
        uppercase = get_uppercase_count(text)
 # Create the summary
        summary = f"[No. of Words: {words}, "
        summary += f"No. of Spaces: {spaces}, "
        summary += f"No. of Uppercase Chars: {uppercase}]"
   # Add the summary before the original text
        result = summary + " " + text
        return result 
 return wrapper

# orignal function 
@add_text_stats
def get_news():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

print(get_news())
