import requests


def read_api_key():
    # Read the secret key from a local file so it is not committed to GitHub.
    with open("api_key.txt", "r") as file:
        api_key = file.read().strip()

    if not api_key:
        raise ValueError("API key file is empty")

    return api_key


def get_coordinates(place, api_key):
    # TomTom Search API converts a place name into latitude and longitude.
    url = f"https://api.tomtom.com/search/2/geocode/{place}.json"

    params = {
        "key": api_key,
        "limit": 1,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    results = data.get("results", [])
    if not results:
        raise ValueError(f"Could not find location: {place}")

    position = results[0]["position"]
    return position["lat"], position["lon"]


def get_travel_data(source, destination, api_key):
    # The Routing API needs coordinates, so first look up both places.
    source_lat, source_lon = get_coordinates(source, api_key)
    destination_lat, destination_lon = get_coordinates(destination, api_key)

    # Request a car route and include current traffic in the travel time.
    locations = f"{source_lat},{source_lon}:{destination_lat},{destination_lon}"
    url = f"https://api.tomtom.com/routing/1/calculateRoute/{locations}/json"

    params = {
        "travelMode": "car",
        "traffic": "true",
        "computeTravelTimeFor": "all",
        "key": api_key,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def extract_travel_seconds(data):
    # Read the traffic-aware travel time from TomTom's nested JSON response.
    routes = data.get("routes", [])
    if not routes:
        raise ValueError("Could not find route")

    summary = routes[0]["summary"]
    return summary["liveTrafficIncidentsTravelTimeInSeconds"]


def format_time(seconds):
    # Convert seconds into the exact hours/minutes wording required by the task.
    minutes = round(seconds / 60)
    hours = minutes // 60
    remaining_minutes = minutes % 60

    if hours == 0:
        return f"{minutes} minutes"

    hour_word = "hour" if hours == 1 else "hours"

    if remaining_minutes == 0:
        return f"{hours} {hour_word}"

    return f"{hours} {hour_word} {remaining_minutes} minutes"


def main():
    try:
        api_key = read_api_key()

        source = input("Source: ")
        destination = input("Destination: ")

        data = get_travel_data(source, destination, api_key)
        seconds = extract_travel_seconds(data)
        travel_time = format_time(seconds)

        print(
            f"Driving from {source} to {destination} takes about "
            f"{travel_time} with current traffic."
        )

    except (OSError, ValueError, KeyError, IndexError, requests.RequestException) as error:
        print(f"Could not get the travel time: {error}")


if __name__ == "__main__":
    main()
