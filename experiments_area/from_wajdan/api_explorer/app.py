import requests


def get_rates(currency):
    response = requests.get(
        f"https://open.er-api.com/v6/latest/{currency}"
    )
    return response.json()


def show_rates(currency, rates):
    print(f"Exchange rates for 1 {currency}:")

    for code in ["OMR", "USD", "EUR"]:
        rate = rates.get(code)
        print(f"{code:<5} {rate:>10.4f}")


def main():
    currency = input("Enter currency code (e.g. OMR): ").strip().upper()
    data = get_rates(currency)
    rates = data.get("rates")
    show_rates(currency, rates)


if __name__ == "__main__":
    main()