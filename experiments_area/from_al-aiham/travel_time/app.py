from urllib.parse import quote

import requests

def read_api_key():
    with open("api_key.txt", "r", encoding="utf-8") as file:
        api_key = file.read().strip()

    if not api_key:
        raise ValueError("API key is empty.")

    return api_key

def get_coordinates(city, api_key):
    city_encoded = quote(city, safe="")

    url = (
        f"https://api.tomtom.com/search/2/"
        f"search/{city_encoded}.json"
    )

    params = {
        "key": api_key,
        "limit": 1,
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()
    results = data.get("results", [])

    if not results:
        raise ValueError(f"Location '{city}' was not found.")

    position = results[0].get("position", {})

    latitude = position.get("lat")
    longitude = position.get("lon")

    if latitude is None or longitude is None:
        raise ValueError(f"Coordinates unavailable for '{city}'.")

    return latitude, longitude

def get_travel_time(source, destination, api_key):
    source_lat, source_lon = get_coordinates(source, api_key)
    dest_lat, dest_lon = get_coordinates(destination, api_key)

    locations = (
        f"{source_lat},{source_lon}:"
        f"{dest_lat},{dest_lon}"
    )

    url = (
        "https://api.tomtom.com/routing/1/"
        f"calculateRoute/{locations}/json"
    )

    params = {
        "key": api_key,
        "travelMode": "car",
        "traffic": "true",
        "departAt": "now",
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()
    routes = data.get("routes", [])

    if not routes:
        raise ValueError("No driving route was found.")

    summary = routes[0].get("summary", {})
    seconds = summary.get("travelTimeInSeconds")

    if seconds is None:
        raise ValueError("Traffic-aware travel time is unavailable.")

    return seconds

def format_duration(seconds):
    total_minutes = int(seconds / 60 + 0.5)

    hours = total_minutes // 60
    minutes = total_minutes % 60

    parts = []

    if hours > 0:
        hour_label = "hour" if hours == 1 else "hours"
        parts.append(f"{hours} {hour_label}")

    if minutes > 0 or hours == 0:
        minute_label = "minute" if minutes == 1 else "minutes"
        parts.append(f"{minutes} {minute_label}")

    return " ".join(parts)

def main():
    try:
        api_key = read_api_key()

        source = input("Enter source: ").strip()
        destination = input("Enter destination: ").strip()

        if not source or not destination:
            raise ValueError("Source and destination cannot be empty.")

        seconds = get_travel_time(source, destination, api_key)

        duration = format_duration(seconds)

        print(
            f"Driving from {source} to {destination} "
            f"takes about {duration} with current traffic."
        )

    except FileNotFoundError:
        print("Could not get the travel time: api_key.txt not found.")

    except requests.exceptions.RequestException as error:
        print(f"Could not get the travel time: {error}")

    except (ValueError, KeyError, IndexError, TypeError) as error:
        print(f"Could not get the travel time: {error}")

    except OSError as error:
        print(f"Could not get the travel time: {error}")


if __name__ == "__main__":
    main()
