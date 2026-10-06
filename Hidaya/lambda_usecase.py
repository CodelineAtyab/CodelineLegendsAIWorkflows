#lambda function is a small anonymous function that can take any number of arguments, but can only have one expression. 
# It is often used for short, simple functions that are not reused elsewhere in the code.

connect_to_db = lambda: None
# it is same this function :
# def connect_to_db():
    #return None

sum = lambda num1, num2: num1 + num2
# it is same this function :
# def sum(num1, num2):
    # return num1 + num2

print(sum(1,2))
print(connect_to_db()) 

data = [11, 2, 3, 12, 6, 7, 3, 9, 45, 100]
filtered_list = list(filter(lambda num: num%2 == 0 , data))
print(filtered_list)

#The same function 
#filtered_list = [] 
#for num in data:
    #if num % 2 == 0:
        #filtered_list.append(num)
