import requests

def main():
    
    currency = input("Enter currency code (e.g. OMR): ").upper()         
    response = requests.get(f"https://open.er-api.com/v6/latest/{currency}")

    result_dict = response.json()
    rates = result_dict.get("rates") 
    
    print ("Exchange rates for 1 " + currency + ":")
    
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





