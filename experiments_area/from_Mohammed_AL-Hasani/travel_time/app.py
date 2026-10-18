import json

import requests


# Reads API key from a text file.
def read_api_key() -> str:
    with open("api_key.txt", "r") as file:
        return file.read().strip()


# Sends the request to Google Routes API.
def get_travel_data(
    source: str,
    destination: str,
    api_key: str,
) -> dict:
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration",
    }

    body = {
        "origin": {"address": source},
        "destination": {"address": destination},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
    }

    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(body),
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


# Converts seconds into hours and minutes.
def format_time(seconds: float) -> str:
    total_minutes = round(seconds / 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60

    parts = []

    if hours > 0:
        hour_text = "hour" if hours == 1 else "hours"
        parts.append(f"{hours} {hour_text}")

    if minutes > 0 or hours == 0:
        minute_text = "minute" if minutes == 1 else "minutes"
        parts.append(f"{minutes} {minute_text}")

    return " ".join(parts)


# Controls the main program.
def main() -> None:
    try:
        key = read_api_key()
        source = input("Enter the source location: ")
        destination = input("Enter the destination location: ")

        data = get_travel_data(source, destination, key)

        routes = data.get("routes", [])

        if not routes:
            raise ValueError("No route found.")

        duration = routes[0].get("duration")

        if not duration:
            raise ValueError("Travel duration is unavailable.")

        seconds = float(duration[:-1])
        travel_time = format_time(seconds)

        print(
            f"Driving from {source} to {destination} "
            f"takes about {travel_time} with current traffic."
        )

    except (
        OSError,
        requests.RequestException,
        ValueError,
        TypeError,
        KeyError,
        IndexError,
    ) as e:
        print(f"Could not get the travel time: {e}")


if __name__ == "__main__":
    main()
