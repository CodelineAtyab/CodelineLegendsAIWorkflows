#Python library used to send HTTP requests to APIs.
import requests

# Find a city and retrieve its weather forecast
def fetch_weather(city):
    

    # Find the city's coordinates.
    #ex: https://geocoding-api.open-meteo.com/v1/search?name=Muscat&count=1&language=en
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    
    #sends a GET request to retrieve information from a server.
    # "count": 1	Requests at most one matching location
    # "language": "en"	Requests English location names
    # timeout=10	Stops waiting if the request takes too long
    # geo_response stores the response returned by the API.
    geo_response = requests.get(
        geo_url,
        params={"name": city, "count": 1, "language": "en"},
        timeout=10
    )
    # .raise_for_status() checks whether the HTTP request was successful.
    geo_response.raise_for_status()
    # The .json() method reads that response and converts the JSON into Python data types(dict).
    # Parse the JSON
    geo_data = geo_response.json()
    '''
    geo_data = {
    "results": [
        {
            "name": "Muscat",
            "latitude": 23.5880,
            "longitude": 58.3829
        }
    ]
}
    '''
    # locations is a list containing a dictionary.
    # Extract the results
    locations = geo_data.get("results", [])

    if not locations:
        print(f"No location found for '{city}'.")
        return None

    location = locations[0]
    latitude = location["latitude"]
    longitude = location["longitude"]

    # Retrieve the weather forecast.
    weather_url = "https://api.open-meteo.com/v1/forecast"
    
    # send a GET request to the weather API with the latitude and longitude of the city 
    weather_response = requests.get(
        weather_url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            # tells the API which measurements to return
            "current": "temperature_2m,relative_humidity_2m,"
                       "apparent_temperature,wind_speed_10m"
        },
        timeout=10
    )
    weather_response.raise_for_status()

    weather_data = weather_response.json()
    # using get() bec sometimes the data may not exist
    return {
        "city": location["name"],
        "country": location.get("country", "Unknown"),
        "weather": weather_data.get("current", {})
    }

# Display weather information in a readable format.
def display_weather(data):
    

    if data is None:
        return

    weather = data["weather"]

    print("\n" + "=" * 35)
    print("          WEATHER REPORT")
    print("=" * 35)
    print(f"City: {data['city']}, {data['country']}")
    print(f"Temperature: {weather.get('temperature_2m')} °C")
    print(f"Feels like: {weather.get('apparent_temperature')} °C")
    print(f"Humidity: {weather.get('relative_humidity_2m')}%")
    print(f"Wind speed: {weather.get('wind_speed_10m')} km/h")
    print("=" * 35)


def main():
    #Run the Weather Explorer application.

    city = input("Enter a city name: ").strip()

    if not city:
        print("Please enter a city name.")
        return

    data = fetch_weather(city)
    display_weather(data)


if __name__ == "__main__":
    main()
