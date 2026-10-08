### ----PART 1---- ###
# Define the all the functions
#word counting 
def words_count(word):
    return len(word.split())
print(words_count("decorator practice"))

#Spaces counting
def space_count(word):
    return word.count(" ")
print(space_count("This is a python decorater practice area"))

#Uppercase count
def uppercase_count(word):
    count = 0
    for ch in word:
        if ch.isupper():
            count +=1
    return count
print(uppercase_count("This is a Python Decorater Practice Area"))
        
# Define the decorator function
def text_status(func):
    def decorator_function(*args, **kwargs):
        word =  func()  #to checke if there is difference if I pass the dynamic arguments here or not ----> word = fun(*args,**kwargs)
        text = words_count(word)
        spaces = space_count(word)
        uppercase = uppercase_count(word)

        analyzer = (f"[Number of words: {text} , " 
                    f"Number of spaces: {spaces} , "
                    f"Number of uppercase letters: {uppercase}] "
                    )

        return analyzer + word 
    return decorator_function

#apply the decorator 
@text_status
def decorator_application():
    return "The Codeline Legends team is learning python decorators this week."
print(decorator_application())

### ---PART 2---###
def analyze_text_fun(count_word= True, count_spaces= True, count_uppercase= True):
    def decorators(func):
        def wrapp_func(*args, **kwargs):
            word = func(*args, **kwargs)
            summary = []
            if count_word:
                summary.append(f"Number of words: {words_count(word)}") #reuse part 1 function
            if count_spaces:
                summary.append(f"Number of spaces: {space_count(word)}")
            if count_uppercase:
                summary.append(f"Number of uppercases: {uppercase_count(word)}")
            else:
                return word
            summary_text = ", ".join(summary)

            return f"[{summary_text}] {word}"
        return wrapp_func
    return decorators

#All true case
@analyze_text_fun()
def analyze_all():
    return "The Codeline Legends team is learning python decorators this week."
print(analyze_all())

#Spaces false case
@analyze_text_fun(count_spaces=False)
def analyze_all():
    return "The Codeline Legends team is learning python decorators this week."
print(analyze_all())

#Spaces and word are false case
@analyze_text_fun(count_word=False, count_spaces=False)
def analyze_all():
    return "The Codeline Legends team is learning python decorators this week."
print(analyze_all())

#all are false 
@analyze_text_fun(count_word=False, count_spaces=False, count_uppercase=False)
def analyze_all():
    return "The Codeline Legends team is learning python decorators this week."
print(analyze_all())