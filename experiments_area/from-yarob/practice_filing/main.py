import random

quotes = [
    "The only way to do great work is to love what you do.",
    "Life is what happens when you're busy making other plans.",
    "The future belongs to those who believe in the beauty of their dreams.",
    "It does not matter how slowly you go as long as you do not stop.",
    "In the end, it's not the years in your life that count. It's the life in your years.",
    "Purpose is the reason you bound out of bed in the morning.",
    "You miss 100% of the shots you don't take.",
    "Whether you think you can or you think you can't, you're right.",
    "The best time to plant a tree was 20 years ago. The second best time is now.",
    "An unexamined life is not worth living.",
    "Your time is limited, don't waste it living someone else's life.",
    "Not how long, but how well you have lived is the main thing.",
    "You must be the change you wish to see in the world.",
    "Spread love everywhere you go. Let no one ever come to you without leaving happier.",
    "Do what you can, with what you have, where you are.",
    "It always seems impossible until it's done.",
    "The only limit to our realization of tomorrow will be our doubts of today.",
    "Keep your face always toward the sunshine and shadows will fall behind you.",
    "What lies behind us and what lies before us are tiny matters compared to what lies within us.",
    "Happiness depends upon ourselves.",
]


def create_quotes_file():
    chosen = random.sample(quotes, 15)
    file = open("quotes.txt", "w", encoding="utf-8")
    for q in chosen:
        file.write(q + "\n")
    file.close()


def append_result(line, a, an, the):
    file = open("quotes_analysis.txt", "a", encoding="utf-8")
    file.write("{a: " + str(a) + ", an: " + str(an) + ", the: " + str(the) + "} " + line + "\n")
    file.close()


def analyze_quotes():
    
    open("quotes_analysis.txt", "w").close()

    try:
        file = open("quotes.txt", "r", encoding="utf-8")
        for line in file:
            line = line.strip()
            words = line.lower().replace(".", " ").replace(",", " ").split()
            a = words.count("a")
            an = words.count("an")
            the = words.count("the")
            append_result(line, a, an, the)
        file.close()
        print("Done, results are in quotes_analysis.txt")
    except FileNotFoundError:
        print("quotes.txt was not found")
    finally:
        print("Finished")


create_quotes_file()
analyze_quotes()