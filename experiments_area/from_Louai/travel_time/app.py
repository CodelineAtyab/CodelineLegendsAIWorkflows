import requests


def read_api_key(file_path="key.txt"):
    # Read the API key from a file
    with open(file_path, "r") as file:
        return file.read().strip()


def fetch_travel_time(source, destination, api_key):

    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": source,
        "destination": destination,
        "departure_time": "now",
        "key": api_key,
    }

    response = requests.get(url, params=params)
    return response.json()


def format_and_print_time(source, destination, data):

    try:
        routes = data.get("routes")
        if not routes:
            print("Could not get the travel time: No route found")
            return

        leg = routes[0].get("legs")[0]
        traffic_duration = leg.get("duration_in_traffic", leg.get("duration"))
        total_seconds = traffic_duration.get("value")

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        time_str = ""
        if hours > 0:
            hour_word = "hour" if hours == 1 else "hours"
            time_str += f"{hours} {hour_word}"
        if minutes > 0 or hours == 0:
            if hours > 0:
                time_str += " "
            time_str += f"{minutes} minutes"

        print(
            f"Driving from {source} to {destination} takes about {time_str} with current traffic."
        )

    except (ValueError, requests.RequestException) as e:
        print(f"Could not get the travel time: {e!s}")


if __name__ == "__main__":
    try:
        source_place = input("Enter source: ")
        dest_place = input("Enter destination: ")

        api_key = read_api_key()
        api_data = fetch_travel_time(source_place, dest_place, api_key)
        format_and_print_time(source_place, dest_place, api_data)

    except (ValueError, requests.RequestException) as e:
        print(f"Could not get the travel time: {e!s}")
