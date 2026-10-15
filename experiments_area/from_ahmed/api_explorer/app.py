import requests

BASE_URL = "https://official-joke-api.appspot.com"
JOKE_TYPES = ["general", "programming", "knock-knock", "dad"]


def fetch_joke(joke_type):
    url = f"{BASE_URL}/jokes/{joke_type}/random"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    jokes = response.json()
    return jokes[0] if jokes else None


def print_joke(joke_data):
    print("\n" + "=" * 50)
    if joke_data is None:
        print("No joke found for that type.")
    else:
        print("JOKE:")
        print(joke_data.get("setup"))
        print("\n" + joke_data.get("punchline"))
    print("=" * 50 + "\n")


def main():
    print("Joke types:", ", ".join(JOKE_TYPES))
    joke_type = input("Pick a joke type: ").strip().lower()
    try:
        joke = fetch_joke(joke_type)
    except requests.RequestException as error:
        print(f"Could not fetch joke: {error}")
        return
    print_joke(joke)


if __name__ == "__main__":
    main()
