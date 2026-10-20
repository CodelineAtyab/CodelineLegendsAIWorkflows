Weather Explorer is a Python application that retrieves current weather information for a city entered by the user. It uses the Open-Meteo APIs to find the city's coordinates and fetch its current weather conditions.

The application displays the temperature, feels-like temperature, relative humidity, and wind speed in a readable format.

Features:

1- Search for a city by name.
2- Retrieve the city's coordinates using the Open-Meteo Geocoding API.
3- Fetch current weather information.
4- Display temperature, feels-like temperature, humidity, and wind speed.
5- Handle cases where no matching location is found.
6- Use request timeouts and HTTP error checking.

Example output:

===================================
          WEATHER REPORT
===================================
City: Muscat, Oman
Temperature: 30 °C
Feels like: 32 °C
Humidity: 65%
Wind speed: 12 km/h
===================================