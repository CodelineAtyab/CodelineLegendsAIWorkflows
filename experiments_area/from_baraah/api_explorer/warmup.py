# List comprehension

squares = [n * n for n in range(1, 6)]
print(squares)

# Dictionary comprehension
pairs = [("name", "Baraah"), ("age", 24)]

student = {key: value for key, value in pairs}
print(student)
