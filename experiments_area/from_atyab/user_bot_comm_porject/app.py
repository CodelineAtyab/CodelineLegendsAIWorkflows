import os
import json
import requests

def main():
    # PLEASE PLEASE DONT UPDATE IT LATER, ITS CONSTANT! 
    DUMMY_DATA_FILE_PATH = os.path.join(".", "dummy_response.json")
    API_URL = "api.nationalize.io"

    result_dict = {}
    user_name = input("Enter your name: ")
    try:
      response = requests.get(f"https://{API_URL}/?name={user_name}")
      result_dict = response.json()
    except Exception as e:
      with open(DUMMY_DATA_FILE_PATH, "r") as res_file:
        result_dict = json.loads(res_file.read())
      print("Error occurred while making the API request:", str(e))

    with open(DUMMY_DATA_FILE_PATH, "w") as res_file :
      res_file.write(json.dump(result_dict))
      

    list_of_countries = result_dict.get("country")

    for curr_country in list_of_countries:
        print(curr_country.get("country_id"))

if __name__ == "__main__":
    main()