import requests


def get_ip_info(ip_address):
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    response.raise_for_status()
    return response.json()


def display_data(data):
    print("==============================================")
    print(f"IP Address: {data.get('ip')}")
    print(f"City: {data.get('city')}")
    print(f"Region: {data.get('region')}")
    print(f"Country: {data.get('country')}")
    print(f"Location: {data.get('loc')}")
    print(f"Organization: {data.get('org')}")
    print(f"Postal Code: {data.get('postal')}")
    print(f"Timezone: {data.get('timezone')}")
    print("==============================================")


if __name__ == "__main__":
    ip_address = input("Enter a public IP address: ")
    data = get_ip_info(ip_address)
    display_data(data)
