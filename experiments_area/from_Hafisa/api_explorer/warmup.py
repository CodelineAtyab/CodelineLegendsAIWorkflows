numbers = [1, 2, 3, 4, 5]

squares = [number * number for number in numbers]

pairs = [
    ("name", "Baraah"),
    ("city", "Muscat"),
    ("country", "Oman")
]

person = {key: value for key, value in pairs}

print(squares)
print(person)