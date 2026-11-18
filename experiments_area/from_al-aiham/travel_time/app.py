
import requests


def read_api_key():
    with open("api_key.txt", "r", encoding="utf-8") as file:
        return file.read().strip()


def get_travel_time(source, destination, api_key):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration",
    }

    data = {
        "origin": {"address": source},
        "destination": {"address": destination},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=15,
    )

    response.raise_for_status()

    result = response.json()
    routes = result.get("routes", [])

    if not routes:
        raise ValueError("No driving route was found.")

    duration = routes[0].get("duration")

    if duration is None:
        raise ValueError("Travel time is unavailable.")

    return float(duration.removesuffix("s"))


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

    except (
        OSError,
        ValueError,
        KeyError,
        IndexError,
        TypeError,
        requests.exceptions.RequestException,
    ) as error:
        print(f"Could not get the travel time: {error}")


if __name__ == "__main__":
    main()
