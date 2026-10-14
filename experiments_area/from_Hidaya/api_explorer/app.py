import requests


def read_api_key():
    try:
        with open("google_api_key.txt") as key_file:
            return key_file.read().strip()
    except OSError:
        print("Could not read the API key file.")
        return None


def get_travel_time_seconds(source, destination, api_key):
    params = {
        "origin": source,
        "destination": destination,
        "mode": "driving",
        "departure_time": "now",
        "key": api_key,
    }

    try:
        response = requests.get(
            "https://maps.googleapis.com/maps/api/directions/json",
            params=params,
        )
        data = response.json()

        if data.get("status") != "OK":
            print(f"Could not get the travel time: {data.get('status', 'bad response')}")
            return None

        seconds = data["routes"][0]["legs"][0]["duration_in_traffic"]["value"]
        return int(seconds)
    except Exception as error:
        print(f"Could not get the travel time: {error}")
        return None


def format_duration(total_minutes):
    hours, minutes = divmod(total_minutes, 60)
    parts = []

    if hours:
        parts.append(f"{hours} hour" + ("s" if hours != 1 else ""))
    if minutes:
        parts.append(f"{minutes} minute" + ("s" if minutes != 1 else ""))

    if not parts:
        parts.append("0 minutes")

    return " ".join(parts)


def main():
    source = input("Enter source: ").strip()
    destination = input("Enter destination: ").strip()

    api_key = read_api_key()
    if api_key is None:
        return

    seconds = get_travel_time_seconds(source, destination, api_key)
    if seconds is None:
        return

    minutes = round(seconds / 60)
    print(
        f"Driving from {source} to {destination} takes about "
        f"{format_duration(minutes)} with current traffic."
    )


if __name__ == "__main__":
    main()
