import requests


def get_api_key():
    with open("api_key_file.txt", "r") as file:
        return file.read().strip()


def get_api_key_respon(source, destination):
    try:
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

    except requests.RequestException as e:
        print(f"Could not get the travel time: {e}")
        return None

    except OSError as e:
        print(f"Could not read the API key: {e}")
        return None


def get_travel_time(data):
    try:
        if data.get("status") != "OK":
            print(
                "Could not get the travel time:",
                data.get("error_message", data.get("status", "API error")),
            )
            return None

        elements = data["rows"][0]["elements"][0]

        if elements.get("status") != "OK":
            print("Could not get the travel time:", elements.get("status"))
            return None

        seconds = elements["duration_in_traffic"]["value"]

        total_minutes = (seconds + 30) // 60

        hours, minutes = divmod(total_minutes, 60)

        if hours == 0:
            return f"{minutes} minutes"

        hour_text = "hour" if hours == 1 else "hours"

        if minutes == 0:
            return f"{hours} {hour_text}"

        return f"{hours} {hour_text} {minutes} minutes"

    except (KeyError, IndexError, TypeError, ValueError) as e:
        print(f"Could not get the travel time: {e}")
        return None


def main():
    source = input("Enter the source: ").strip()
    destination = input("Enter the destination: ").strip()

    data = get_api_key_respon(source, destination)

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
