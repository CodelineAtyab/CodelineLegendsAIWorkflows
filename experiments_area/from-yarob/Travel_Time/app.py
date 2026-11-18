import requests


def read_api_key(path="API.txt"):
    with open(path) as f:
        return f.read().strip()


def get_route(source, destination, key):
    response = requests.post(
        "https://routes.googleapis.com/directions/v2:computeRoutes",
        headers={
            "X-Goog-Api-Key": key,
            "X-Goog-FieldMask": "routes.duration",  
        },
        json={
            "origin": {"address": source},
            "destination": {"address": destination},
            "travelMode": "DRIVE",
            "routingPreference": "TRAFFIC_AWARE",  
        },
        timeout=10,
    )
    return response.json()


def get_traffic_seconds(data):
    if data.get("error"):
        raise ValueError(data.get("error").get("message"))
    routes = data.get("routes")
    if not routes:
        raise ValueError("No route found")
    
    duration = routes[0].get("duration")
    return int(duration.rstrip("s"))


def format_time(seconds):
    total_minutes = round(seconds / 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60

    parts = []
    if hours > 0:
        parts.append(f"{hours} hour" + ("" if hours == 1 else "s"))
    if minutes > 0 or hours == 0:
        parts.append(f"{minutes} minute" + ("" if minutes == 1 else "s"))
    return " ".join(parts)


def main():
    source = input("Enter the starting place: ")
    destination = input("Enter the destination: ")

    try:
        key = read_api_key()
        data = get_route(source, destination, key)
        seconds = get_traffic_seconds(data)
        print(
            f"Driving from {source} to {destination} takes about "
            f"{format_time(seconds)} with current traffic."
        )
    except Exception as e:
        print("Could not get the travel time:", str(e))


if __name__ == "__main__":
    main()