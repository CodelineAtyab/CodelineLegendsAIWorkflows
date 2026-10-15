from pathlib import Path

import requests


API_KEY_FILE = Path(__file__).with_name("api_key_file.txt")
ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"


def get_api_key():
    api_key = API_KEY_FILE.read_text(encoding="utf-8").strip()
    if not api_key:
        raise ValueError(f"API key is missing from {API_KEY_FILE}")
    return api_key


def get_route_response(source, destination):
    try:
        api_key = get_api_key()
        response = requests.post(
            ROUTES_URL,
            json={
                "origin": {"address": source},
                "destination": {"address": destination},
                "travelMode": "DRIVE",
                "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
            },
            headers={
                "X-Goog-Api-Key": api_key,
                "X-Goog-FieldMask": "routes.duration",
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    except requests.HTTPError as error:
        message = str(error)
        if error.response is not None:
            try:
                message = error.response.json()["error"]["message"]
            except (KeyError, TypeError, ValueError):
                pass
        print(f"Could not get the travel time: {message}")
    except (requests.RequestException, OSError, ValueError) as error:
        print(f"Could not get the travel time: {error}")
    return None


def get_travel_time(data):
    try:
        if "error" in data:
            print("Could not get the travel time:", data["error"].get("message", "API error"))
            return None

        routes = data.get("routes", [])
        if not routes:
            print("Could not get the travel time: no driving route was found")
            return None

        duration = routes[0]["duration"]
        if not duration.endswith("s"):
            raise ValueError("invalid route duration")
        seconds = float(duration[:-1])
        total_minutes = round(seconds / 60)
        hours, minutes = divmod(total_minutes, 60)

        if hours == 0:
            return f"{minutes} {'minute' if minutes == 1 else 'minutes'}"

        hour_text = "hour" if hours == 1 else "hours"
        if minutes == 0:
            return f"{hours} {hour_text}"

        return f"{hours} {hour_text} {minutes} {'minute' if minutes == 1 else 'minutes'}"

    except (KeyError, IndexError, TypeError, ValueError) as error:
        print(f"Could not get the travel time: {error}")
        return None


def main():
    source = input("Enter the source: ").strip()
    destination = input("Enter the destination: ").strip()

    if not source or not destination:
        print("Please enter both a source and a destination.")
        return

    data = get_route_response(source, destination)
    if data is None:
        return

    travel_time = get_travel_time(data)
    if travel_time is None:
        return

    print(
        f"Driving from {source} to {destination} "
        f"takes about {travel_time} with current traffic."
    )


if __name__ == "__main__":
    main()
