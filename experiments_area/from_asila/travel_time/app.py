import requests
from requests.exceptions import RequestException


# read the Google API key from a local file.
def read_api_key():
    with open("api_key.txt", "r", encoding="utf-8") as file:
        return file.read().strip()


# request driving time with current traffic.
# This function asks Google for the driving time between two places, including traffic.
def get_travel_time(source, destination, api_key):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    headers = {  # here header includes your API key and the fields you want back.
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration",
    }

    data_to_send = {
        "origin": {"address": source},
        "destination": {"address": destination},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
    }

    response = requests.post(
        url,
        headers=headers,
        json=data_to_send,  # sends data as JSON.
        timeout=30,  # limits how long it waits for a connection or data.
    )

    if not response.ok:
        error = response.json().get("error", {})
        message = error.get("message", f"HTTP {response.status_code}")
        raise ValueError(message)

    data = response.json()
    routes = data.get("routes", [])

    if not routes:
        raise ValueError("No driving route was found")

    return routes[0]["duration"]


# Convert seconds into hours and minutes.
def format_duration(duration):
    total_seconds = float(duration[:-1])
    total_minutes = int(total_seconds / 60 + 0.5)

    hours = total_minutes // 60
    minutes = total_minutes % 60

    parts = []

    if hours:
        unit = "hour" if hours == 1 else "hours"
        parts.append(f"{hours} {unit}")

    if minutes:
        unit = "minute" if minutes == 1 else "minutes"
        parts.append(f"{minutes} {unit}")

    return " ".join(parts) if parts else "0 minutes"


def main():
    source = input("Enter starting place: ")
    destination = input("Enter destination: ")

    if not source or not destination:
        print("Could not get the travel time: Enter both places")
        return
    
    try:
        api_key = read_api_key()
        duration = get_travel_time(source, destination, api_key)
        travel_time = format_duration(duration)

        print(
            f"Driving from {source} to {destination} takes about "
            f"{travel_time} with current traffic."
        )

    except RequestException:
        print("Could not get the travel time: Google API or network request failed")

    except (OSError, KeyError, IndexError, ValueError, TypeError) as error:
        print(f"Could not get the travel time: {error}")


if __name__ == "__main__":
    main()
