import random
import re

quotes = [
    "The sun rises over the mountains every morning.",
    "A journey of a thousand miles begins with a single step.",
    "An apple a day keeps the doctor away.",
    "The best way to learn is to practice every day.",
    "A good programmer understands the problem before writing the code.",
    "The future belongs to those who believe in a dream.",
    "An opportunity is a chance to make the world better.",
    "The more you practice, the better you become.",
    "A small mistake can teach an important lesson.",
    "The theme of the story is another mystery.",
    "An honest person always tells the truth.",
    "A developer needs an idea and the courage to build it.",
    "The road to success is a long and difficult journey.",
    "Another day brings a new opportunity to learn.",
    "The answer to a problem is not always the easiest one.",
    "An engineer can turn a simple idea into a useful tool.",
    "A book is a window into the world of knowledge.",
    "The teacher gave an example to the students.",
    "A strong team needs the trust of every member.",
    "The artist created a beautiful painting in an hour.",
    "An unexpected challenge can become a valuable experience.",
    "The Python language is a powerful tool for developers.",
    "A curious mind asks the questions others forget.",
    "The adventure begins with an idea and a plan.",
    "THE cat found A toy near AN old house.",
]



def create_quotes_file():
    selected_quotes = random.sample(quotes, 15)

    try:
        with open("quotes.txt", "w") as file:
            for quote in selected_quotes:
                file.write(quote + "\n")

    except OSError as error:
        print(f"Something went wrong: {error}")



def append_result(quote, A, AN, THE):
    try:
        with open("quotes_analysis.txt","a") as analyzed:
            analyzed.write(f"{{a:{A},an:{AN},the:{THE}}} {quote}")

    except OSError as error:
            print(f"Something went wrong: {error}")



def analyzed_quotes():
    try:
        with open("quotes.txt","r") as file:
            for quote in file:
                A = len(re.findall(r"\ba\b", quote, re.IGNORECASE))
                AN = len(re.findall(r"\ban\b", quote, re.IGNORECASE))
                THE = len(re.findall(r"\bthe\b", quote, re.IGNORECASE))

                append_result(quote, A, AN, THE)


    except FileNotFoundError:
        print("The File You Want is Not Found")

    except OSError as error:
                print(f"Something went wrong: {error}")

    else:
        print("Quotes analysis completed.")


create_quotes_file()


with open("quotes_analysis.txt", "w"):
    pass

analyzed_quotes()