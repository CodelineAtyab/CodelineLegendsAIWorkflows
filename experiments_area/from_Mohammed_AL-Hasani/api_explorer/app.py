
# mypy: explicit_package_bases

import requests


def get_joke():
    response = requests.get(
        "https://official-joke-api.appspot.com/random_joke"
    )
    return response.json()


def main():
    name = input("Enter your name: ")

    data = get_joke()

    print("\nHello,", name)
    print("Joke category:", data.get("type"))
    print("Question:", data.get("setup"))
    print("Answer:", data.get("punchline"))
    print("Joke ID:", data.get("id"))


if __name__ == "__main__":
    main()