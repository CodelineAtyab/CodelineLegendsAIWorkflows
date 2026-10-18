import requests


# Read API key from file
def get_api_key():
    with open("api_key_file.txt", "r") as file:
        return file.read().strip()


# Fetch travel data from Google Routes API
def fetch_travel_data(source, destination):
    api_key = get_api_key()

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

    response = requests.post(url, headers=headers, json=body, timeout=30)

    # Show error message 
    if not response.ok:
        try:
            message = response.json().get("error", {}).get("message", "API error")
        except ValueError:
            message = "Google API request failed"

        raise ValueError(message)

    return response.json()


# Convert travel time into hours and minutes
def get_travel_time(data):
    if not data.get("routes"):
        raise ValueError("No route found")

    seconds = float(data["routes"][0]["duration"].rstrip("s"))
    total = round(seconds / 60)

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