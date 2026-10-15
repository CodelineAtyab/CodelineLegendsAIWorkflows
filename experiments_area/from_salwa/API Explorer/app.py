import requests

activity_type = input("Enter activity type: ")

response = requests.get(
    "https://bored-api.appbrewery.com/filter",
    params={"type": activity_type},
)
data = response.json()

for activity in data[:3]:
    print("Activity:", activity["activity"])
    print("Participants:", activity["participants"])
    print("--------------------")
