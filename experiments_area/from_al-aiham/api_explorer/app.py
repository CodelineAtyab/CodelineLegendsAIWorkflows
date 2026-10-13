import requests


def get_response(name):
    response = requests.get("https://api.nationalize.io", params={"name": name})
    data = response.json()
    countries = data.get("country")

    return countries


def display_response(result):

    for i in range(len(result)):
        print(
            f"{i + 1}. {result[i]['country_id']} - {result[i]['probability'] * 100:.2f}%"
        )


def main():
    name = input("Enter your Name: ")

    print(f'\nLikely Countries for "{name}":')

    result = get_response(name)
    display_response(result)


if __name__ == "__main__":
    main()
