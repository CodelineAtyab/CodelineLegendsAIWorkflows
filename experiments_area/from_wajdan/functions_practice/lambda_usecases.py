#def connect_to_database():
  # pass
connect_to_database = lambda :None
sum = lambda num1, num2: num1 + num2
sum(1,2)
connect_to_database()

data = [1,2,7,6,45,100]
#filter()
filtered_list =[]
for num in data:
    if num %2 == 0:
        filtered_list.append(num)
        print(filtered_list)
                    
                    