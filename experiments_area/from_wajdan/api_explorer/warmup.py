
squares =[num * num for num in range(1,11)]
print(squares)
# Dict comprehension: build a dict in one line from key/value pairs.
pairs = [("name","wajdan" ), ("id",1)]
student = {k:v for k,v in pairs}
print(student)
