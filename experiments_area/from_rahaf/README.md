# Travel Time Finder 🚗

## Description
This Python program calculates the driving time between two places using the TomTom API and current traffic information.

## Features
- Asks the user to enter a starting place and destination.
- Uses the TomTom API to get driving time.
- Displays the travel time in hours and minutes.
- Reads the API key from a separate file.
- Handles errors using try/except.

## API Used
**TomTom API**

I chose this API because it provides driving routes with current traffic information.

## How to Run
1. Install requests:
   ```
   uv add requests
   ```
2. Create a file called `api_key.txt` and add your TomTom API key.
3. Run the program:
   ```
   uv run app.py
   ```

## Example Output
```text
Enter source: Muscat
Enter destination: Sohar

Driving from Muscat to Sohar takes about 2 hours 10 minutes with current traffic.
```

*The actual travel time depends on current traffic.*

## Error Handling
I used `try/except` to handle errors such as missing files, invalid locations, and API connection problems.

## What I Learned
- How to use `requests.get()` to call an API.
- How to use `.json()` to read API responses.
- How to read files using `with open()`.
- How to handle errors using `try/except`.
- How to work with dictionaries and functions.
