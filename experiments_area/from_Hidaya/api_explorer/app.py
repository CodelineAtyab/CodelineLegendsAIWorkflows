import requests


def fetch_data(name):
    response = requests.get("https://api.agify.io/", params={"name": name})
    return response.json()


def print_prediction(data):
    name = data.get("name")
    age = data.get("age")
    count = data.get("count")
    print("\nAge Prediction")
    print("----------------------------")
    print(f"Name: {name}")
    print(f"Predicted age: {age} years")
    print(f"Number of records: {count}")


def main():
    name = input("Enter your name: ")
    data = fetch_data(name)
    print_prediction(data)


if __name__ == "__main__":
    main()
