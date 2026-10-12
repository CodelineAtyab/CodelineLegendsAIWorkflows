import requests

response = requests.get("https://api.nationalize.io/?name=sara")
data = response.json()          # JSON text -> Python dict (or list)
countries = data.get("country") # use .get() on a dict to read a key

def main():
    print("Hello from api-explorer!")


if __name__ == "__main__":
    main()
