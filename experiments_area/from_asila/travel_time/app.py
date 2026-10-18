import requests 
from urllib.parse import quote



def read_api_key():
    with open("api_key.txt", "r") as file:  #read the key from the file.
        key = file.read().strip()

    return key

# Convert a place name into coordinates for TomTom.
def get_coordinates(place, key):
    response = requests.get(
        f"https://api.tomtom.com/search/2/geocode/{quote(place, safe='')}.json",
        params={"key": key,"limit": 1}
    )
    
    
    if not response.ok:
        raise ValueError(f"Location request failed: HTTP {response.status_code}")

    data = response.json()
    position = data.get("results")[0].get("position")
    return f"{position['lat']},{position['lon']}"



# Request a driving route with current traffic.
def get_travel_data(source, destination, key):
    start = get_coordinates(source, key)
    end = get_coordinates(destination, key)

    response = requests.get(
        f"https://api.tomtom.com/routing/1/calculateRoute/{start}:{end}/json",
        params={
            "key": key,
            "travelMode": "car",
            "traffic": "true",
            "departAt": "now",
            "computeTravelTimeFor": "all"
        }
    )

    if not response.ok:
        raise ValueError("Driving route request failed")

    return response.json()


# convert the traffic time into hours and minutes.
def format_time(data):
    summary = data.get("routes")[0].get("summary")
    seconds = summary.get("liveTrafficIncidentsTravelTimeInSeconds")

    if seconds is None:
        raise ValueError("Current traffic time is unavailable")

    total_minutes = int(seconds / 60 + 0.5)
    hours = total_minutes // 60
    minutes = total_minutes % 60

    parts = []

    if hours > 0:
        hour_word = "hour" if hours == 1 else "hours"
        parts.append(f"{hours} {hour_word}")

    if minutes > 0 or hours == 0:
        minute_word = "minute" if minutes == 1 else "minutes"
        parts.append(f"{minutes} {minute_word}")

    return " ".join(parts)


def main():
    #Ask for the source and destination.
    source = input("Enter the source: ")
    destination = input("Enter the destination: ")

    #Handle request and parsing failures.
    try:
        key = read_api_key()
        data = get_travel_data(source, destination, key)
        travel_time = format_time(data)

        #Print the required result.
        print(
            f"Driving from {source} to {destination} takes about "
            f"{travel_time} with current traffic."
        )

    except requests.exceptions.RequestException:
        print("Could not get the travel time: Network request failed")
    except Exception as error:
        print(f"Could not get the travel time: {error}")


if __name__ == "__main__":
    main()
