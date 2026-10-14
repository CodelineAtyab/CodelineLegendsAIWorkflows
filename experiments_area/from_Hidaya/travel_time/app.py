import requests


def read_api_key():
    with open("google_api_key.txt") as file:
        return file.read().strip()


def get_travel_time_seconds(source, destination, api_key):
    params = {
        "origin": source,
        "destination": destination,
        "mode": "driving",
        "departure_time": "now",
        "key": api_key,
    }

    response = requests.get(
        "https://maps.googleapis.com/maps/api/directions/json",
        params=params,
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "OK":
        raise ValueError(data.get("status", "bad response"))

    return data["routes"][0]["legs"][0]["duration_in_traffic"]["value"]


def format_duration(seconds):
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

    return f"{hour_text} {minute_text}"


def main():
    source = input("Enter source: ").strip()
    destination = input("Enter destination: ").strip()

    try:
        api_key = read_api_key()
        seconds = get_travel_time_seconds(source, destination, api_key)
        duration = format_duration(seconds)

        print(
            f"Driving from {source} to {destination} "
            f"takes about {duration} with current traffic."
        )
    except OSError:
        print("Could not get the travel time: file or network problem")
    except ValueError:
        print("Could not get the travel time: invalid API response")
    except (KeyError, IndexError, TypeError):
        print("Could not get the travel time: traffic time unavailable")


if __name__ == "__main__":
    main()