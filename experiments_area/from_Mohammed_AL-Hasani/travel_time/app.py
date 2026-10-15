
import requests


# Reads API key from a text file.
def read_api_key():
    with open("api_key.txt", "r") as file:
        return file.read().strip()


# Sends the request to Google Routes API.
def get_travel_data(source, destination, api_key):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    
    
    #tell the server like how the data is formatted and which API key to use.
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration",
    }

    params = {
        "origin": {
            "address": source,
        },
        "destination": {
            "address": destination,
        },
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
    }

    response = requests.post(
        url,
        headers=headers,
        json=params,
        timeout=10,
    )
    response.raise_for_status() #checks whether the HTTP request was successful or returned an HTTP error.
    return response.json()


# Converts seconds into hours and minutes.
def format_time(seconds):
    minutes = round(seconds / 60)
    hours = minutes // 60
    minutes = minutes % 60

    if hours == 0:
        return f"{minutes} minutes"

    hour_text = "hour" if hours == 1 else "hours"

    if minutes == 0:
        return f"{hours} {hour_text}"

    return f"{hours} {hour_text} {minutes} minutes"


# Controls the main program.
def main():
    try:
        key = read_api_key()
        source = input("Enter the source location: ")
        destination = input("Enter the destination location: ")

        data = get_travel_data(source, destination, key)

        routes = data.get("routes", [])

        if not routes:
            raise ValueError("No route found.")

        duration = routes[0].get("duration")

        if not duration:
            raise ValueError("Travel duration is unavailable.")

        seconds = float(duration.removesuffix("s"))
        travel_time = format_time(seconds)

        print(
            f"Driving from {source} to {destination} "
            f"takes about {travel_time} with current traffic."
        )

    except (
        OSError,
        requests.RequestException,
        ValueError,
        TypeError,
        KeyError,
        IndexError,
    ) as e:
        print(f"Could not get the travel time: {e}")


if __name__ == "__main__":
    main()
