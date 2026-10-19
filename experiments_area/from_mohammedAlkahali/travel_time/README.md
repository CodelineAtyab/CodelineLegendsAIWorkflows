# Travel Time Finder (#126)

A small terminal script that asks for a starting place and a destination, calls the **Google Routes API**, and prints the driving time with current traffic.

Practises: the `requests` library, sending and reading JSON, reading a file with `with`, and `try/except/else`.

## How it works

1. `read_api_key()` reads the Google API key from `api_key.txt`.
2. `fetch_route()` sends a `POST` request to the Routes API (`computeRoutes`) with:
   - the origin and destination as addresses
   - `travelMode: DRIVE` and `routingPreference: TRAFFIC_AWARE`
   - a field mask so the API returns only `routes.duration`
3. The API returns the duration as a string like `"7800s"`. The script strips the `s` and converts it to seconds.
4. `format_time()` turns the seconds into readable text, e.g. `2 hours 10 minutes`.

## Setup

1. Install dependencies:
```bash
   uv sync
```
2. Create a file called `api_key.txt` in this folder and put your Google API key in it (one line, nothing else). The **Routes API** must be enabled for that key.

> ⚠️ `api_key.txt` is listed in `.gitignore` and must **never** be committed.

## Run

```bash
uv run app.py
```

Example:

```
Enter the starting place: Muscat
Enter the destination: Nizwa
Driving from Muscat to Nizwa takes about 1 hour 45 minutes with current traffic.
```

## Error handling

| Problem | Message shown |
|---|---|
| `api_key.txt` is missing | key file not found |
| No internet, invalid key, or API error | request failed (check internet or key) |
| Place not found / empty response | place not found |