
# List comprehension
numbers = [1, 2, 3, 4, 5]

squares = [number * number for number in numbers]

print(squares)


# Dictionary comprehension
pairs = [("name", "Rahaf"), ("city", "Muscat"), ("country", "Oman")]

person = {key: value for key, value in pairs}

print(person)
