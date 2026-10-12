import requests

def main():
    currency = input("Enter currency code (e.g. OMR): ").upper()

    try:
        response = requests.get(
            f"https://open.er-api.com/v6/latest/{currency}",
           
        )
        response.raise_for_status()
        result_dict = response.json()

    except requests.exceptions.RequestException:
        print("Could not get valid data from the API.")
        return

    rates = result_dict.get("rates")

    if rates is None:
        print("Invalid currency code. Enter OMR or USD.")
        return

    print("Exchange rates for 1 " + currency + ":")

    for country_currency, rate in rates.items():
        print(f"{country_currency}: {rate}")

    # #-----name API
    # name = input("Enter your name: ")
    # response = requests.get(f"https://api.nationalize.io/?name={name}")
    # result_dict = response.json()
    # countries = result_dict.get("country")

    # for country in countries:
    #     print(country.get("country_id"))

if __name__ == "__main__":
    main()





