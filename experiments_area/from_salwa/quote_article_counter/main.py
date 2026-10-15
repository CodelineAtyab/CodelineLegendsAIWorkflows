import random

quotes = [
    "The best time to start is now.",
    "A journey begins with a single step.",
    "An apple a day keeps the doctor away.",
    "The future belongs to those who learn.",
    "A small change makes a big difference.",
    "An idea can change the world.",
    "The sun shines after the rain.",
    "A good book opens a new world.",
    "An honest answer builds trust.",
    "The secret of success is hard work.",
    "A kind word can change a day.",
    "An opportunity may come at any time.",
    "The sky is full of stars.",
    "A new day brings new hope.",
    "An old friend is a treasure.",
    "The road to success needs patience.",
    "A little practice improves a skill.",
    "An open mind learns new things.",
    "The best lessons come from experience.",
    "A dream needs action to become real.",
    "The world is full of possibilities.",
    "An early start can save time.",
]

# Function : Create quotes.txt


# Function: Create quotes.txt
def create_quotes_file(file_path="quotes.txt"):
    selected_quotes = random.sample(quotes, 15)

    try:
        with open(file_path, "w") as file:
            file.writelines(quote + "\n" for quote in selected_quotes)

    except OSError as error:
        print(f"Could not create the file: {error}")

    else:
        print("Quotes file created successfully.")

    finally:
        print("Create quotes operation finished.")


# Function : Append one result
def append_result(
    line,
    article_counts,
    output_path="quotes_analysis.txt",
):
    result = (
        f"{{a: {article_counts['a']}, "
        f"an: {article_counts['an']}, "
        f"the: {article_counts['the']}}} "
        f"{line.strip()}\n"
    )

    try:
        with open(output_path, "a") as file:
            file.write(result)

    except OSError as error:
        print(f"Could not append the result: {error}")


# Function : Analyze quotes
def analyze_quotes(
    input_path="quotes.txt",
    output_path="quotes_analysis.txt",
):
    try:
        # Clear old analysis results
        with open(output_path, "w") as file:
            pass

        with open(input_path, "r") as file:
            for line in file:
                article_counts = {
                    "a": 0,
                    "an": 0,
                    "the": 0,
                }

                words = line.lower().split()

                for word in words:
                    word = word.strip(".,!?;:\"'()")

                    if word == "a":
                        article_counts["a"] += 1
                    elif word == "an":
                        article_counts["an"] += 1
                    elif word == "the":
                        article_counts["the"] += 1

                append_result(
                    line,
                    article_counts,
                    output_path,
                )

    except FileNotFoundError:
        print(f"Sorry, {input_path} does not exist.")

    except OSError as error:
        print(f"File operation failed: {error}")

    else:
        print("Analysis completed successfully.")

    finally:
        print("Analysis attempt finished.")


# Run the program
if __name__ == "__main__":
    create_quotes_file()
    analyze_quotes()
