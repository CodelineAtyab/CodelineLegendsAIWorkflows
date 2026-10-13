import requests


ROUTES_API_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"
KEY_FILE = "config.txt"


def read_api_key():
    with open(KEY_FILE, "r") as f:
        return f.read().strip()


def get_travel_data(source, destination, api_key):
    request_headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        # FieldMask is MANDATORY for the Routes API so it knows what data to return
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters",
    }
    request_body = {
        "origin": {"address": source},
        "destination": {"address": destination},
        "travelMode": "DRIVE",
        # TRAFFIC_AWARE makes routes.duration include live traffic.
        # departureTime is left out: it defaults to now, and a time already in
        # the past (even by a second) is rejected by the API.
        "routingPreference": "TRAFFIC_AWARE",
    }
    response = requests.post(ROUTES_API_URL, headers=request_headers, json=request_body, timeout=10)
    return response.json()


def extract_traffic_seconds(data):
    if "error" in data:
        raise ValueError(data.get("error").get("message"))

    routes = data.get("routes")
    if not routes:
        raise ValueError("no route found")

    # duration comes back as a string such as "8790s"
    return int(routes[0].get("duration").rstrip("s"))


def format_duration(total_seconds):
    total_minutes = round(total_seconds / 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60

    parts = []
    if hours > 0:
        parts.append(f"{hours} hour" if hours == 1 else f"{hours} hours")
    if minutes > 0 or hours == 0:
        parts.append(f"{minutes} minute" if minutes == 1 else f"{minutes} minutes")
    return " ".join(parts)


def main():
    source = input("Enter the source: ")
    destination = input("Enter the destination: ")

    try:
        api_key = read_api_key()
        data = get_travel_data(source, destination, api_key)
        travel_seconds = extract_traffic_seconds(data)
        print(f"Driving from {source} to {destination} takes about {format_duration(travel_seconds)} with current traffic.")
    except Exception as ex:
        print(f"Could not get the travel time: {str(ex)}")


if __name__ == "__main__":
    main()
