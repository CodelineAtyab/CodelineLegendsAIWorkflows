data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = []

# for num in data:
#      result.append(num*num)
# print(result)
result = [num * num for num in data]
print(result)

# data = [onum * onum for onum in [num * num for num in range(1, 11)]]
# print(data)
