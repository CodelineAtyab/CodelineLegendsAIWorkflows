
import os
import requests


API_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"


def get_api_key(file_path="key.txt"):
    """Read the API key from an environment variable or a file."""

    api_key = os.getenv("MAPS_API_KEY")

    if api_key and api_key.strip():
        return api_key.strip()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            api_key = file.read().strip()

            if api_key:
                return api_key

            print("Error: The API key file is empty.")

    except FileNotFoundError:
        print(f"Error: The API key file '{file_path}' was not found.")

    print(
        "Please set MAPS_API_KEY or create a key.txt file "
        "containing your Google API key."
    )
    raise SystemExit(1)


def fetch_travel_time(source, destination, api_key):
    """Request driving time and distance from Google Routes API."""

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters",
    }

    payload = {
        "origin": {"address": source},
        "destination": {"address": destination},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as error:
        print(f"Google API HTTP error: {error}")
        print(f"Response details: {response.text}")
        return None

    except requests.exceptions.RequestException as error:
        print(f"Network error: {error}")
        return None


def format_and_print_route(source, destination, data):
    """Display the route duration and distance."""

    if not data:
        return

    try:
        routes = data.get("routes", [])

        if not routes:
            print("No route found between these locations.")
            return

        route = routes[0]

        duration_str = route.get("duration")

        if not duration_str or not duration_str.endswith("s"):
            print("Error: Google returned an invalid duration.")
            return

        total_seconds = int(duration_str[:-1])

        if total_seconds < 0:
            print("Error: Google returned an invalid duration.")
            return

        total_minutes = round(total_seconds / 60)

        if total_minutes == 0 and total_seconds > 0:
            total_minutes = 1

        hours = total_minutes // 60
        minutes = total_minutes % 60

        time_parts = []

        if hours > 0:
            hour_word = "hour" if hours == 1 else "hours"
            time_parts.append(f"{hours} {hour_word}")

        if minutes > 0 or hours == 0:
            minute_word = "minute" if minutes == 1 else "minutes"
            time_parts.append(f"{minutes} {minute_word}")

        time_str = " ".join(time_parts)

        distance_meters = route.get("distanceMeters")

        print("\n--- Google Routes Result ---")
        print(f"From: {source}")
        print(f"To: {destination}")
        print(f"Estimated driving time: {time_str}")

        if distance_meters is not None:
            distance_km = distance_meters / 1000
            print(f"Distance: {distance_km:.1f} km")

        print("----------------------------")

    except (ValueError, KeyError, TypeError) as error:
        print(f"Could not process Google's response: {error}")


def main():
    try:
        source = input("Enter source: ").strip()
        destination = input("Enter destination: ").strip()

        if not source or not destination:
            print("Error: Source and destination cannot be empty.")
            return

        api_key = get_api_key()

        data = fetch_travel_time(
            source,
            destination,
            api_key,
        )

        format_and_print_route(source, destination, data)

    except (EOFError, KeyboardInterrupt):
        print("\nOperation cancelled.")


if __name__ == "__main__":
    main()
