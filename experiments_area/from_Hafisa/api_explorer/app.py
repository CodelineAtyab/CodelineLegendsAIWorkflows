import requests


def get_nationality(name):
    url = f"https://api.nationalize.io/?name={name}"

    response = requests.get(url)

    return response.json()


def show_results(data):
    name = data.get("name")
    countries = data.get("country")

    print(f'Likely countries for "{name}":')

    for index, country in enumerate(countries, start=1):
        country_name = country.get("country_id")
        probability = country.get("probability") * 100

        print(f"{index}. {country_name} - {probability:.1f}%")


def main():
    name = input("Enter a name: ")

    data = get_nationality(name)

    show_results(data)


if __name__ == "__main__":
    main()
