# Reusable @add_text_stats Decorator
def add_text_stats (func):
    def wrapper(*args, **kwargs):
        
        return wrapper



#Part 1 – decorator  
@add_text_stats
def get_news():
    return "The Codeline Legends team is learning Python decorators in Muscat this week."

print(get_news())

# Part 2 – decorator with arguments
@add_text_stats
 