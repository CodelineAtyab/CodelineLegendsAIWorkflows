import random

QUOTES = ["We are what we repeatedly do. Excellence, then, is not an act, but a habit.",
            "The unexamined life is not worth living.", "Knowing is not enough; we must apply.",
            "I have not failed. I've just found 10,000 ways that won't work.",
            "The best time to plant a tree was 20 years ago. The second best time is now.",
            "We suffer more often in imagination than in reality.",
            "Luck is what happens when preparation meets opportunity.",
            "You have power over your mind, not outside events. Realize this, and you will find strength.",
            "It always seems impossible until it's done.",
            "Fall seven times, stand up eight.",
            "The only way to do great work is to love what you do.",
            "Done is better than perfect.",
            "Quality is not an act, it is a habit.",
            "Well begun is half done.",
            "Talk is cheap. Show me the code.",
            "Premature optimization is the root of all evil.",
            "Simplicity is prerequisite for reliability.",
            "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.",
            "Programs must be written for people to read, and only incidentally for machines to execute.",
            "First, solve the problem. Then, write the code.",
            "If you want to go fast, go alone. If you want to go far, go together.",
            "Management is doing things right; leadership is doing the right things.",
            "A leader is best when people barely know he exists.",
            "Alone we can do so little; together we can do so much."]

def create_quotes_file(quotes_list):
    picked_quotes = random.sample(quotes_list, 15)
    try:
        with open("quotes.txt", "w") as file:
            for quote in picked_quotes:
                file.write(quote + "\n")
    except OSError as error:
        print(f"Something else went wrong: {error}")
    else:
        print("Write OK")  
    finally:
        print("Done trying") 

create_quotes_file(QUOTES)