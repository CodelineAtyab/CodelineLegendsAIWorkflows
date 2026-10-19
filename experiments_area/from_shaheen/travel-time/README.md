# Travel time

This command-line app estimates driving time with current traffic using Google Maps Platform's **Routes API**.

## Set up

1. In the Google Cloud project that owns your existing API key, [enable the Routes API](https://console.cloud.google.com/apis/library/routes.googleapis.com). Billing must be enabled for that project.
2. If your key has API restrictions, add **Routes API** to its allowed APIs in [Credentials](https://console.cloud.google.com/apis/credentials). A key restricted to website referrers cannot authenticate this Python web-service request; use a key with an appropriate application restriction for where the script runs, such as its public IP address.
3. Create a local file named `api_key_file.txt` next to `app.py` and put that **same existing key** inside it. This file is ignored by Git; keep it private.
4. Run `uv run python app.py`, then enter the start and destination as addresses.

The program requests only the route duration. Google's `TRAFFIC_AWARE` routing preference uses live traffic data, and with no departure time the estimate is for now. Routes API usage may be billed according to your Google Maps Platform plan.

If something goes wrong, the app prints `Could not get the travel time:` followed by the reason (for example Google's own message). If that message says the API key is not valid or the API is not enabled, check that Routes API is enabled in the **same project as the key** and that the key's API and application restrictions allow this request.
