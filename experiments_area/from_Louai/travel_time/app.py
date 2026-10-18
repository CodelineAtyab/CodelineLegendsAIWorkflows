
import requests


def get_api_key(file_path="key.txt"):
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: The API key file '{file_path}' was not found.")
        print("Please set the MAPS_API_KEY environment variable or create the key file.")
        raise SystemExit(1)


def fetch_travel_time(source, destination, api_key):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters"
    }
    
    payload = {
        "origin": {"address": source},
        "destination": {"address": destination},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
       
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:

        print("Could not get the travel time due to a network or API error.")
        return None


def format_and_print_time(source, destination, data):
    if not data:
        return

    try:
        routes = data.get("routes")
        if not routes:
            print("Could not get the travel time: No route found")
            return


        duration_str = routes[0].get("duration", "0s")
        total_seconds = int(duration_str.rstrip("s"))


        total_minutes = round(total_seconds / 60)
        if total_minutes == 0 and total_seconds > 0:
            total_minutes = 1  # At least 1 minute if there are some seconds

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

        print(
            f"Driving from {source} to {destination} takes about {time_str} with current traffic."
        )

    except (ValueError, KeyError, TypeError):
        print("Could not get the travel time: Malformed response received from API.")


def main():
    try:
        source_place = input("Enter source: ").strip()
        dest_place = input("Enter destination: ").strip()

        if not source_place or not dest_place:
            print("Source and destination cannot be empty.")
            return

        api_key = get_api_key()
        api_data = fetch_travel_time(source_place, dest_place, api_key)
        format_and_print_time(source_place, dest_place, api_data)

    except (EOFError, KeyboardInterrupt):
        print("\nOperation cancelled.")


if __name__ == "__main__":
    main()