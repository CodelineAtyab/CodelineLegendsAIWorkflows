
# Create a list of five integers to use in the list-comprehension example.
numbers = [1, 2, 3, 4, 5]

# Build a new list by multiplying each number in numbers by itself (squaring it).
squares = [number * number for number in numbers]

# Display the list of squared numbers in the terminal.
print(squares)


# Create a list of two-item tuples; each tuple contains a dictionary key and value.
pairs = [("name", "Rahaf"), ("city", "Muscat"), ("country", "Oman")]

# Build a dictionary by taking the first and second item from each tuple as key and value.
person = {key: value for key, value in pairs}

# Display the resulting dictionary in the terminal.
print(person)
