list_of_odd_numbers = [num for num in range(101) if num % 2 != 0]
print(list_of_odd_numbers)


tuple_items = (["name", "Ahmed"], ["ID", "123234"], ["Gender", "Male"])
dict_of_user_info = {k: v for k, v in tuple_items}
print(dict_of_user_info)
