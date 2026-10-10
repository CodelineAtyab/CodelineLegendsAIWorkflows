# num1: int = 23
# num2 = 45

# ifWorks:bool = True
# mohd: str = "Hello, World!"
# mohd2: str = "Python is fun!"

# sum: int = num1 + num2
# if ifWorks:
#     print(mohd)
#     print(mohd2)
#     print(sum)
# elif not ifWorks:
#     print("The condition is false.")
# elif num1 > num2:
#     print("num1 is greater than num2.")
# else:
#     print("num2 is greater than num1.")
    
CodeLine: list = ["Atyab", "Fatma", "Ikhlas", "Kareem" , "Ishaq"]

startLetter = input("Enter startLetter to filter the list: ")
endLetter = input("Enter endLetter to filter the list: ")
result = list(filter(lambda x: x.startswith(startLetter), CodeLine))
result2 = list(filter(lambda x: x.endswith(endLetter), CodeLine))
print(result)
print(result2)