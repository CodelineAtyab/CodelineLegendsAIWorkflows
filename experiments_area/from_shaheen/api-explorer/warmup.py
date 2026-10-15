list_name = [num * num for num in range(10)]
print(list_name)

dict_name = [("Ali", 85), ("Ahmed", 90), ("Sara", 95)]

student_grades = {name: grade for name, grade in dict_name}

print(student_grades)
