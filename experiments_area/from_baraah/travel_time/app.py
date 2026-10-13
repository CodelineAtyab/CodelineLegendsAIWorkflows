import requests


# read API key from file
def read_key():
    with open("api_key.txt", "r") as file:
        return file.read().strip()


# convert city name into coordinates
def get_location(city, key):
    url = f"https://api.tomtom.com/search/2/geocode/{city}.json"
    data = requests.get(url, params={"key": key}).json()
    position = data["results"][0]["position"]

    return f"{position['lat']},{position['lon']}"


# get time with current traffic
def get_travel_time(source, destination, key):
    start = get_location(source, key)
    end = get_location(destination, key)

    url = f"https://api.tomtom.com/routing/1/calculateRoute/{start}:{end}/json"

    params = {"key": key, "travelMode": "car", "traffic": "true", "departAt": "now"}

    return requests.get(url, params=params).json()


# convert seconds to hours and minutes
def format_time(seconds):
    total = (seconds + 30) // 60
    hours = total // 60
    minutes = total % 60

    if hours == 0:
        return f"{minutes} minutes"
    if minutes == 0:
        return f"{hours} hour" if hours == 1 else f"{hours} hours"

    return f"{hours} hours {minutes} minutes"


# run
def main():
    source = input("Enter source: ")
    destination = input("Enter destination: ")

    try:
        key = read_key()
        data = get_travel_time(source, destination, key)
        seconds = data["routes"][0]["summary"]["travelTimeInSeconds"]

        print(
            f"Driving from {source} to {destination} takes about {format_time(seconds)} with current traffic."
        )

    except Exception as e:
        print("Could not get the travel time:", e)


if __name__ == "__main__":
    main()
