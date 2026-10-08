connect_to_db = lambda: None

sum = lambda num1, num2: num1 + num2

sum(1, 2)
connect_to_db()

data = [11, 2, 3, 12, 6, 7, 3, 9, 45, 100]

# filtered_list = []
# for num in data:
#   if num % 2 == 0:
#     filtered_list.append(num)

filtered_list = list(filter(lambda num: num % 2 == 0, data))
print(filtered_list)
