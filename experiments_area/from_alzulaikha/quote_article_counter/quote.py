import random

def create_quotes_file(file_path="quotes.txt"):
    quotes = [
    "A brave person never gives up.",
    "The ocean is full of hidden wonders.",
    "An old friend is a special treasure.",
    "A new day brings new hope.",
    "The moon looks beautiful tonight.",
    "An active mind loves to learn.",
    "A warm smile can spread happiness.",
    "The little things make life special.",
    "An amazing story begins with an idea.",
    "A clear goal helps you succeed.",
    "The rain makes the flowers grow.",
    "An empty mind cannot learn much.",
    "A good habit improves your life.",
    "The right choice can change everything.",
    "An unexpected moment can bring joy.",
    "A strong team works together.",
    "The morning breeze feels refreshing.",
    "An interesting book opens new doors.",
    "A little kindness goes a long way.",
    "The road to success starts with effort.",
]


     selected_quotes = random.sample(quotes, 15)
     try:
        with open(file_path, "w") as file:
            file.writelines(quote + "\n" for quote in selected_quotes)

     except OSError as error:
        print(f"Error creating quotes file: {error}")
     else:
        print("Quotes file created successfully.")
