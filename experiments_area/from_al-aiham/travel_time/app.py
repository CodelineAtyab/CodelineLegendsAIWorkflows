
import requests


def read_api_key():
    with open("api_key.txt", "r", encoding="utf-8") as file:
        return file.read().strip()


def get_travel_time(source, destination, api_key):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    params = {
        "origins": source,
        "destinations": destination,
        "mode": "driving",
        "departure_time": "now",
        "key": api_key,
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()

    if data.get("status") != "OK":
        raise ValueError(
            data.get("error_message")
            or data.get("status", "Unknown API error")
        )

    rows = data.get("rows", [])

    if not rows or not rows[0].get("elements"):
        raise ValueError("No route was found.")

    route = rows[0]["elements"][0]

    if route.get("status") != "OK":
        raise ValueError(
            f"Route unavailable: {route.get('status')}"
        )

    traffic = route.get("duration_in_traffic")

    if not traffic or "value" not in traffic:
        raise ValueError("Traffic-aware travel time is unavailable.")

    return traffic["value"]


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

    except (OSError, ValueError, KeyError, IndexError, TypeError,
            requests.exceptions.RequestException) as error:
        print(f"Could not get the travel time: {error}")


if __name__ == "__main__":
    main()
