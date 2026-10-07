def greet_opal_2(message):
    return message 
print(greet_opal_2("Hello Opal 2!"))
print(greet_opal_2("Opal 2 i doing amazing!"))
print(greet_opal_2("python seems funny!"))


def greet_opal_2():
    return "Hello Opal 2!"
def Feedback_about_opal_2():
    return "Opal 2 is doing amazing!"
def get_feedback_about_python():
    return "Python seems funny!"

#First way we can do this 
print("-----------------------------------")
print(greet_opal_2())
print("-----------------------------------")
print(Feedback_about_opal_2())
print("-----------------------------------")
print(get_feedback_about_python())
print("-----------------------------------")


# this is another way to do the same thing 
#what is decorator in python? 
#the function that takes another function as an argument and extends the behavior of the latter function without explicitly modifying it.
def decorator(func):
    def decorated_func():
        final_msg = " "
        final_msg = final_msg + " ---------------- "
        final_msg = final_msg + func()
        final_msg = final_msg + " ---------------- "
        return final_msg
    return decorated_func
        
new_func = decorator(greet_opal_2)
new_func2 = decorator(Feedback_about_opal_2)
new_func3 = decorator(get_feedback_about_python) 

print(new_func())
print(new_func2())
print(new_func3())