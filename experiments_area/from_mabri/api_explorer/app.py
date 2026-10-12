import requests




if __name__ == "__main__":
    ip_address = input("Enter a public IP address: ")
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    response.raise_for_status()
    data = response.json()
    print(data)