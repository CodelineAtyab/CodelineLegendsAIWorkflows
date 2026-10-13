
# Import the requests library so this program can make HTTP requests.
import requests


# Define a function that asks the Cat Facts API for a requested number of facts.
def get_cat_facts(number):
    # Build the API URL and insert the requested number as its limit parameter.
    url = f"https://catfact.ninja/facts?limit={number}"

    # Send an HTTP GET request to the URL and keep the server's response.
    response = requests.get(url)

    # Decode the response body from JSON into Python data and return it.
    return response.json()


# Define a function that prints the facts contained in the API response data.
def show_results(data):
    # Get the list stored under "data", or use an empty list if that key is missing.
    facts = data.get("data", [])

    # Loop through each fact, numbering them from 1 instead of the default 0.
    for index, cat in enumerate(facts, start=1):
        # Read the fact text from this item; get() returns None if the key is missing.
        fact = cat.get("fact")
        # Read the fact's character count; get() returns None if the key is missing.
        length = cat.get("length")

        # Print the fact with its number in front of it.
        print(f"{index}. {fact}")
        # Print the character count returned for this fact.
        print(f"Length: {length} characters")
        # Print an empty line to separate this fact from the next one.
        print()


# Define the function that coordinates the user prompt, API call, and output.
def main():
    # Ask the user how many facts to request; input() returns the answer as text.
    number = input("How many cat facts do you want? ")

    # Request that number of facts from the API and save the decoded response.
    data = get_cat_facts(number)

    # Pass the response data to the function that displays the facts.
    show_results(data)


# Check whether this file was run directly, rather than imported by another file.
if __name__ == "__main__":
    # Start the application by calling the main function.
    main()
