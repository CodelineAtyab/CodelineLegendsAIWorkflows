#writing to a file
#file = open('data.txt', 'w')
#file.write("This is a sample text file.\n")
#file.close()
#############################################
#read a file
#f = open("data.txt", "r")
#text = f.read()
#f.close()
#print(text)
#############################################
import csv
#f = open("data.csv", "r")
#text = f.read()
#f.close()
#print(text)
#############################################
header_to_write = "id, name,email"
data_to_write=["123,Mr.A,mra@gmail.com" ,"123,Mr.A,mra@gmail.com","123,Mr.A,mra@gmail.com"]
fw = open("data.csv", "w")
for row in data_to_write:
    fw.write(row + "\n")
fw.close()