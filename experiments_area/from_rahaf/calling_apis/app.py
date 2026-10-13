
import requests


# Get cat facts from API
def get_cat_facts(number):
    url = f"https://catfact.ninja/facts?limit={number}"

    response = requests.get(url)

    return response.json()

# Show cat fact
def show_results(data):
    facts = data.get("data", [])

    for index, cat in enumerate(facts, start=1):
        fact = cat.get("fact")
        length = cat.get("length")

        print(f"{index}. {fact}")
        print(f"Length: {length} characters")
        print()


# Run the program
def main():
    number = input("How many cat facts do you want? ")

    data = get_cat_facts(number)

    show_results(data)


if __name__ == "__main__":
    main()
