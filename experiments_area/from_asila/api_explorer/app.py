import requests # to use requests library to can communicate with Apis


# send a GET request to the API
def get_joke():
    response = requests.get(
        "https://official-joke-api.appspot.com/random_joke"
    )

    data = response.json()  # to convert JSON response into a Python dictionary
    return data

#to display the result
def display_result(data): 
    print(data.get("setup"))
    print(data.get("punchline"))


def main(): #to start the program and run all the functions in order.
    joke = get_joke()
    display_result(joke)


if __name__ == "__main__":
    main()
    
    
#I choose the Official Joke API to get random jokes.
# I choose it because it is simple to use and lets the program display a joke from an API.