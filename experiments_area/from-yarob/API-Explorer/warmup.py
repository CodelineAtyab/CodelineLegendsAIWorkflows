countries = ["Oman", "Egypt", "UAE", "Tunisia", "Morocco"]


upper_countries = [country.upper() for country in countries]
print(upper_countries)


country_name_lengths = {country: len(country) for country in countries}
print(country_name_lengths)