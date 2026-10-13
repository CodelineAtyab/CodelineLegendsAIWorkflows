def normal_range(start, end):
    count = start
    while count <= end:
        return count
        count = count + 1


# res = normal_range(1, 3)
# print(res)
# res = normal_range(1, 3)
# print(res)
# res = normal_range(1, 3)
# print(res)


def my_range(start, end):
    count = start
    while count <= end:
        yield count
        count = count + 1


# gen = my_range(1, 3)  # Just returns the generator object that we can use later
# res = next(gen)  # Call for the first time
# print(res)
# res = next(gen)  # Call for the second time
# print(res)
# res = next(gen)  # Call for the third time
# print(res)

for i in my_range(1, 30):
    print(i)
