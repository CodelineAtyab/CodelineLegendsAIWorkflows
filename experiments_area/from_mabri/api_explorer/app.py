import requests


def get_ip_info(ip_address):
    response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    ip_address = input("Enter a public IP address: ")
    data = get_ip_info(ip_address)
    print(data)