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

# Function 1
def create_quotes_file(file_path="quotes.txt"):
    picked_quotes = random.sample(QUOTES, 15)
    try:
        with open(file_path, "w") as file:
            for quote in picked_quotes:
                file.write(quote + "\n")
    except OSError as error:
        print(f"Something else went wrong: {error}")
    else:
        print("Write OK")  
    finally:
        print("Done trying") 

create_quotes_file()


# Function 2
def analyze_quotes(input_path="quotes.txt", output_path="quotes_analysis.txt"):
    try:
        with open(input_path, "r") as file:
            for line in file:
                article_counts = {'a': 0, 'an': 0, 'the': 0}

                for word in line.split():
                    word = word.lower()
                    if word in ['a', 'an', 'the']:
                        article_counts[word] += 1

                append_result(line.strip(), article_counts, output_path)

    except FileNotFoundError:
        print("That file does not exist yet.")
    except OSError as error:
        print(f"Something else went wrong: {error}")
    else:
        print("Read OK")
    finally:
        print("Done trying")


# Function 3
def append_result(line, article_counts, output_path="quotes_analysis.txt"):
    try:
        with open(output_path, "a") as file:
            file.write(f"{{a: {article_counts['a']}, an: {article_counts['an']}, the: {article_counts['the']}}} {line}\n")
    except OSError as error:
        print(f"Something else went wrong: {error}")
    else:
        print("Write OK")  
    finally:
        print("Done trying")


analyze_quotes()