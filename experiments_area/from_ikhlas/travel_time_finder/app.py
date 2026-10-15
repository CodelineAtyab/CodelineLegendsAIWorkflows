import os
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

url="https://routes.googleapis.com/directions/v2:computeRoutes"

# To read the api key from .env file 
def read_api():
    load_dotenv()
    return os.getenv("GOOGLE_MAPS_API_KEY")


# To get the travel time from google routs api
def fetch_api_data(source, destination, API_KEY):
    body = {
    "origin": {"address": source},
    "destination": {"address": destination},
    "travelMode": "DRIVE",
    "routingPreference": "TRAFFIC_AWARE",
    "departureTime": (datetime.now(timezone.utc) + timedelta(minutes=1)).isoformat(timespec="seconds").replace("+00:00", "Z")}

    headers={
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"}

    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code != 200:  #to check the API status - if it is working or not
        print(response.text)

    response.raise_for_status()
    data = response.json()
    duration = data.get("routes", [])[0].get("duration")
    total_seconds = int(duration.rstrip("s"))

    return round(total_seconds / 60)


#track and format travel timing
def travel_time(total_duration):
    hours = total_duration // 60
    mins = total_duration % 60

    if hours == 0:
        return f"{mins} minutes"
    elif hours == 1:
        return f"1 hour {mins} minutes" if mins else "1 hour"
    elif mins == 0:
        return f"{hours} hours"
    else:
        return f"{hours} hours {mins} minutes"



def main():
    try:
        api_key = read_api()
        if not api_key:
            raise ValueError("Google maps API key is missing in .env file")
        
        source = input("Enter starting source place: ")
        destination = input("Enter destination: ")
        total_minutes = fetch_api_data(source, destination, api_key)
        formatted_time = travel_time(total_minutes)

        print(f"Driving from {source} to {destination} "
              f"takes about {formatted_time} with current traffic.")

    except Exception as ex:
        print(f"Couldn't get the travel time: {ex}")

if __name__ == "__main__":
    main()