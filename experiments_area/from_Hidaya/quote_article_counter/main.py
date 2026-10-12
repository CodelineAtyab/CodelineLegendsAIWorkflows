import random
import re

def create_quotes_file(file_path="quotes.txt"):
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
    try:
        with open(file_path, "w") as file:
            for quote in selected_quotes:
                file.write(quote + "\n")

    except OSError as error:
        print(f"Could not create {file_path}: {error}")
        return False

    else:
        print(f"{file_path} created successfully.")
        return True    
def analyze_quotes(input_path="quotes.txt", output_path="quotes_analysis.txt"):
    try:
        with open(input_path, "r") as file:
            with open(output_path, "w") as output:
                output.write("")
            for line in file:
                words = re.findall(r"\b[a-z]+\b", line.lower())

                article_counts = {
                    "a": words.count("a"),
                    "an": words.count("an"),
                    "the": words.count("the"),
                }

                saved = append_result(line, article_counts, output_path)

                if not saved:
                    return

    except FileNotFoundError:
        print(f"{input_path} was not found. Create the quotes file first.")

    except OSError as error:
        print(f"Could not analyze the files: {error}")

    else:
        print("Analysis completed successfully.")  

def append_result(line, article_counts, output_path="quotes_analysis.txt"):
    quote = line.rstrip("\r\n")
    try:
        with open(output_path, "a") as file:
            file.write(
                f"{{a: {article_counts['a']}, "
                f"an: {article_counts['an']}, "
                f"the: {article_counts['the']}}} {quote}\n"
            )
    except OSError as error:
        print(f"Could not save the result: {error}")
        return False

    return True
        

if __name__ == "__main__":
    if create_quotes_file():
        analyze_quotes()
  

    