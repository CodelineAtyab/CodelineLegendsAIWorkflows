import requests


DISTANCE_MATRIX_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"
KEY_FILE = "config.txt"


def read_api_key():
    with open(KEY_FILE, "r") as f:
        return f.read().strip()


def get_travel_data(source, destination, api_key):
    request_params = {
        "origins": source,
        "destinations": destination,
        "mode": "driving",
        # departure_time=now makes Google return live traffic
        "departure_time": "now",
        "key": api_key,
    }
    response = requests.get(DISTANCE_MATRIX_URL, params=request_params, timeout=10)
    return response.json()


def extract_duration_in_traffic(data):
    if data.get("status") != "OK":
        raise ValueError(data.get("error_message", data.get("status")))

    element = data.get("rows")[0].get("elements")[0]
    if element.get("status") != "OK":
        raise ValueError(f"no route found ({element.get('status')})")

    return element.get("duration_in_traffic").get("text")


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


# ---------------------------------------------------------------------------
# Alternative: Google Routes API (the newer API Google recommends).
# Kept commented out because the issue requires requests.get(...) with params=,
# and the Routes API only accepts POST with a JSON body.
# To use it, uncomment these two functions and swap them into main() in place of
# get_travel_data / extract_traffic_seconds.
# ---------------------------------------------------------------------------
# ROUTES_API_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"
#
#
# def get_travel_data_routes(source, destination, api_key):
#     request_headers = {
#         "Content-Type": "application/json",
#         "X-Goog-Api-Key": api_key,
#         # FieldMask is MANDATORY for the Routes API so it knows what data to return
#         "X-Goog-FieldMask": "routes.duration,routes.distanceMeters",
#     }
#     request_body = {
#         "origin": {"address": source},
#         "destination": {"address": destination},
#         "travelMode": "DRIVE",
#         # TRAFFIC_AWARE makes routes.duration include live traffic.
#         # departureTime is left out: it defaults to now, and a time already in
#         # the past (even by a second) is rejected by the API.
#         "routingPreference": "TRAFFIC_AWARE",
#     }
#     response = requests.post(ROUTES_API_URL, headers=request_headers, json=request_body, timeout=10)
#     return response.json()
#
#
# def extract_traffic_seconds_routes(data):
#     if "error" in data:
#         raise ValueError(data.get("error").get("message"))
#
#     routes = data.get("routes")
#     if not routes:
#         raise ValueError("no route found")
#
#     # duration comes back as a string such as "8790s"
#     return int(routes[0].get("duration").rstrip("s"))


def main():
    source = input("Enter the source: ")
    destination = input("Enter the destination: ")

    try:
        api_key = read_api_key()
        data = get_travel_data(source, destination, api_key)
        duration_text = extract_duration_in_traffic(data)
        print(f"Driving from {source} to {destination} takes about {duration_text} with current traffic.")
    except Exception as ex:
        print(f"Could not get the travel time: {str(ex)}")


if __name__ == "__main__":
    main()
