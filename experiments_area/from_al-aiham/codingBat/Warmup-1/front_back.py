def front_back(str1):
  if len(str1) > 1:
    return str1[-1]+str1[1:-1:1]+str1[0]
  else:
    return str1