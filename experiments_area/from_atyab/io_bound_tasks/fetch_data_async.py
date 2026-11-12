import requests
from threading import Thread, Lock


# Global List
planet_names: list[str] = []

def fetch_planet_deatils(planet_id):
  response = requests.get(f"https://swapi.info/api/planets/{planet_id}")
  planet_info: dict = response.json()
  planet_names.append(planet_info.get("name")) 


if __name__ == "__main__":
  child_threads: list = []
  for planet_id in range(1, 11):
    curr_thread = Thread(target=fetch_planet_deatils, args=(planet_id,))
    child_threads.append(curr_thread)
    curr_thread.start()

  # Wait for all child threads to finish before printing the results
  for curr_thread in child_threads:
    curr_thread.join()

  print(f"Result: {planet_names}")
  print("End of Main Program (Thread)")