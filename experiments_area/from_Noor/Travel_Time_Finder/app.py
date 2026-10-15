
import requests


# Read the API key from a local file.
def read_api_key():
    with open("api_key.txt", "r", encoding="utf-8") as file:
        return file.read().strip()


# Find a city's latitude and longitude.
# API key, which authorizes your request.
def get_coordinates(city, api_key):
    # creates the URL used to search for the city.
    url = f"https://api.tomtom.com/search/2/geocode/{city}.json"
    # sends an HTTP GET request
    # Sends your API key for authorization
    response = requests.get(
        url,
        params={"key": api_key, "limit": 1},
        timeout=10
    )
    response.raise_for_status()
    # Convert JSON into Python data
    # for example:
    '''
    data = {
    "results": [
        {
            "position": {
                "lat": 23.5880,
                "lon": 58.3829
            }
        }
    ]
}
'''
    # this 
    data = response.json()
    results = data.get("results", [])

    if not results:
        raise ValueError(f"No location found for '{city}'.")

    position = results[0]["position"]

    return position["lat"], position["lon"]


# Get the driving time using current traffic information.
def fetch_travel_time(source, destination, api_key):
    start_lat, start_lon = get_coordinates(source, api_key)
    end_lat, end_lon = get_coordinates(destination, api_key)

    route = (
        f"{start_lat},{start_lon}:"
        f"{end_lat},{end_lon}"
    )
    # Build the API URL
    url = (
        "https://api.tomtom.com/routing/1/"
        f"calculateRoute/{route}/json"
    )

    # Send the HTTP request
    # https://example.com/route?key=YOUR_API_KEY&traffic=true
    # "traffic": "true": calculate the route using available traffic information.
    response = requests.get(
        url,
        params={
            "key": api_key,
            "traffic": "true"
        },
        timeout=10
    )
    response.raise_for_status()

    data = response.json()
    routes = data.get("routes", [])

    if not routes:
        raise ValueError("No driving route was found.")

    return routes[0]["summary"]["travelTimeInSeconds"]


# Convert seconds into a readable time.
def format_time(seconds):
    # Convert seconds into minutes
    total_minutes = round(seconds / 60)
    hours = total_minutes // 60
    # Calculate the remaining minutes
    minutes = total_minutes % 60

    if hours == 0:
        return f"{minutes} minutes"

    hour_word = "hour" if hours == 1 else "hours"

    if minutes == 0:
        return f"{hours} {hour_word}"

    return f"{hours} {hour_word} {minutes} minutes"


# Run the application.
def main():
    source = input("Enter the starting place: ").strip()
    destination = input("Enter the destination: ").strip()

    if not source or not destination:
        print("Please enter both places.")
        return

    try:
        api_key = read_api_key()

        if not api_key:
            print("Could not get the travel time: API key is empty.")
            return

        seconds = fetch_travel_time(source, destination, api_key)
        travel_time = format_time(seconds)

        print(
            f"Driving from {source} to {destination} takes "
            f"about {travel_time} with current traffic."
        )

    except (requests.RequestException, ValueError, KeyError) as error:
        print(f"Could not get the travel time: {error}")

    except OSError:
        print("Could not get the travel time: Could not read api_key.txt.")


if __name__ == "__main__":
    main()
