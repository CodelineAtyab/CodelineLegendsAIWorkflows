
import requests


def get_activities(activity_type):
    response = requests.get(
        "https://bored-api.appbrewery.com/filter",
        params={"type": activity_type},
    )

    response.raise_for_status()
    data = response.json()

    return data


def show_activities(activities):
    for activity in activities[:3]:
        print("Activity:", activity["activity"])
        print("Participants:", activity["participants"])
        print("--------------------")


def main():
    activity_type = input("Enter activity type: ")

    activities = get_activities(activity_type)

    show_activities(activities)


if __name__ == "__main__":
    main()
