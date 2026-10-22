import requests

KEY_FILE = "api_key.txt"
URL = "https://routes.googleapis.com/directions/v2:computeRoutes"


def read_api_key(path=KEY_FILE):
    with open(path) as key_file:
        return key_file.read().strip()


def fetch_route(source, destination, api_key):
    headers = {
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration",
    }
    body = {
        "origin": {"address": source},
        "destination": {"address": destination},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
    }
    response = requests.post(URL, headers=headers, json=body, timeout=10)
    data = response.json()
    if not response.ok:
        error_msg = data.get("error", {}).get("message", "API request failed")
        raise ValueError(error_msg)
    return data


def get_traffic_seconds(data):
    routes = data.get("routes")
    if not routes:
        raise ValueError("no route found")
    return int(routes[0].get("duration").rstrip("s"))


def format_duration(seconds):
    total_minutes = round(seconds / 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    parts = []
    if hours:
        parts.append(f"{hours} {'hour' if hours == 1 else 'hours'}")
    if minutes or not hours:
        parts.append(f"{minutes} {'minute' if minutes == 1 else 'minutes'}")
    return " ".join(parts)


def main():
    source = input("Source: ").strip()
    destination = input("Destination: ").strip()
    try:
        api_key = read_api_key()
        data = fetch_route(source, destination, api_key)
        seconds = get_traffic_seconds(data)
        print(
            f"Driving from {source} to {destination} takes about "
            f"{format_duration(seconds)} with current traffic."
        )
    except (requests.RequestException, OSError, ValueError, KeyError, IndexError, TypeError) as e:
        print("Could not get the travel time:", str(e))


if __name__ == "__main__":
    main()
