import requests


def read_api_key():
    with open('api_key.txt', 'r') as file:
        return file.read().strip()
    
def get_travel_data(source, destination, api_key):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    
    params = {
        "origins": source,
        "destinations": destination,
        "departure_time": "now",
        "key": api_key
    }
    
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status() 
    return response.json()

def format_time(seconds):
     minutes = round(seconds / 60)
     hours = minutes // 60
     minutes = minutes % 60
     
     if hours == 0:
         return f"{minutes} minutes"
     if minutes == 0:
         return f"{hours} {'hour' if hours == 1 else 'hours'}"
     
     
     
     return f"{hours} hours and {minutes} minutes" if hours else f"{minutes} minutes"
 
def main():
    try:
        key = read_api_key()
        source = input("Enter the source location: ")
        destination = input("Enter the destination location: ")
        
        data = get_travel_data(source, destination, key)
        
        if data.get("status") != "OK":
            raise ValueError(data.get("error_message", data.get("status")))
        
        route = data.get("rows")[0].get("elements")[0]
        if route.get("status") != "OK":
            raise ValueError(route.get("status"))

        seconds = route.get("duration_in_traffic").get("value")
        travel_time = format_time(seconds)
        
        print(
    f"Driving from {source} to {destination} "
    f"takes about {travel_time} with current traffic."
    )
        
    except requests.RequestException as e:
        print("could not get travel time:", str(e))
        
if __name__ == "__main__":
    main()