import requests


def get_universities(country_name):
    url = "http://universities.hipolabs.com/search"
    try:
        response = requests.get(url, params={"country": country_name})
        return response.json()
    except requests.RequestException as e:
        print(f"Error occurred while making the API request: {e}")
        return []


def show_universities(universities):
    if not universities:
        print("No universities found.")
        return

    for index, university in enumerate(universities, start=1):
        name = university.get("name")
        country = university.get("country")
        print(f"{index}. {name} ({country})")


def main():
    country_name = input("Enter a country name: ")
    universities = get_universities(country_name)
    show_universities(universities)


if __name__ == "__main__":
    main()