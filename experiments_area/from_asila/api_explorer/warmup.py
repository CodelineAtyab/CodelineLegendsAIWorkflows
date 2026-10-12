# List comprehension: multiply each number by 2
numbers = [1, 2, 3, 4, 5]

double_numbers = [number * 2 for number in numbers] #List comprehension its a short way to create a list using a loop in one line.

print(double_numbers)



# Dictionary comprehension
countries = [("Oman", "Muscat"), ("UAE", "Abu Dhabi"), ("France", "Paris")] #store countries and their capitals

capitals = {country: capital for country, capital in countries}

print(capitals)