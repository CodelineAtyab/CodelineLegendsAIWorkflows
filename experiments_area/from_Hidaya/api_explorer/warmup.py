# List comprehension: squares of numbers 1 to 10
squares = [number**2 for number in range(1, 11)]
print(squares)

# Dict comprehension: build a dictionary from pairs
pairs = [("name", "Hidaya"), ("course", "Python")]
student = {key: value for key, value in pairs}
print(student)

