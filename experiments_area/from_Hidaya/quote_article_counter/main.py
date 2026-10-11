import random

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
