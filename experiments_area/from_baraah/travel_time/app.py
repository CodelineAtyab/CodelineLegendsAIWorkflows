import requests


# Read API key from file
def get_api_key():
    with open("api_key_file.txt", "r") as file:
        return file.read().strip()


# Fetch travel data from Google
def fetch_travel_data(source, destination):
    api_key = get_api_key()

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    params = {
        "origins": source,
        "destinations": destination,
        "mode": "driving",
        "departure_time": "now",
        "traffic_model": "best_guess",
        "key": api_key,
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json()


# Convert travel time into hours and minutes
def get_travel_time(data):
    if data.get("status") != "OK":
        raise ValueError(data.get("error_message", "API error"))

    route = data["rows"][0]["elements"][0]

    if route.get("status") != "OK":
        raise ValueError(route["status"])

    seconds = route["duration_in_traffic"]["value"]
    total = (seconds + 30) // 60
    hours, minutes = divmod(total, 60)

    h = "hour" if hours == 1 else "hours"
    m = "minute" if minutes == 1 else "minutes"

    if hours == 0:
        return f"{minutes} {m}"
    if minutes == 0:
        return f"{hours} {h}"

    return f"{hours} {h} {minutes} {m}"


# Run
def main():
    source = input("Enter the source: ").strip()
    destination = input("Enter the destination: ").strip()

    try:
        data = fetch_travel_data(source, destination)
        travel_time = get_travel_time(data)

        print(
            f"Driving from {source} to {destination} "
            f"takes about {travel_time} with current traffic."
        )

    except (
        requests.RequestException,
        OSError,
        KeyError,
        IndexError,
        TypeError,
        ValueError,
    ) as e:
        print(f"Could not get the travel time: {e}")


if __name__ == "__main__":
    main()
