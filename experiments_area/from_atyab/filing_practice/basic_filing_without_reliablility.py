
# Read a file
fr = None
try:
  fr = open("data.txt", "r")
  text = fr.read()
  print(text)
  x = 1/0
except FileNotFoundError:
  print("File data.txt is not present!.")
except ZeroDivisionError:
  print("Why the hell are you diving by zero!!! ???")
except Exception:
  print("Something else happened! and we can not complete the filing operation.")
finally:
  fr.close()
  print("Closed the file:", fr.name)


print("EXITING PROGRAM OR CONTINUE DOING WORK")
print("EXITING PROGRAM OR CONTINUE DOING WORK")
print("EXITING PROGRAM OR CONTINUE DOING WORK")


