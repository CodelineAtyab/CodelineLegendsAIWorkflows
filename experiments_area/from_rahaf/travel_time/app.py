
import requests


# Read the API key from the file
def read_key():
    with open("api_key.txt", "r") as file:
        return file.read().strip()


# Convert a place name into coordinates
def get_location(city, key):
    city = requests.utils.quote(city, safe="")
    url = f"https://api.tomtom.com/search/2/geocode/{city}.json"

    response = requests.get(url, params={"key": key}, timeout=15)
    response.raise_for_status()
    data = response.json()

    results = data.get("results", [])

    if not results:
        raise ValueError("Location not found")

    position = results[0].get("position")

    return f"{position.get('lat')},{position.get('lon')}"


# Get driving time with current traffic
def get_travel_time(source, destination, key):
    start = get_location(source, key)
    end = get_location(destination, key)

    url = f"https://api.tomtom.com/routing/1/calculateRoute/{start}:{end}/json"

    params = {
        "key": key,
        "travelMode": "car",
        "traffic": "true",
        "departAt": "now",
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    return response.json()


# Convert seconds into hours and minutes
def format_time(data):
    seconds = data.get("routes")[0].get("summary").get("travelTimeInSeconds")

    minutes = int(seconds / 60 + 0.5)

    hours = minutes // 60
    remaining_minutes = minutes % 60

    if hours == 0:
        return f"{remaining_minutes} minutes"

    if hours == 1:
        return f"1 hour {remaining_minutes} minutes"

    return f"{hours} hours {remaining_minutes} minutes"


# Run the program
def main():
    source = input("Enter source: ")
    destination = input("Enter destination: ")

    try:
        key = read_key()
        data = get_travel_time(source, destination, key)
        time = format_time(data)

        print(
            f"Driving from {source} to {destination} "
            f"takes about {time} with current traffic."
        )

    except requests.exceptions.RequestException:
        print("Could not get the travel time: Check your internet connection or API key.")

    except (OSError, ValueError, KeyError, IndexError, TypeError, AttributeError) as error:
        print("Could not get the travel time:", str(error))


if __name__ == "__main__":
    main()
