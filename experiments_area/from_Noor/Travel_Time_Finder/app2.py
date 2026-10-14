
import requests


# Read the Google Maps API key from a local file.
def read_api_key():
    with open("api_key2.txt", "r", encoding="utf-8") as file:
        return file.read().strip()


# Get the driving time using traffic-aware routing.
def fetch_travel_time(source, destination, api_key):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration,routes.staticDuration"
    }

    body = {
        "origin": {
            "address": source
        },
        "destination": {
            "address": destination
        },
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE"
    }

    response = requests.post(
        url,
        headers=headers,
        json=body,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()
    routes = data.get("routes", [])

    if not routes:
        raise ValueError("No driving route was found.")

    # Google returns duration as text, for example "7800s".
    duration = routes[0]["duration"]

    return float(duration.removesuffix("s"))


# Convert seconds into a readable time.
def format_time(seconds):
    total_minutes = round(seconds / 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60

    if hours == 0:
        return f"{minutes} minutes"

    hour_word = "hour" if hours == 1 else "hours"

    if minutes == 0:
        return f"{hours} {hour_word}"

    return f"{hours} {hour_word} {minutes} minutes"


# Run the application.
def main():
    source = input("Enter the starting place: ").strip()
    destination = input("Enter the destination: ").strip()

    if not source or not destination:
        print("Please enter both places.")
        return

    try:
        api_key = read_api_key()

        if not api_key:
            print("Could not get the travel time: API key is empty.")
            return

        seconds = fetch_travel_time(source, destination, api_key)
        travel_time = format_time(seconds)

        print(
            f"Driving from {source} to {destination} takes "
            f"about {travel_time} with current traffic."
        )

    except requests.RequestException as error:
        print(f"Could not get the travel time: {error}")

    except (ValueError, KeyError) as error:
        print(f"Could not get the travel time: {error}")

    except OSError:
        print("Could not get the travel time: Could not read api_key2.txt.")


if __name__ == "__main__":
    main()
