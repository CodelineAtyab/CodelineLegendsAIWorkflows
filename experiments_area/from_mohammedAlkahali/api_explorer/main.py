import requests

def main():
    country_name = input("Enter the country name: ")
    response = requests.get(f"http://universities.hipolabs.com/search?country={country_name}")
    data = response.json()

    for university in data:
        print(f"Name: {university['name']}")




if __name__ == "__main__":
    main()
