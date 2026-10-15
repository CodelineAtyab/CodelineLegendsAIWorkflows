# Travel Time Finder 🚗

This Python program estimates the driving time between two places using current traffic conditions.

## API

The program uses the official Google Maps Platform Routes API at `https://routes.googleapis.com/directions/v2:computeRoutes`. It sends the origin and destination in one request with `routingPreference=TRAFFIC_AWARE`, letting Google use the request time as the departure time, then formats the returned traffic-aware `routes.duration`.

I chose this service because its official documentation describes traffic-aware route durations. I found it by checking the Google Maps Platform Routes API documentation for current-traffic routing support.

## Setup and run

1. From this directory, install the project dependencies:
   ```sh
   uv sync
   ```
2. Create `api_key.txt` in this directory and put a Google Maps Platform API key there. Enable the Routes API for the key. The key file is git-ignored; do not commit it.
3. Run the program:
   ```sh
   uv run main.py
   ```

## Example output

```text
Enter source: Muscat
Enter destination: Sohar

Driving from Muscat to Sohar takes about 2 hours 10 minutes with current traffic.
```

The actual travel time depends on current traffic. Errors such as a missing key, invalid route, or API connection problem are reported to the user.

## Troubleshooting

If Google returns HTTP 403, check that Routes API is enabled for the Google Cloud project, billing is active, and the API key belongs to that project and is permitted to use Routes API. `api_key.txt` should contain only the key value. The program prints Google's HTTP error details to help identify the specific issue; never share or commit the key.
