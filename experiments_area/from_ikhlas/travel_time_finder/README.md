# Travel Time Finder

A Python app that calculates estimated driving time between two locations using the Google Routes API with traffic-aware routing.

## Setup
1. Install dependencies:
   ```bash
   uv add requests python-dotenv
   ```
2. Add your API key to `.env`:
   ```env
   GOOGLE_MAPS_API_KEY=your_api_key_here
   ```
3. Run the app:
   ```bash
   uv run app.py
   ```

## Features
- Accepts source and destination.
- Calculates traffic-aware travel time.
- Handles errors with `try/except`.

**Security:** Add `.env` to `.gitignore` and never commit your API key.