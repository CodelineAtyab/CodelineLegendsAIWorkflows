import requests

def main():
    currency = input("Enter currency code (e.g. ORM): ").upper()         
    response = requests.get(f"https://open.er-api.com/v6/latest/{currency}")

    result_dict = response.json()
    rates = result_dict.get("rates") 
    
    print ("Exchange rates for 1 " + currency + ":")
    
    for country_currency, rate in rates.items():
        print(f"{country_currency}: {rate}")

if __name__ == "__main__":
    main()
