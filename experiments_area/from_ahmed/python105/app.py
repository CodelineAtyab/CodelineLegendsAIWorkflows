import requests

def fetch_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    data = response.json()
    return data

def print_joke(joke_data):
    setup = joke_data.get("setup")
    punchline = joke_data.get("punchline")
    
    print("\n" + "=" * 50)
    print("JOKE:")
    print(setup)
    print("\n" + punchline)
    print("=" * 50 + "\n")

if __name__ == "__main__":
    joke = fetch_joke()
    print_joke(joke)
