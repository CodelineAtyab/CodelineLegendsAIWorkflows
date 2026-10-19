import random
import re

# Function for the quotes
def create_quotes_files():
    quotes = [
        "The best time to plant a tree was 20 years ago.",
        "A journey of a thousand miles begins with a single step.",
        "An investment in knowledge pays the best interest.",
        "The secret of getting ahead is getting started.",
        "Where there is a will, there is a way.",
        "A good book is a great friend.",
        "The future depends on what you do today.",
        "An honest answer is the sign of true friendship.",
        "The only way to do great work is to love what you do.",
        "A person who never made a mistake never tried anything new.",
        "The purpose of life is to contribute in some way.",
        "An early start can make a big difference.",
        "A little progress each day adds up to big results.",
        "The harder you work, the luckier you get.",
        "A calm mind brings inner strength.",
        "An idea can change the world.",
        "The best preparation for tomorrow is doing your best today.",
        "A smile is the shortest distance between two people.",
        "The journey matters more than the destination.",
        "An opportunity rarely arrives at the perfect time.",
        "A kind word can change someone's day.",
        "The more you learn, the more you grow.",
    ]
    quotes_selected = random.sample(quotes, 15)

    
    try:
        with open("quotes_file.txt", "w") as f:
            for q in quotes_selected:
                f.write(q + "\n")
    
    except OSError as er:
        print(f"Couldn't write the quotes to the file: {er}")
    
    else:
        print("Successfully wrote 15 quotes to (quotes_file.txt) file.")

# Append the quotes
def append_result(line, article_counts, output_path="quotes_analysis.txt"):
    result = (f"{{a: {article_counts['a']}, "
              f"an: {article_counts['an']}, "
              f"the: {article_counts['the']}}} {line}\n")
    
    with open(output_path, "a") as file:   # Open analysis file with append mode
        file.write(result)


def analyze_quotes(input_path="quotes_file.txt",
                   output_path="quotes_analysis.txt"):
    try:
        with open(input_path, "r") as file:
            for line in file:
                quote = line.strip()
                words = re.findall(r"\b[a-zA-Z]+\b", quote.lower())

                article_counts = {
                    "a": words.count("a"),
                    "an": words.count("an"),
                    "the": words.count("the"),
                }

                try:
                    append_result(quote, article_counts, output_path)
                except OSError as error:
                    print(f"Couldn't append analysis result: {error}")
                    return

    except FileNotFoundError:
        print(f"Error: The input file '{input_path}' was not found")
    
    except OSError as error:
        print(f"Couldn't read the input file: {error}")
    
    else:
        print(f"Analysis completed. Results saved to {output_path}")

# Run the functions in order
def main():
    create_quotes_files()
    print("Starting quote analysis.....")
    analyze_quotes()


if __name__ == "__main__":
    main()