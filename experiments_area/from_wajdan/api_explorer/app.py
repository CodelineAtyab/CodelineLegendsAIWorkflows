import requests


def get_rates(currency):
    response = requests.get(
        f"https://open.er-api.com/v6/latest/{currency}"
    )
    return response.json()


def print_rates(data):
    currency = data.get("base_code")
    rates = data.get("rates")

    print("Exchange rates for 1 " + currency + ":")

    for country_currency, rate in rates.items():
        print(f"{country_currency}: {rate}")


def main():
    currency = input("Enter currency code (e.g. OMR): ").strip().upper()
    data = get_rates(currency)
    print_rates(data)


if __name__ == "__main__":
    main()