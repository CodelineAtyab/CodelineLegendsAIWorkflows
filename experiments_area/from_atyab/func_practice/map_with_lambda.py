data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = []

result = list(map(lambda num: num * num, data))

# for num in data:
#   result.append(num * num)

print(result)
# result = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]