import requests

def main():
    user_name = input("Enter your name: ")
    response = requests.get("https://api.nationalize.io/?name=" + user_name)
    result_dict = response.json()

    list_of_countries = result_dict.get("country")

    for curr_country in list_of_countries:
        print(curr_country.get("country_id"))

if __name__ == "__main__":
    main()