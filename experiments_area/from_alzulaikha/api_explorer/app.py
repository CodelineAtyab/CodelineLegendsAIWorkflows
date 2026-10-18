## Get a first name and fetch nationality predictions from the API
import requests

# name = input("Enter a first name: ")

# response = requests.get(
#     "https://api.nationalize.io/",
#     params={"name": name},
# )

# data = response.json()

# print(data)
# countries = data.get("country", [])
# print(countries)

# filtered_countries = [
#     country for country in countries
#     if country["probability"] >= 0.05
# ]

# response = requests.get(
#     "https://official-joke-api.appspot.com/random_joke"
# )

# data = response.json()

# print(data)



# Fetch a random joke from the API
def get_random_joke(category):
    response = requests.get(
        f"https://official-joke-api.appspot.com/jokes/{category}/random"
    )
    data = response.json()
    return data


# Print the joke details
def display_joke(data):
    print("\n🎭 Random Joke")
    print(f"Setup: {data['setup']}")
    print(f"Punchline: {data['punchline']}")


# Run the program
def main():
    category = input(
        "Choose a category (general, programming, knock-knock): "
    )
    jokes = get_random_joke(category)

    if isinstance(jokes, list):
        display_joke(jokes[0])
    else:
        display_joke(jokes)


if __name__ == "__main__":
    main()