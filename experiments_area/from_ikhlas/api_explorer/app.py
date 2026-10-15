import requests


def fetch_api(name):
    response_result = requests.get("https://api.agify.io", params={"name": name})

    print("Status code:", response_result.status_code)
    data = response_result.json()
    return data


def main():
    name = input("Enter your name: ")
    data = fetch_api(name)

    print("Name:", data.get("name"))
    print("Estimated age:", data.get("age"))


if __name__ == "__main__":
    main()
