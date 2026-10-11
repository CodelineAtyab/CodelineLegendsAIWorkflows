
print("welcome to python")

name = "salwa"
age=34
major="networking"
is_astudent=True
gender='F'
grade=80

print(name)
print(age)

a=int(input("Enter first number : "))
b=int(input("Enter secand number:"))
print(a+b)
print(a-b)
print(a/b)
print(a*b)


if grade >=90:
 print("A")

elif grade>=80:
 print("B")

elif grade>=70:
 print("C")
else:
 print("fail")

 
name_members: list = ["Hydaya", "Shaheen", "Ikhlas", "Mohammed"]
print(len(name_members))
   
for name in name_members:
  print(name)

name_members.append("salwa")
name_members.remove(name_members[0])



member_info: dict = {"status": "OK", "ip_address": "192.168.1.10", "active": True}
print(member_info["ip_address"])




sentence = "Why do Omanis never get lost in the desert? Because even the dunes know the way to Muscat!"
list_of_words = sentence.split()
new_sentence = "-".join(list_of_words)
print(new_sentence)

print(sentence.upper())
print(sentence.lower())
print(len(sentence))


def hello(name):
    print("hello",name)
hello("salwa")

def sum(a,b):
  return a+b
print(sum(4,6))


#for i in  range(0,4):
 #print(i)

for i in range(1,11,2):
 print(i)