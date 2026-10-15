import requests


def get_ip_info(ip):
    response = requests.get(
        f"https://ipapi.co/{ip}/json/",
        timeout=10,
    )
    return response.json()


def main():
    name = input("Enter your name: ")
    ip = input("Enter an IP address (e.g. 8.8.8.8): ")

    data = get_ip_info(ip)

    
    if data.get("error"):
        print("\nError:", data.get("reason"))
        return

    print("\nHello,", name)
    print("IP:", data.get("ip"))
    print("City:", data.get("city"))
    print("Region:", data.get("region"))
    print("Country:", data.get("country_name"))
    print("Timezone:", data.get("timezone"))
    print("Currency:", data.get("currency"))
    print("Organization:", data.get("org"))


if __name__ == "__main__":
    main()