import requests

ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"


def read_key():
    with open("api_key.txt", encoding="utf-8") as key_file:
        return key_file.read().strip()


def get_travel_time(source, destination, key):
    request_body = {
        "origin": {"address": source},
        "destination": {"address": destination},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
    }
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": key,
        "X-Goog-FieldMask": "routes.duration",
    }
    response = requests.post(ROUTES_URL, json=request_body, headers=headers, timeout=15)
    response.raise_for_status()
    return response.json()


def format_time(data):
    try:
        duration = data["routes"][0]["duration"]
    except (IndexError, KeyError, TypeError) as error:
        raise ValueError("No route was returned by Google Maps.") from error

    if not isinstance(duration, str) or not duration.endswith("s"):
        raise ValueError("Traffic-aware travel time was not returned.")

    try:
        seconds = float(duration[:-1])
    except ValueError as error:
        raise ValueError("Google Maps returned an invalid travel time.") from error

    minutes = int(seconds / 60 + 0.5)
    hours, remaining_minutes = divmod(minutes, 60)

    parts = []
    if hours:
        unit = "hour" if hours == 1 else "hours"
        parts.append(f"{hours} {unit}")
    if remaining_minutes or not parts:
        unit = "minute" if remaining_minutes == 1 else "minutes"
        parts.append(f"{remaining_minutes} {unit}")

    return " ".join(parts)


def main():
    source = input("Enter source: ")
    destination = input("Enter destination: ")

    try:
        key = read_key()
        data = get_travel_time(source, destination, key)
        time = format_time(data)
        print(
            f"Driving from {source} to {destination} "
            f"takes about {time} with current traffic."
        )
    except requests.exceptions.HTTPError as error:
        response = error.response
        if response is None:
            details = str(error)
        else:
            try:
                details = response.json().get("error", {}).get("message", "")
            except (AttributeError, ValueError):
                details = ""
            details = details or response.text.strip() or str(error)
            details = (
                f"Google Routes API returned HTTP {response.status_code}: {details}"
            )
        print("Could not get the travel time:", details)
    except requests.exceptions.RequestException as error:
        print("Could not connect to Google Routes API:", str(error))
    except (
        OSError,
        ValueError,
        KeyError,
        IndexError,
        TypeError,
        AttributeError,
    ) as error:
        print("Could not get the travel time:", str(error))


if __name__ == "__main__":
    main()
