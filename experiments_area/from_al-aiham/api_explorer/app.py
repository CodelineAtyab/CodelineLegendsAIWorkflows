import requests

name = input("Enter your Name: ")
def get_respones(name):
    response = requests.get("https://api.nationalize.io", params={"name":name})
    data = response.json()
    countries = data.get("country")

    print(f'Likely Countries for "{name}":')
    return countries

def display_respones(result):

    for i in range (len(result)):
        print(f"{i+1}. {result["country_id"]} - {result["probability"] * 100}")


if __name__ == "__main__":
    display_respones(get_respones(name))