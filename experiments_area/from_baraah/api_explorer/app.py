import requests

# get prayer times
def get_prayers(city):
    response = requests.get(f"https://api.aladhan.com/v1/timingsByCity?city={city}&country=Oman" )

    return response.json()


# display prayer times
def show_prayers(data):
    times = data.get("data").get("timings")

    print("Fajr:", times.get("Fajr"))
    print("Dhuhr:", times.get("Dhuhr"))
    print("Asr:", times.get("Asr"))
    print("Maghrib:", times.get("Maghrib"))
    print("Isha:", times.get("Isha"))


# Run 
def main():
    city = input("Enter city in Oman: ")
    show_prayers(get_prayers(city))


if __name__ == "__main__":
    main()