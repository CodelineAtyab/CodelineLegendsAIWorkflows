import requests

def fetch_nationality(name):
    url = f"https://api.nationalize.io/?name={name}"
    response = requests.get(url)
    return response.json()


def print_results(name, data):
    countries = data.get('country', [])
    print(f'nLikely countries for the name "{name}":')
    if not countries:
        print("No data available.")
        return

    for index, item in enumerate(countries, start=1):
        country_id = item.get('country_id')
        probability = item.get('probability', 0.0) * 100
        print(f"{index}. Country: {country_id}, Probability: {probability:.1f}%")

    if __name__ == "__main__":
        name = input("Enter a name: ")
        data = fetch_nationality(name)
        print_results(name, data)


import requests

name = input("Enter a name to guess age: ")
response = requests.get(f"https://api.agify.io/?name={name}")
data = response.json()

age = data.get("age")
count = data.get("count")
print(f"Name: {name}, Estimated Age: {age}, Based on {count} samples.")

 