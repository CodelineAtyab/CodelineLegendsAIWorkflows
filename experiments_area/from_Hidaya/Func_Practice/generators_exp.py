def normal_range(start, end):
    count = start
    while count <= end:
        return count
        count += 1
    
res = normal_range(1, 3)
print(res)  
res = normal_range(1, 3)
print(res)  
res = normal_range(1, 3)
print(res)  
print("************")  
def my_range(start, end):
    current = start
    while current <= end:
        yield current
        current += 1
    
gen=my_range(1, 3) #just returns the geenerator object that we can use later 
res=next(gen) # call for the first time 
print(res) 
res=next(gen) # call for the second time
print(res)
res=next(gen) # call for the third time
print(res)

