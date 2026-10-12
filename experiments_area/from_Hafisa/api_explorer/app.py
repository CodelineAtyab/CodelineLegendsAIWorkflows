import requests


def get_city(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"

    response = requests.get(url)
    data = response.json()

    location = data.get("results")[0]

    return location


def get_weather(latitude, longitude):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&hourly=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
        "&forecast_days=1"
        "&timezone=auto"
    )

    response = requests.get(url)

    return response.json()


def show_weather(data, city):
    hourly = data.get("hourly")

    times = hourly.get("time")
    temperatures = hourly.get("temperature_2m")
    humidity = hourly.get("relative_humidity_2m")
    rain = hourly.get("precipitation")
    wind = hourly.get("wind_speed_10m")

    print(f"\nHourly weather for {city}:\n")

    for index in range(len(times)):
        print(f"Time: {times[index]}")
        print(f"Temperature: {temperatures[index]} °C")
        print(f"Humidity: {humidity[index]}%")
        print(f"Rain: {rain[index]} mm")
        print(f"Wind: {wind[index]} km/h")
        print("--------------------")


def main():
    city = input("Enter an Oman city: ")

    location = get_city(city)

    latitude = location.get("latitude")
    longitude = location.get("longitude")

    weather = get_weather(latitude, longitude)

    show_weather(weather, city)


if __name__ == "__main__":
    main()