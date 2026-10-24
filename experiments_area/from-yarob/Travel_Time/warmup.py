cities = ["muscat", "nizwa", "sohar", "salalah", "sur"]


capitalized_cities = [city.capitalize() for city in cities]
print(capitalized_cities)


city_name_lengths = {city: len(city) for city in cities}
print(city_name_lengths)