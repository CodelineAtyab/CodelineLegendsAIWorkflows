def not_string(str1):
  if (str1[0:4] == "not ") or (str1 == "not"):
    return str1
  else:
    return "not " + str1