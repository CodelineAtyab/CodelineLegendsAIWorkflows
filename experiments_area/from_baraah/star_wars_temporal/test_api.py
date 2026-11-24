#test 1
#import asyncio

#from activities import find_character


#async def main():
 #   character = await find_character("Luke Skywalker")
  #  print(character["name"])
 #   print(character["homeworld"])


#asyncio.run(main())

#test2
#import asyncio

#from activities import find_character, get_homeworld


#async def main():
    # First, find the character.
   # character = await find_character("Luke Skywalker")

    # Use the first request's result in the second request.
   # homeworld = await get_homeworld(character["homeworld"])

  #  print("Character:", character["name"])
   # print("Homeworld:", homeworld)


#asyncio.run(main())

#test3

import asyncio

from activities import find_character, get_films, get_homeworld


async def main():
    # Step 1: Find the character.
    character = await find_character("Luke Skywalker")

    # Step 2: Get the character's homeworld.
    homeworld = await get_homeworld(character["homeworld"])

    # Step 3: Get every film title.
    films = []

    for film_url in character["films"]:
        title = await get_films(film_url)
        films.append(title)

    print("Character:", character["name"])
    print("Homeworld:", homeworld)
    print("Films:", films)


asyncio.run(main())
