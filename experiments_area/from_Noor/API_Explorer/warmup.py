
# List comprehension: calculate the squares of numbers from 1 to 10.
squares = [num ** 2 for num in range(1, 11)]

print("Squares of numbers from 1 to 10: ", squares)

# Dict comprehension: create a dictionary of students and their marks.
pairs = [("Sara", 90), ("Ali", 85), ("Muna", 95)]

students = {name: mark for name, mark in pairs}

print("Student marks: ", students)