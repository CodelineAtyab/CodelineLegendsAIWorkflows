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

def append_result(line, article_counts, output_path="quotes_analysis.txt"):
    try:
        with open(output_path, "a") as file:
            # Format the counts and the original quote.
            result = (
                f"{{a: {article_counts['a']}, "
                f"an: {article_counts['an']}, "
                f"the: {article_counts['the']}}} {line}"
            )

            file.write(result + "\n")

    except OSError:
        print("Could not write the result.")
        return False

    return True


def analyze_quotes(input_path="quotes.txt", output_path="quotes_analysis.txt"):
    try:
        with open(input_path, "r") as file:
            # Clear the old analysis results.
            with open(output_path, "w") as output:
                output.write("")

            for line in file:
                line = line.strip()
                article_counts = {"a": 0, "an": 0, "the": 0}

                for word in line.lower().split():
                    word = word.strip(".,!?;:\"'()")

                    if word in article_counts:
                        article_counts[word] += 1

                if append_result(line, article_counts, output_path) == False:
                    return

    except FileNotFoundError:
        print("File or folder not found. Check your paths.")

    except OSError:
        print("Could not analyze the file.")

    else:
        print("Analysis completed.")


if __name__ == "__main__":
    if create_quotes_file():
        analyze_quotes()
   

