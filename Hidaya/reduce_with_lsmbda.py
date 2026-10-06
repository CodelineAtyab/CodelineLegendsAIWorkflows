from functools import reduce

data = [ 1, 2, 3, 4, 5]
#A function that takes two arguments and returns their sum: 1 is state, 2nd is action
# x=0 , y = 1 => 0 + 1 = 1
# x=1 , y = 2 => 1 + 2 = 3
# x=3 , y = 3 => 3 + 3 = 6
# x=6 , y = 4 => 6 + 4 = 10
# x=10 , y = 5 => 10 + 5 = 15
reduce(lambda x, y: x + y, data, 0) # 15
reduce(None, data)