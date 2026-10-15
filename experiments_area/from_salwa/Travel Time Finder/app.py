import requests


def read_api_key():
    with open("api_key.txt", "r") as file:
        api_key = file.read().strip()

    return api_key


def get_coordinates(place, api_key):
    url = f"https://api.tomtom.com/search/2/geocode/{place}.json"

    params = {
        "key": api_key,
        "countrySet": "OM",
        "limit": 1,
    }

    response = requests.get(url, params=params, timeout=15)

    if response.status_code != 200:
        print("HTTP status:", response.status_code)
        print("TomTom error:", response.text)
        raise ValueError("TomTom API request failed")

    data = response.json()
    results = data.get("results", [])

    if not results:
        raise ValueError(f"Location not found: {place}")

    position = results[0]["position"]

    return position["lat"], position["lon"]


def get_travel_data(source, destination, api_key):
    source_lat, source_lon = get_coordinates(source, api_key)
    destination_lat, destination_lon = get_coordinates(destination, api_key)

    locations = f"{source_lat},{source_lon}:{destination_lat},{destination_lon}"

    url = f"https://api.tomtom.com/routing/1/calculateRoute/{locations}/json"

    params = {
        "key": api_key,
        "traffic": "true",
        "departAt": "now",
        "travelMode": "car",
    }

    response = requests.get(url, params=params, timeout=15)

    if response.status_code != 200:
        print("HTTP status:", response.status_code)
        print("TomTom error:", response.text)
        raise ValueError("TomTom routing request failed")

    data = response.json()
    routes = data.get("routes", [])

    if not routes:
        raise ValueError("No route was found")

    return routes[0]["summary"]


def format_travel_time(summary):
    seconds = summary["travelTimeInSeconds"]
    total_minutes = round(seconds / 60)

    hours = total_minutes // 60
    minutes = total_minutes % 60

    if hours == 0:
        return f"{minutes} minutes"

    if minutes == 0:
        return f"{hours} hours"

    return f"{hours} hours {minutes} minutes"


def main():
    try:
        api_key = read_api_key()

        source = input("Enter starting place: ")
        destination = input("Enter destination: ")

        summary = get_travel_data(source, destination, api_key)

        travel_time = format_travel_time(summary)
        distance_km = summary["lengthInMeters"] / 1000

        print(f"Distance: {distance_km:.1f} km")
        print(
            f"Driving from {source} to {destination} "
            f"takes about {travel_time} with current traffic."
        )

    except requests.exceptions.RequestException as error:
        print(f"Could not get the travel time: {error}")

    except (ValueError, KeyError, IndexError, TypeError) as error:
        print(f"Could not process the travel data: {error}")

    except OSError as error:
        print(f"Could not read the API key file: {error}")


if __name__ == "__main__":
    main()
