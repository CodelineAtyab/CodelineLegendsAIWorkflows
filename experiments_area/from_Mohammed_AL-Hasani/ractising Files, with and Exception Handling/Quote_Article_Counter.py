import random
import re
def create_quotes_file(file_path="quotes.txt"):
    quotes =[
        "Small steps still move you forward.",
        "Curiosity turns ordinary days into discoveries.",
        "Every sunrise is a fresh page.",
        "Patience gives good ideas room to grow.",
        "Choose progress over perfection.",
        "A kind word can change the shape of a day.",
        "The best path is often made by walking it.",
        "Make space for wonder, even in routine.",
        "Mistakes are maps to what you can learn next.",
        "Listen closely; insight often arrives quietly.",
        "Bravery can begin with one honest question.",
        "Share what you know, and your light multiplies.",
        "Rest is part of the journey, not a delay.",
        "Build a life that leaves room for laughter.",
        "Hope is a small flame worth tending.",
        "Seek out the stories that make you feel alive.",
        "Gratitude turns what we have into enough.",
        "The world is wide, and your curiosity is a compass.",
        "Every ending is a chance to start anew.",
        "Courage is found in the moments we choose to act.",
        "The quiet moments often hold the loudest truths.",]
    
    selected_quotes = random.sample(quotes, 15)
    
    try:
         with open(file_path, "w") as file:
            for quote in selected_quotes:
             file.write(quote + "\n")
    except OSError as error:
        print(f"Error creating quotes file: {error}")


def append_result(line, article_counts, output_path="quotes_analysis.txt"):
    try:
        with open(output_path, "a") as file:
            file.write(
                f"{{a: {article_counts['a']}, an: {article_counts['an']}, the: {article_counts['the']}}} {line}\n"
            )
    except OSError as error:
        print(f"Error writing analysis file: {error}")
        
        



def analyze_quotes(input_path="quotes.txt", output_path="quotes_analysis.txt"):
    try:
        with open(input_path, "r") as file:
            for line in file:
                quote = line.strip()

                a_count = len(re.findall(r"\ba\b", quote, re.IGNORECASE))
                an_count = len(re.findall(r"\ban\b", quote, re.IGNORECASE))
                the_count = len(re.findall(r"\bthe\b", quote, re.IGNORECASE))

                article_count = {
                    "a": a_count,
                    "an": an_count,
                    "the": the_count
                }

                append_result(quote, article_count, output_path)

    except FileNotFoundError:
        print("quotes.txt was not found")

    except OSError as error:
        print(f"{input_path}An error occurred: {error}")

    else:
        print("Quote analysis completed successfully.")

create_quotes_file()

with open("quotes_analysis.txt", "w") as file:
    pass

analyze_quotes()


