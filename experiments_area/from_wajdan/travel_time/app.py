import requests


def read_api_key():
    with open("api_key.txt", "r", encoding="utf-8") as key_file:
        return key_file.read().strip()


def get_travel_seconds(api_key, source, destination):
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
        raise ValueError("Google Maps returned an error")

    route = data["routes"][0]
    return sum(
        leg["duration_in_traffic"]["value"] for leg in route["legs"]
    )


def format_duration(seconds):
    minutes = int((seconds + 30) // 60)
    hours, minutes = divmod(minutes, 60)
    parts = []

    if hours:
        unit = "hour" if hours == 1 else "hours"
        parts.append(f"{hours} {unit}")
    if minutes:
        unit = "minute" if minutes == 1 else "minutes"
        parts.append(f"{minutes} {unit}")

    return " ".join(parts) if parts else "0 minutes"


def main():
    try:
        api_key = read_api_key()
        source = input("Enter the source: ")
        destination = input("Enter the destination: ")
        seconds = get_travel_seconds(api_key, source, destination)
        travel_time = format_duration(seconds)
        print(
            f"Driving from {source} to {destination} takes about "
            f"{travel_time} with current traffic."
        )
    except FileNotFoundError:
        print("Could not get the travel time: API key file not found")
    except OSError:
        print("Could not get the travel time: API key file could not be read")
    except requests.exceptions.RequestException:
        print("Could not get the travel time: network request failed")
    except (ValueError, KeyError, IndexError, TypeError):
        print("Could not get the travel time: invalid API response")


if __name__ == "__main__":
    main()
