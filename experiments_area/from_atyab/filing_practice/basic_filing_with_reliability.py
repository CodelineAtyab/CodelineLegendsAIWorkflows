import traceback

try:
  text = ""
  with open("data.txt", "r") as data_file:
    text = data_file.read()

  1/0
  
  print(text)
except Exception:
  print(traceback.format_exc())
