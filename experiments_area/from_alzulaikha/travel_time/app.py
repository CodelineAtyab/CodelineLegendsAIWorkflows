
import requests
from requests.exceptions import RequestException


def read_api_key():
    with open("api_key.txt", "r", encoding="utf-8") as file:
        return file.read().strip()


def get_travel_time(source, destination, api_key):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration,routes.staticDuration",
    }

    params = {
        "origin": {
            "address": source
        },
        "destination": {
            "address": destination
        },
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
        "departureTime": "now",
    }

    response = requests.post(
        url,
        headers=headers,
        json=params,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()
    return data["routes"][0]["duration"]


def format_duration(duration):
    total_seconds = int(duration.removesuffix("s"))
    total_minutes = round(total_seconds / 60)

    hours = total_minutes // 60
    minutes = total_minutes % 60

    parts = []

    if hours:
        unit = "hour" if hours == 1 else "hours"
        parts.append(f"{hours} {unit}")

    if minutes:
        parts.append(f"{minutes} minutes")

    return " ".join(parts) if parts else "0 minutes"


def main():
    source = input("Enter starting place: ")
    destination = input("Enter destination: ")

    try:
        api_key = read_api_key()
        duration = get_travel_time(source, destination, api_key)
        travel_time = format_duration(duration)

        print(
            f"Driving from {source} to {destination} takes about "
            f"{travel_time} with current traffic."
        )

    except (RequestException, FileNotFoundError, KeyError, IndexError, ValueError) as error:
        print(f"Could not get the travel time: {error!s}")


if __name__ == "__main__":
    main()
