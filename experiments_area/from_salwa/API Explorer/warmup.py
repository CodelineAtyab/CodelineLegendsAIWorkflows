# list Comprehension

names = ["salwa", "ali", "khalfan"]
upper_name = [name.upper() for name in names]
print(upper_name)

numbers = [1, 2, 3, 4, 5]
squares = [num**2 for num in numbers]
print(squares)

even_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_num = [num for num in even_numbers if num % 2 == 0]
print(even_num)

#  dict comprehension

numbers_dic = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers_dic = {number: number**2 for number in numbers_dic if number % 2 == 0}
print(even_numbers_dic)
