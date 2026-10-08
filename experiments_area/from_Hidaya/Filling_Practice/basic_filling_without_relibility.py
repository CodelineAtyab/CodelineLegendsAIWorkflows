#writing to a file
file = open('data.txt', 'w')
file.write("This is a sample text file.\n")
file.close()

#read a file
f = open("data.txt", "r")
text = f.read()
f.close()
print(text)