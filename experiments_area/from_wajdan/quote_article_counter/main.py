import random


def create_quotes_file(file_path="quotes.txt"):
    quotes = [
        "The sun is a source of energy.",
        "An apple a day keeps the doctor away.",
        "A friend makes the day better.",
        "The journey starts with a step.",
        "An idea can change the world.",
        "A book is a good friend.",
        "The future starts today.",
        "An honest person earns respect.",
        "A smile brings happiness.",
        "The sky is blue.",
        "A small step makes a difference.",
        "An opportunity is a chance to grow.",
        "The best time is now.",
        "A teacher helps the students.",
        "An artist sees the beauty.",
        "The world needs kindness.",
        "A dream needs an action plan.",
        "The answer is simple.",
        "An effort brings a result.",
        "A mistake is a lesson.",
    ]
    try:
        selected_quotes = random.sample(quotes, 15)

        with open(file_path, "w") as file:
            for quote in selected_quotes:
                file.write(quote + "\n")

    except OSError:
        print("Could not create the quotes file.")
        return False

    return True


