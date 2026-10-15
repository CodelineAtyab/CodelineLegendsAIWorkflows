import requests


def read_api_key():
    with open("api_key.txt", "r") as file:
        return file.read().strip()


def fetch_route(source, destination, api_key):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration",
    }
    body = {
        "origin": {"address": source},
        "destination": {"address": destination},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
    }
    response = requests.post(url, headers=headers, json=body, timeout=10)
    response.raise_for_status()
    return response.json()


def format_time(seconds):
    total_minutes = round(seconds / 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60

    parts = []
    if hours == 1:
        parts.append("1 hour")
    elif hours > 1:
        parts.append(f"{hours} hours")

    if minutes == 1:
        parts.append("1 minute")
    elif minutes > 1 or hours == 0:
        parts.append(f"{minutes} minutes")

    return " ".join(parts)


def main():
    source = input("Enter the starting place: ")
    destination = input("Enter the destination: ")

    try:
        api_key = read_api_key()
        data = fetch_route(source, destination, api_key)
        duration_text = data["routes"][0]["duration"]  # looks like "7800s"
        seconds = float(duration_text.replace("s", ""))
    except FileNotFoundError:
        print("Could not get the travel time: key file not found")
    except requests.RequestException:
        print("Could not get the travel time: request failed (check internet or key)")
    except KeyError, IndexError:
        print("Could not get the travel time: place not found")
    else:
        print(
            f"Driving from {source} to {destination} takes about "
            f"{format_time(seconds)} with current traffic."
        )


if __name__ == "__main__":
    main()
