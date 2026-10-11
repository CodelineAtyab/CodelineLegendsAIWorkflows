import random
import re

def create_quotes_file():
    quotes = [ 
        "A fresh start brings hope.",
        "The stars shine at night.",
        "An adventure starts today.",
        "A little practice helps you improve.",
        "The flowers grow in the garden.",
        "An artist sees beauty everywhere.",
        "A happy heart spreads joy.",
        "The rain helps the trees grow.",
        "An answer begins with a question.",
        "A quiet moment brings peace.",
        "The sea is calm today.",
        "An empty page welcomes a story.",
        "A helping hand means a lot.",
        "The moon lights the sky.",
        "An easy task builds confidence.",
        "A warm welcome makes people smile.",
        "The morning brings new chances.",
        "An animal needs love and care.",
        "A simple plan saves time.",
        "The path becomes clear as you walk.",
        "Another try may bring success.",
        "The theme of the day is friendship.",
        ]
    selected_quotes = random.sample(quotes, 15)

    with open ("quotes.txt","w") as file:
        for quote in selected_quotes:
            file.write(quote + "\n")
create_quotes_file()     

def analyze_quotes():
    try:
        with open("quotes.txt", "r") as file:
            for line in file:
                words = re.findall(r"\b[a-z]+\b", line.lower())

                a_count = words.count("a")
                an_count = words.count("an")
                the_count = words.count("the")

                append_result(line, a_count, an_count, the_count)

    except FileNotFoundError:
        print("quotes.txt was not found. Create the quotes file first.")     

def append_result(line, a_count, an_count, the_count):
    quote = line.rstrip("\r\n")

    with open("quotes_analysis.txt", "a") as file:
        file.write(
            f"{{a: {a_count}, an: {an_count}, the: {the_count}}} {quote}\n"
        )
        

if __name__ == "__main__":
    append_result(
    "The best time .\n",
    1,
    0,
    2,
)

    