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
    duration = data["routes"][0]["duration"]
    seconds = int(duration[:-1])
    total_minutes = round(seconds / 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60

    if hours == 1:
        hour_text = "1 hour"
    else:
        hour_text = f"{hours} hours"

    if minutes == 1:
        minute_text = "1 minute"
    else:
        minute_text = f"{minutes} minutes"

    if hours == 0:
        return minute_text
    if minutes == 0:
        return hour_text
    return hour_text + " " + minute_text


def main():
    source = input("Enter source: ").strip()
    destination = input("Enter destination: ").strip()

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
            reason = "Google Routes API request failed"
        else:
            reason = f"Google Routes API returned HTTP {response.status_code}"
        print(f"Could not get the travel time: {reason}")
    except requests.exceptions.RequestException:
        print("Could not get the travel time: no internet connection")
    except (KeyError, IndexError):
        print("Could not get the travel time: Google did not return a route")
    except (OSError, ValueError, TypeError) as error:
        print(f"Could not get the travel time: {error}")


if __name__ == "__main__":
    main()
