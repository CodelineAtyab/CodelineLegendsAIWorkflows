from pathlib import Path

import requests

API_KEY_FILE = Path(__file__).with_name("api_key_file.txt")
ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"


def get_api_key():
    return API_KEY_FILE.read_text(encoding="utf-8").strip()


def get_route_response(source, destination):
    api_key = get_api_key()
    response = requests.post(
        ROUTES_URL,
        json={
            "origin": {"address": source},
            "destination": {"address": destination},
            "travelMode": "DRIVE",
            "routingPreference": "TRAFFIC_AWARE",
        },
        headers={
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "routes.duration",
        },
        timeout=30,
    )
    return response.json()


def get_travel_time(data):
    duration = data["routes"][0]["duration"]
    seconds = float(duration[:-1])
    total_minutes = round(seconds / 60)
    hours, minutes = divmod(total_minutes, 60)

    minute_text = "minute" if minutes == 1 else "minutes"

    if hours == 0:
        return f"{minutes} {minute_text}"

    hour_text = "hour" if hours == 1 else "hours"

    if minutes == 0:
        return f"{hours} {hour_text}"

    return f"{hours} {hour_text} {minutes} {minute_text}"


def main():
    source = input("Enter the source: ").strip()
    destination = input("Enter the destination: ").strip()

    if not source or not destination:
        print("Please enter both a source and a destination.")
        return

    try:
        data = get_route_response(source, destination)

        if "error" in data:
            print(f"Could not get the travel time: {data['error']['message']}")
        elif not data.get("routes"):
            print("Could not get the travel time: no driving route was found")
        else:
            travel_time = get_travel_time(data)
            print(
                f"Driving from {source} to {destination} "
                f"takes about {travel_time} with current traffic."
            )

    except (
        OSError,
        requests.RequestException,
        KeyError,
        IndexError,
        TypeError,
        ValueError,
    ) as error:
        print(f"Could not get the travel time: {error}")


if __name__ == "__main__":
    main()
