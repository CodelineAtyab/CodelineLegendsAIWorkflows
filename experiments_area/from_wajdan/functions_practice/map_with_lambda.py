data =[1,2,3,4,5,6,7,8,9,10 ]
result=[]

#for num in data:
#      result.append(num*num)
#print(result)   
result = list(map(lambda num: num*num, data))
print(result)
